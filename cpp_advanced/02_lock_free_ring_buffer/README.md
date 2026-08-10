# Lock-Free Ring Buffer (SPSC)

**Level:** Advanced | **Concepts:** `std::atomic`, memory ordering, single-producer/single-consumer queues

A single-producer/single-consumer lock-free ring buffer: one thread calls
`push()`, another calls `pop()`, and neither ever blocks on a mutex — just
`std::atomic<size_t>` head/tail indices with acquire/release ordering. This
specific design (SPSC, power-of-two capacity) is the classic "first
lock-free structure to actually get right" exercise.

## Files

- `spsc_ring_buffer.hpp` — the ring buffer itself, templated on element type and capacity
- `main.cpp` — one producer thread pushing N items, one consumer thread
  popping them, verifying every item arrives exactly once and in order

## How to run

```bash
make
./ring_buffer_demo
```

## Notes

Correctness here rests entirely on the acquire/release pairing around the
head/tail indices — `push()` writes the data *then* releases the new tail;
`pop()` acquires the tail *before* reading the data, so the consumer never
observes a slot write that hasn't happened yet. This is the one thing to
scrutinize if you extend this to MPMC — the invariants change.
