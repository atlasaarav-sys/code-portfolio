#pragma once

#include <atomic>
#include <deque>
#include <functional>
#include <mutex>
#include <optional>
#include <random>
#include <thread>
#include <vector>

class WorkStealingPool {
public:
    explicit WorkStealingPool(size_t num_workers)
        : deques_(num_workers), mutexes_(num_workers), stop_(false), active_tasks_(0) {
        for (size_t i = 0; i < num_workers; i++) {
            workers_.emplace_back([this, i] { worker_loop(i); });
        }
    }

    ~WorkStealingPool() {
        wait_idle();
        stop_.store(true, std::memory_order_release);
        for (auto &t : workers_) {
            if (t.joinable()) t.join();
        }
    }

    // Submit from outside the pool (round-robins across workers).
    void submit(std::function<void()> task) {
        size_t idx = next_submit_.fetch_add(1, std::memory_order_relaxed) % deques_.size();
        {
            std::lock_guard<std::mutex> lock(mutexes_[idx]);
            deques_[idx].push_back(std::move(task));
        }
        active_tasks_.fetch_add(1, std::memory_order_relaxed);
    }

    void wait_idle() {
        while (active_tasks_.load(std::memory_order_acquire) > 0) {
            std::this_thread::yield();
        }
    }

private:
    void worker_loop(size_t self_idx) {
        std::mt19937 rng(std::random_device{}() + static_cast<unsigned>(self_idx));

        while (!stop_.load(std::memory_order_acquire)) {
            std::optional<std::function<void()>> task = pop_own(self_idx);
            if (!task) {
                task = steal_from_peer(self_idx, rng);
            }

            if (task) {
                (*task)();
                active_tasks_.fetch_sub(1, std::memory_order_release);
            } else {
                std::this_thread::yield();
            }
        }
    }

    std::optional<std::function<void()>> pop_own(size_t idx) {
        std::lock_guard<std::mutex> lock(mutexes_[idx]);
        if (deques_[idx].empty()) return std::nullopt;
        auto task = std::move(deques_[idx].back()); // LIFO for the owner
        deques_[idx].pop_back();
        return task;
    }

    std::optional<std::function<void()>> steal_from_peer(size_t self_idx, std::mt19937 &rng) {
        size_t n = deques_.size();
        std::uniform_int_distribution<size_t> dist(0, n - 1);

        for (size_t attempts = 0; attempts < n; attempts++) {
            size_t victim = dist(rng);
            if (victim == self_idx) continue;

            std::lock_guard<std::mutex> lock(mutexes_[victim]);
            if (!deques_[victim].empty()) {
                auto task = std::move(deques_[victim].front()); // FIFO for the thief
                deques_[victim].pop_front();
                return task;
            }
        }
        return std::nullopt;
    }

    std::vector<std::thread> workers_;
    std::vector<std::deque<std::function<void()>>> deques_;
    std::vector<std::mutex> mutexes_;
    std::atomic<size_t> next_submit_{0};
    std::atomic<bool> stop_;
    std::atomic<long> active_tasks_;
};
