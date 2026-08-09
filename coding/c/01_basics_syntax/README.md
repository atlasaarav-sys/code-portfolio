# 01 — C Basics & Syntax

**Language:** C (C11)
**Level:** Beginner

## What this demonstrates

- Variables, types, format specifiers
- Control flow (if/else, for, while, switch)
- Functions, pointers, pass-by-reference
- Arrays and `sizeof`
- `struct` basics

## Files

- `basics.c` — syntax tour
- `pointers.c` — pointer/array/pass-by-reference exercises
- `structs.c` — struct usage with a small `Point`/`Rectangle` example

## How to run

```bash
make
./basics
./pointers
./structs
```

Or compile individually:

```bash
gcc -Wall -Wextra -std=c11 -o basics basics.c
```

## Notes

Written/reviewed for standard C11 correctness; not machine-compiled in the
authoring environment (no toolchain installed there) — compile locally with
`make` before relying on it, and open an issue/fix forward if anything
doesn't build.
