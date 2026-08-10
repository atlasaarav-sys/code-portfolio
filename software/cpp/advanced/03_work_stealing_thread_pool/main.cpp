#include <atomic>
#include <chrono>
#include <cstdio>

#include "work_stealing_pool.hpp"

// Deliberately uneven recursive workload: expensive on the left branch,
// cheap on the right, so a naive fixed-assignment scheduler stalls while
// stealing keeps every worker busy.
long fib_work(int n) {
    if (n < 2) return n;
    long a = fib_work(n - 1);
    long b = fib_work(n - 2);
    return a + b;
}

void run_uneven_workload(WorkStealingPool &pool, std::atomic<long> &total) {
    // A handful of large tasks (left) and many small tasks (right) submitted
    // together -- workers that finish their own small tasks early should
    // steal pieces of the large ones instead of idling.
    for (int i = 0; i < 4; i++) {
        pool.submit([&total] { total += fib_work(30); });
    }
    for (int i = 0; i < 40; i++) {
        pool.submit([&total] { total += fib_work(20); });
    }
    pool.wait_idle();
}

int main() {
    const size_t NUM_WORKERS = 4;
    std::atomic<long> total{0};

    auto start = std::chrono::steady_clock::now();
    {
        WorkStealingPool pool(NUM_WORKERS);
        run_uneven_workload(pool, total);
    }
    auto elapsed = std::chrono::steady_clock::now() - start;

    std::printf("Work-stealing pool (%zu workers): checksum=%ld, %.3f s\n",
                NUM_WORKERS, total.load(),
                std::chrono::duration<double>(elapsed).count());
    std::printf("(Compare against this repo's simpler single-queue pool in\n"
                " hardware/embedded-projects/rpi_cluster_arduino_datacenter/scheduler for the shared-queue baseline.)\n");

    return 0;
}
