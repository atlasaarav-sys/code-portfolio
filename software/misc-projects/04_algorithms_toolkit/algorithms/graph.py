"""Graph algorithms on a simple adjacency-list graph."""

import heapq
from collections import deque, defaultdict


class Graph:
    def __init__(self):
        self.adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)

    def add_edge(self, u, v, weight=1.0, directed=False):
        self.adjacency[u].append((v, weight))
        self.adjacency.setdefault(v, [])
        if not directed:
            self.adjacency[v].append((u, weight))


def bfs(graph: Graph, start) -> list:
    """O(V + E) time. Returns nodes in breadth-first visit order."""
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor, _ in graph.adjacency[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: Graph, start) -> list:
    """O(V + E) time. Returns nodes in depth-first (pre-order) visit order."""
    visited = set()
    order = []

    def visit(node):
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        for neighbor, _ in graph.adjacency[node]:
            visit(neighbor)

    visit(start)
    return order


def dijkstra(graph: Graph, start) -> dict:
    """O((V + E) log V) time with a binary heap. Returns shortest
    distances from start to every reachable node."""
    distances = {start: 0.0}
    heap = [(0.0, start)]

    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances.get(node, float("inf")):
            continue  # stale heap entry, a shorter path was already found

        for neighbor, weight in graph.adjacency[node]:
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances
