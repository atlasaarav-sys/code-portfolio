#pragma once

#include <cstddef>
#include <cstdlib>
#include <new>
#include <stdexcept>

// Fixed-size-block pool allocator. Pre-allocates `capacity` blocks of
// `block_size` bytes each and hands them out via an intrusive free list
// (the free block's own memory stores the "next free" pointer).
class FixedPool {
public:
    FixedPool(size_t block_size, size_t capacity)
        : block_size_(block_size < sizeof(void *) ? sizeof(void *) : block_size),
          capacity_(capacity) {
        arena_ = static_cast<std::byte *>(std::malloc(block_size_ * capacity_));
        if (!arena_) {
            throw std::bad_alloc();
        }

        free_list_ = reinterpret_cast<void **>(arena_);
        void **current = free_list_;
        for (size_t i = 0; i < capacity_ - 1; i++) {
            void **next = reinterpret_cast<void **>(arena_ + (i + 1) * block_size_);
            *current = next;
            current = next;
        }
        *current = nullptr;
    }

    ~FixedPool() {
        std::free(arena_);
    }

    FixedPool(const FixedPool &) = delete;
    FixedPool &operator=(const FixedPool &) = delete;

    void *allocate() {
        if (!free_list_) {
            throw std::bad_alloc(); // pool exhausted
        }
        void *block = free_list_;
        free_list_ = *reinterpret_cast<void **>(block);
        in_use_++;
        return block;
    }

    void deallocate(void *block) {
        *reinterpret_cast<void **>(block) = free_list_;
        free_list_ = reinterpret_cast<void **>(block);
        in_use_--;
    }

    size_t block_size() const { return block_size_; }
    size_t capacity() const { return capacity_; }
    size_t in_use() const { return in_use_; }

private:
    size_t block_size_;
    size_t capacity_;
    size_t in_use_ = 0;
    std::byte *arena_ = nullptr;
    void **free_list_ = nullptr;
};

// STL-compatible allocator adapter. All instances sharing the same pool
// pointer are considered equal (required for container copy semantics).
template <typename T>
class PoolAllocator {
public:
    using value_type = T;

    explicit PoolAllocator(FixedPool &pool) : pool_(&pool) {}

    template <typename U>
    PoolAllocator(const PoolAllocator<U> &other) : pool_(other.pool_) {}

    T *allocate(size_t n) {
        if (n != 1) {
            // This simple pool only hands out single fixed-size blocks;
            // fall back to global new for bulk allocations.
            return static_cast<T *>(::operator new(n * sizeof(T)));
        }
        return static_cast<T *>(pool_->allocate());
    }

    void deallocate(T *p, size_t n) {
        if (n != 1) {
            ::operator delete(p);
            return;
        }
        pool_->deallocate(p);
    }

    template <typename U>
    bool operator==(const PoolAllocator<U> &other) const { return pool_ == other.pool_; }
    template <typename U>
    bool operator!=(const PoolAllocator<U> &other) const { return pool_ != other.pool_; }

    template <typename U> friend class PoolAllocator;

private:
    FixedPool *pool_;
};
