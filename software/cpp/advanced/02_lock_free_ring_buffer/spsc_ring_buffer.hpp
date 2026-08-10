#pragma once

#include <atomic>
#include <cstddef>
#include <optional>

// Single-producer/single-consumer lock-free ring buffer.
// Capacity must be a power of two (enforced via static_assert) so index
// wraparound is a cheap bitmask instead of a modulo.
template <typename T, size_t Capacity>
class SPSCRingBuffer {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be a power of two");

public:
    // Called only from the producer thread.
    bool push(T value) {
        size_t tail = tail_.load(std::memory_order_relaxed);
        size_t next_tail = (tail + 1) & mask_;

        if (next_tail == head_.load(std::memory_order_acquire)) {
            return false; // full
        }

        buffer_[tail] = std::move(value);
        tail_.store(next_tail, std::memory_order_release);
        return true;
    }

    // Called only from the consumer thread.
    std::optional<T> pop() {
        size_t head = head_.load(std::memory_order_relaxed);

        if (head == tail_.load(std::memory_order_acquire)) {
            return std::nullopt; // empty
        }

        T value = std::move(buffer_[head]);
        head_.store((head + 1) & mask_, std::memory_order_release);
        return value;
    }

    bool empty() const {
        return head_.load(std::memory_order_acquire) == tail_.load(std::memory_order_acquire);
    }

private:
    static constexpr size_t mask_ = Capacity - 1;
    T buffer_[Capacity];
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
};
