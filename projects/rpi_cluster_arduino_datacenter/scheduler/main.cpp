#include <atomic>
#include <chrono>
#include <cstdio>
#include <vector>

#include "task_scheduler.hpp"

// A deliberately compute-bound task (counts primes below `limit`) so wall
// time actually reflects parallel work, not I/O waiting.
long count_primes_below(long limit) {
    long count = 0;
    for (long n = 2; n < limit; n++) {
        bool is_prime = true;
        for (long d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            count++;
        }
    }
    return count;
}

double run_benchmark(size_t num_workers, int num_tasks, long work_per_task) {
    std::atomic<long> total{0};

    auto start = std::chrono::steady_clock::now();
    {
        TaskScheduler scheduler(num_workers);
        for (int i = 0; i < num_tasks; i++) {
            scheduler.submit([&total, work_per_task] {
                total += count_primes_below(work_per_task);
            });
        }
        scheduler.wait_idle();
    }
    auto end = std::chrono::steady_clock::now();

    std::chrono::duration<double> elapsed = end - start;
    std::printf("  workers=%zu tasks=%d -> %.3f s (checksum=%ld)\n",
                num_workers, num_tasks, elapsed.count(), total.load());
    return elapsed.count();
}

int main() {
    const int NUM_TASKS = 20;
    const long WORK_PER_TASK = 200000;

    std::printf("Single-node baseline (1 worker):\n");
    double single_node_time = run_benchmark(1, NUM_TASKS, WORK_PER_TASK);

    std::printf("\n5-node cluster (5 workers):\n");
    double cluster_time = run_benchmark(5, NUM_TASKS, WORK_PER_TASK);

    double speedup_pct = (single_node_time - cluster_time) / single_node_time * 100.0;
    std::printf("\nParallel workload-processing speedup vs. single-node: %.1f%%\n", speedup_pct);

    return 0;
}
