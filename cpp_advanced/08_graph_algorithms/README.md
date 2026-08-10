# Graph Algorithms

**Level:** Advanced | **Concepts:** adjacency-list graph, BFS/DFS, Dijkstra, topological sort

A generic weighted directed graph (adjacency list, integer node IDs) plus
four classic algorithms implemented directly against it: BFS (shortest
path by edge count), DFS (with pre/post visit order), Dijkstra (shortest
path by weight, binary-heap priority queue), and Kahn's algorithm for
topological sort (with cycle detection).

## Files

- `graph.hpp` — `Graph` (adjacency list, `add_edge`), `bfs`, `dfs`,
  `dijkstra`, `topological_sort`
- `main.cpp` — builds a small weighted DAG and a separate cyclic graph,
  runs all four algorithms, and checks the results against known-correct
  answers

## How to run

```bash
make
./graph_demo
```

## Notes

`topological_sort` returns `std::nullopt` on a cyclic graph instead of a
partial/wrong ordering — `main.cpp` exercises both the DAG case (valid
order) and a graph with a manually-introduced cycle (correctly detected).
