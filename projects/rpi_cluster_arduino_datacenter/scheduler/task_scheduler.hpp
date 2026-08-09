#pragma once

#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

// A minimal thread-pool task scheduler. Each worker thread stands in for
// one cluster node pulling work off a shared queue.
class TaskScheduler {
public:
    explicit TaskScheduler(size_t num_workers) : stop_(false) {
        for (size_t i = 0; i < num_workers; i++) {
            workers_.emplace_back([this] { worker_loop(); });
        }
    }

    ~TaskScheduler() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto &t : workers_) {
            if (t.joinable()) {
                t.join();
            }
        }
    }

    void submit(std::function<void()> task) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            tasks_.push(std::move(task));
        }
        cv_.notify_one();
    }

    // Blocks until the task queue is empty and all in-flight tasks finish.
    void wait_idle() {
        std::unique_lock<std::mutex> lock(mutex_);
        idle_cv_.wait(lock, [this] { return tasks_.empty() && active_tasks_ == 0; });
    }

private:
    void worker_loop() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(mutex_);
                cv_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
                if (stop_ && tasks_.empty()) {
                    return;
                }
                task = std::move(tasks_.front());
                tasks_.pop();
                active_tasks_++;
            }

            task();

            {
                std::lock_guard<std::mutex> lock(mutex_);
                active_tasks_--;
                if (tasks_.empty() && active_tasks_ == 0) {
                    idle_cv_.notify_all();
                }
            }
        }
    }

    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mutex_;
    std::condition_variable cv_;
    std::condition_variable idle_cv_;
    size_t active_tasks_ = 0;
    bool stop_;
};
