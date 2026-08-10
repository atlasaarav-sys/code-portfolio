# 02 — C Data Structures

**Language:** C (C11)
**Level:** Intermediate

## What this demonstrates

- Manual memory management (`malloc`/`free`), avoiding leaks
- Singly linked list with dynamic allocation
- Stack implemented on a linked list
- Simple hash table with chaining (string keys, `unsigned long` values)

## Files

- `linked_list.c` — dynamically allocated linked list (insert/delete/print/free)
- `stack.c` — array-based stack (push/pop/peek) with a balanced-parens demo
- `hash_table.c` — fixed-bucket-count hash table with separate chaining

## How to run

```bash
make
./linked_list
./stack
./hash_table
```

## Notes

Every `malloc` has a matching `free`; run under `valgrind` (Linux/WSL) to
verify no leaks if you want to double-check.
