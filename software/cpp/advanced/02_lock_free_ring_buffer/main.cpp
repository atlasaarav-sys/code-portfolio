#include <atomic>
#include <cstdio>
#include <thread>
#include <vector>

#include "spsc_ring_buffer.hpp"

int main() {
    constexpr size_t CAPACITY = 1024;
    constexpr int NUM_ITEMS = 2'000'000;

    SPSCRingBuffer<int, CAPACITY> ring;
    std::atomic<bool> producer_done{false};

    std::thread producer([&] {
        for (int i = 0; i < NUM_ITEMS; i++) {
            while (!ring.push(i)) {
                std::this_thread::yield(); // buffer full, back off
            }
        }
        producer_done.store(true, std::memory_order_release);
    });

    std::vector<int> received;
    received.reserve(NUM_ITEMS);

    std::thread consumer([&] {
        while (true) {
            auto value = ring.pop();
            if (value.has_value()) {
                received.push_back(*value);
            } else if (producer_done.load(std::memory_order_acquire) && ring.empty()) {
                break;
            } else {
                std::this_thread::yield();
            }
        }
    });

    producer.join();
    consumer.join();

    bool ok = received.size() == static_cast<size_t>(NUM_ITEMS);
    for (int i = 0; ok && i < NUM_ITEMS; i++) {
        if (received[i] != i) {
            ok = false;
            std::printf("MISMATCH at index %d: expected %d, got %d\n", i, i, received[i]);
        }
    }

    std::printf("Pushed %d items, received %zu items.\n", NUM_ITEMS, received.size());
    std::printf("Order/completeness check: %s\n", ok ? "PASS" : "FAIL");

    return ok ? 0 : 1;
}
