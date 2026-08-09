# 02 — Python Data Structures

**Language:** Python 3
**Level:** Intermediate

## What this demonstrates

- Implementing classic data structures from scratch (no relying on
  `collections`/`heapq` internals) to understand how they work
- Classes, `__repr__`, generics via duck typing
- Recursion (BST traversal)
- Big-O tradeoffs between structures

## Files

- `linked_list.py` — singly linked list (insert, delete, search, reverse)
- `stack_queue.py` — stack and queue built on the linked list, plus a
  balanced-parentheses checker using the stack
- `binary_search_tree.py` — BST with insert/search/delete and in-order,
  pre-order, post-order traversal

## How to run

```bash
python linked_list.py
python stack_queue.py
python binary_search_tree.py
```

Each file has a `if __name__ == "__main__":` demo block that exercises the
structure and prints results.
