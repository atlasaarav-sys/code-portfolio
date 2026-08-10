# Algorithms Toolkit

**Stack:** Python 3, stdlib only

A small library of classic algorithms — sorting, searching, and graph
traversal — each implemented from scratch with a docstring stating its
time/space complexity, a full `unittest` suite, and a benchmark CLI that
empirically measures runtime growth against input size (so the claimed
Big-O isn't just asserted, it's shown).

## What's included

- `algorithms/sorting.py` — quicksort (Lomuto partition), mergesort, heapsort
- `algorithms/searching.py` — binary search (iterative), binary search
  variants (`find_first`, `find_last` for duplicate-containing arrays)
- `algorithms/graph.py` — BFS, DFS, Dijkstra's shortest path (adjacency-list graph)
- `benchmark.py` — times each sort against growing random input sizes and
  prints the ratio between consecutive runs (an O(n log n) algorithm's
  runtime ratio should track `2*log2(2n)/log2(n)` roughly, not `2` or `4`,
  which is what you'd see from O(n) or O(n^2) instead)

## How to run

```bash
python -m unittest discover tests
python benchmark.py
```

## What's tested

- Correctness against Python's built-in `sorted()`/`in` as ground truth,
  including edge cases (empty input, single element, already-sorted,
  reverse-sorted, duplicates)
- Graph algorithms against hand-verified small graphs with known shortest
  paths/traversal orders (same style as
  [`software/cpp/advanced/08_graph_algorithms`](../../software/cpp/advanced/08_graph_algorithms)
  in this repo, but in Python and with an empirical complexity benchmark
  added on top)

## Notes

This isn't meant to replace `sorted()`/`heapq`/etc. for real use — the
point is showing the algorithms work correctly and that their measured
runtime growth actually matches the complexity claimed in each
docstring, which is the part a lot of "I implemented quicksort" projects
skip.
