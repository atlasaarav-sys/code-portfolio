# 02 — C++ Data Structures

**Language:** C++17
**Level:** Intermediate

## What this demonstrates

- Class templates (generic containers)
- `std::unique_ptr` for automatic ownership/cleanup (no manual `delete`)
- Operator overloading
- Exceptions (`std::out_of_range`)

## Files

- `linked_list.hpp` — templated singly linked list class
- `stack.hpp` — templated stack built on `std::vector`
- `main.cpp` — exercises both, plus a templated `BST<T>` for search/insert

## How to run

```bash
make
./data_structures_demo
```

## Notes

Headers are templates, so they're header-only (no separate .cpp to compile)
— `main.cpp` includes them directly. Builds and runs clean under g++/C++17.
