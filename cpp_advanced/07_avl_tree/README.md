# AVL Tree

**Level:** Advanced | **Concepts:** self-balancing BST, rotations, templates

A templated AVL tree: insert/erase/search in guaranteed O(log n) by
tracking a balance factor per node and rebalancing via single/double
rotations whenever an insertion or deletion pushes a subtree's height
difference beyond 1.

## Files

- `avl_tree.hpp` — `AVLTree<T>`: `insert`, `erase`, `contains`, `height`,
  `in_order()` (sorted traversal), with all four rotation cases
  (left-left, right-right, left-right, right-left)
- `main.cpp` — inserts a sequence designed to trigger each rotation case,
  verifies the tree stays balanced (height stays within `O(log n)`) and
  sorted after a mix of inserts/erases

## How to run

```bash
make
./avl_demo
```

## Notes

Balance factor = height(right) - height(left); a node is rebalanced when
`|balance| > 1`. The four rotation cases are distinguished by the sign of
the balance factor at the node *and* at the offending child — that's the
part that's easy to get backwards, so `main.cpp` explicitly checks the
resulting height bound rather than just eyeballing output.
