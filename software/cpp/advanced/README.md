# C++ Advanced Projects

Ten systems-level C++17 projects — each a self-contained implementation of
a data structure or technique you'd otherwise reach for a library to get:
custom memory management, lock-free concurrency, parsers, and classic
algorithms/data structures built from scratch.

## Projects

| # | Project | Concepts |
|---|---|---|
| 1 | [Custom Memory Allocator](01_custom_memory_allocator) | fixed-size pool allocator, placement new, free lists |
| 2 | [Lock-Free Ring Buffer](02_lock_free_ring_buffer) | SPSC queue, `std::atomic`, memory ordering |
| 3 | [Work-Stealing Thread Pool](03_work_stealing_thread_pool) | per-thread deques, work stealing, `std::jthread` |
| 4 | [LRU Cache](04_lru_cache) | templates, intrusive doubly-linked list + hash map, O(1) get/put |
| 5 | [JSON Parser](05_json_parser) | recursive descent parsing, variant-based value tree |
| 6 | [Regex Engine](06_regex_engine) | Thompson NFA construction + simulation |
| 7 | [AVL Tree](07_avl_tree) | self-balancing BST, rotations, templates |
| 8 | [Graph Algorithms](08_graph_algorithms) | generic graph, BFS/DFS, Dijkstra, topological sort |
| 9 | [Expression Evaluator](09_expression_evaluator) | shunting-yard, operator precedence, RPN evaluation |
| 10 | [Custom Smart Pointers](10_custom_smart_pointers) | `unique_ptr`/`shared_ptr` reimplementation, control blocks |

## Notes

None of this is machine-compiled in the authoring environment (no C++
toolchain installed there) — every project has a `Makefile` targeting
g++/C++17; build locally (`make`) before relying on it. Code follows the
same conventions as [`software/cpp`](..): headers for reusable
components, a `main.cpp` demo/test driver per project.
