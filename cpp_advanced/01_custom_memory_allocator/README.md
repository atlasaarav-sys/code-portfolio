# Custom Memory Allocator

**Level:** Advanced | **Concepts:** fixed-size pool allocation, free lists, placement new

A fixed-block-size pool allocator: pre-allocates one large arena, carves it
into equal-size slots, and hands them out/takes them back via an intrusive
free list (no per-allocation `malloc`/`free` once the pool is primed).
Includes a `PoolAllocator<T>` adapter usable as a C++ `Allocator` with
STL containers (e.g. `std::vector<T, PoolAllocator<T>>`).

## Files

- `pool_allocator.hpp` — `FixedPool` (raw fixed-size-block allocator) and
  `PoolAllocator<T>` (STL-compatible adapter)
- `main.cpp` — demo: allocates/frees from the pool directly, then uses
  `PoolAllocator<int>` with `std::vector` and times it against the default
  allocator for many small allocations

## How to run

```bash
make
./allocator_demo
```

## Notes

`FixedPool` only supports blocks of a single size (set at construction) —
that's the whole point: no size-class bookkeeping, no fragmentation beyond
what you get from never coalescing (which never happens because every
block is the same size).
