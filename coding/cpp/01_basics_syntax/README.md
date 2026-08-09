# 01 — C++ Basics & Syntax (OOP intro)

**Language:** C++17
**Level:** Beginner

## What this demonstrates

- Variables, references, `auto`
- Control flow, range-based for
- Functions, function overloading, default args
- `std::vector`, `std::string`
- Basic classes: constructors, member functions, `const` correctness

## Files

- `basics.cpp` — syntax tour
- `shapes.cpp` — small class hierarchy (`Shape` base, `Circle`/`Rectangle`
  derived, virtual `area()`) — first taste of OOP/polymorphism

## How to run

```bash
make
./basics
./shapes
```

## Notes

Not machine-compiled in the authoring environment (no toolchain installed
there) — build locally with `make` (g++, C++17) before relying on it.
