# Work-Stealing Thread Pool

**Level:** Advanced | **Concepts:** per-thread task deques, work stealing, load balancing

A thread pool where each worker owns its own task deque instead of all
workers pulling from one shared queue: a worker pushes/pops its own
submissions from one end (LIFO, good cache locality), and when its own
deque is empty it "steals" a task from the *other* end of a random peer's
deque (FIFO from the thief's perspective, which minimizes contention with
the owner). This is the technique behind Cilk, TBB, and Rust's Rayon.

## Files

- `work_stealing_pool.hpp` — `WorkStealingPool`: N worker threads, N
  mutex-protected deques (a real lock-free deque is its own project; this
  uses a small per-deque mutex, which is still far less contended than one
  global queue since a worker almost always touches only its own deque)
- `main.cpp` — benchmark: a recursive fibonacci-via-tasks workload
  (deliberately uneven — some subtrees are cheap, some expensive) run
  against a single shared-queue pool vs. the work-stealing pool, showing
  the imbalance-handling difference

## How to run

```bash
make
./work_stealing_demo
```

## Notes

The uneven recursive workload is the point: a naive round-robin/shared
queue pool leaves some workers idle while one worker chews through a large
subtree; stealing lets idle workers grab pieces of that subtree instead of
waiting.
