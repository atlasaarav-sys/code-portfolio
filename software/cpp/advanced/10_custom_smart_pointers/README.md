# Custom Smart Pointers

**Level:** Advanced | **Concepts:** RAII, move semantics, reference counting, control blocks

Reimplementations of `std::unique_ptr` and `std::shared_ptr` (simplified,
no custom deleters or arrays) — to actually understand what the standard
library versions are doing under the hood: move-only ownership for
`MyUniquePtr`, and a separate heap-allocated control block holding an
atomic reference count for `MySharedPtr`.

## Files

- `my_unique_ptr.hpp` — `MyUniquePtr<T>`: move-only, deletes the managed
  object on destruction or reset, copy constructor/assignment explicitly
  deleted
- `my_shared_ptr.hpp` — `MySharedPtr<T>`: control block
  (`std::atomic<int>` ref count + raw pointer) shared across copies;
  object is deleted when the count hits zero; thread-safe increment/
  decrement
- `main.cpp` — exercises both: move semantics on `MyUniquePtr`, copy/share
  semantics and destruction timing on `MySharedPtr`, verified via a
  `Tracked` type that counts constructions/destructions

## How to run

```bash
make
./smart_ptr_demo
```

## Notes

`MySharedPtr` deliberately does *not* implement `weak_ptr` or
`enable_shared_from_this` — those require a second counter (weak count)
in the control block and are the natural "next feature" once the
strong-count-only version is solid.
