#include <cassert>
#include <cstdio>

#include "graph.hpp"

void print_path(const std::vector<int> &path) {
    for (size_t i = 0; i < path.size(); i++) {
        std::printf("%d%s", path[i], (i + 1 < path.size()) ? " -> " : "\n");
    }
}

int main() {
    // A small weighted DAG:
    //   0 -> 1 (4), 0 -> 2 (1)
    //   2 -> 1 (1), 1 -> 3 (1)
    //   2 -> 3 (5)
    Graph dag;
    dag.add_edge(0, 1, 4.0);
    dag.add_edge(0, 2, 1.0);
    dag.add_edge(2, 1, 1.0);
    dag.add_edge(1, 3, 1.0);
    dag.add_edge(2, 3, 5.0);

    std::printf("BFS path 0 -> 3 (fewest edges): ");
    print_path(bfs(dag, 0, 3));

    std::printf("DFS order from 0: ");
    print_path(dfs(dag, 0));

    auto dist = dijkstra(dag, 0);
    std::printf("Dijkstra distances from 0: 1=%.0f 2=%.0f 3=%.0f\n", dist[1], dist[2], dist[3]);
    assert(dist[2] == 1.0);
    assert(dist[1] == 2.0);  // via 0->2->1 (1+1) beats direct 0->1 (4)
    assert(dist[3] == 3.0);  // via 0->2->1->3 (1+1+1)

    auto topo = topological_sort(dag);
    assert(topo.has_value());
    std::printf("Topological order: ");
    print_path(*topo);

    // Introduce a cycle: 3 -> 0
    Graph cyclic = dag;
    cyclic.add_edge(3, 0);
    auto topo_cyclic = topological_sort(cyclic);
    assert(!topo_cyclic.has_value());
    std::printf("Cyclic graph correctly detected: topological_sort returned nullopt\n");

    std::printf("\nAll assertions passed.\n");
    return 0;
}
