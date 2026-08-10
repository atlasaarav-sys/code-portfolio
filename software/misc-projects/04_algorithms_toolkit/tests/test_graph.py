import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.graph import Graph, bfs, dfs, dijkstra


def make_test_graph():
    # Same small weighted DAG used in software/cpp/advanced/08_graph_algorithms,
    # so the "known-correct" distances are hand-verified in two languages:
    #   0 -> 1 (4), 0 -> 2 (1), 2 -> 1 (1), 1 -> 3 (1), 2 -> 3 (5)
    g = Graph()
    g.add_edge(0, 1, 4.0, directed=True)
    g.add_edge(0, 2, 1.0, directed=True)
    g.add_edge(2, 1, 1.0, directed=True)
    g.add_edge(1, 3, 1.0, directed=True)
    g.add_edge(2, 3, 5.0, directed=True)
    return g


class TestGraph(unittest.TestCase):
    def test_bfs_visits_all_reachable_nodes(self):
        g = make_test_graph()
        order = bfs(g, 0)
        self.assertEqual(set(order), {0, 1, 2, 3})
        self.assertEqual(order[0], 0)  # start node visited first

    def test_dfs_visits_all_reachable_nodes(self):
        g = make_test_graph()
        order = dfs(g, 0)
        self.assertEqual(set(order), {0, 1, 2, 3})
        self.assertEqual(order[0], 0)

    def test_dijkstra_shortest_distances(self):
        g = make_test_graph()
        distances = dijkstra(g, 0)
        self.assertEqual(distances[0], 0.0)
        self.assertEqual(distances[2], 1.0)
        self.assertEqual(distances[1], 2.0)  # via 0->2->1 (1+1), beats direct 0->1 (4)
        self.assertEqual(distances[3], 3.0)  # via 0->2->1->3 (1+1+1)

    def test_undirected_edge_goes_both_ways(self):
        g = Graph()
        g.add_edge("a", "b", 1.0)  # directed=False by default
        self.assertIn(("b", 1.0), g.adjacency["a"])
        self.assertIn(("a", 1.0), g.adjacency["b"])

    def test_unreachable_node_not_in_dijkstra_result(self):
        g = make_test_graph()
        g.adjacency.setdefault(99, [])  # isolated node, no edges
        distances = dijkstra(g, 0)
        self.assertNotIn(99, distances)


if __name__ == "__main__":
    unittest.main()
