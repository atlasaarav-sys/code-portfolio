#include <chrono>
#include <cstdio>
#include <vector>

#include "pool_allocator.hpp"

struct Vec3 {
    float x, y, z;
};

void demo_raw_pool() {
    FixedPool pool(sizeof(Vec3), 8);

    std::printf("Raw pool: block_size=%zu capacity=%zu\n", pool.block_size(), pool.capacity());

    void *blocks[8];
    for (int i = 0; i < 8; i++) {
        blocks[i] = pool.allocate();
    }
    std::printf("Allocated 8/8 blocks (in_use=%zu)\n", pool.in_use());

    pool.deallocate(blocks[3]);
    pool.deallocate(blocks[5]);
    std::printf("Freed 2 blocks (in_use=%zu)\n", pool.in_use());

    void *reused = pool.allocate();
    std::printf("Reallocated one block (LIFO reuse expected): %s\n",
                (reused == blocks[5]) ? "matches last-freed block" : "different block");

    for (int i = 0; i < 8; i++) {
        if (i != 3 && i != 5) pool.deallocate(blocks[i]);
    }
    pool.deallocate(reused);
}

void demo_stl_adapter() {
    FixedPool pool(sizeof(int), 100000);
    PoolAllocator<int> alloc(pool);

    const int N = 50000;

    auto start = std::chrono::steady_clock::now();
    std::vector<int, PoolAllocator<int>> pooled_vec(alloc);
    pooled_vec.reserve(N);
    for (int i = 0; i < N; i++) pooled_vec.push_back(i);
    auto pooled_time = std::chrono::steady_clock::now() - start;

    start = std::chrono::steady_clock::now();
    std::vector<int> default_vec;
    default_vec.reserve(N);
    for (int i = 0; i < N; i++) default_vec.push_back(i);
    auto default_time = std::chrono::steady_clock::now() - start;

    std::printf("\nSTL adapter: pushed %d ints\n", N);
    std::printf("  pool-backed vector:    %lld us\n",
                static_cast<long long>(std::chrono::duration_cast<std::chrono::microseconds>(pooled_time).count()));
    std::printf("  default-alloc vector:  %lld us\n",
                static_cast<long long>(std::chrono::duration_cast<std::chrono::microseconds>(default_time).count()));
    std::printf("  (both reserve() up front, so this mostly shows steady-state allocator overhead)\n");
}

int main() {
    demo_raw_pool();
    demo_stl_adapter();
    return 0;
}
