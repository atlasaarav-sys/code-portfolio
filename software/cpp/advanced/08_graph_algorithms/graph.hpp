#pragma once

#include <algorithm>
#include <limits>
#include <optional>
#include <queue>
#include <unordered_map>
#include <vector>

class Graph {
public:
    void add_node(int id) {
        adj_.try_emplace(id);
    }

    void add_edge(int from, int to, double weight = 1.0) {
        adj_[from].push_back({to, weight});
        adj_.try_emplace(to); // ensure the destination exists even with no outgoing edges
    }

    const std::vector<std::pair<int, double>> &neighbors(int node) const {
        static const std::vector<std::pair<int, double>> empty;
        auto it = adj_.find(node);
        return it != adj_.end() ? it->second : empty;
    }

    std::vector<int> nodes() const {
        std::vector<int> result;
        for (const auto &[id, _] : adj_) result.push_back(id);
        return result;
    }

private:
    std::unordered_map<int, std::vector<std::pair<int, double>>> adj_; // node -> [(neighbor, weight)]
};

// BFS: shortest path by edge count. Returns the path from start to goal, or empty if unreachable.
inline std::vector<int> bfs(const Graph &g, int start, int goal) {
    std::unordered_map<int, int> parent;
    std::queue<int> q;
    q.push(start);
    parent[start] = start;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (u == goal) break;
        for (const auto &[v, _] : g.neighbors(u)) {
            if (!parent.count(v)) {
                parent[v] = u;
                q.push(v);
            }
        }
    }

    if (!parent.count(goal)) return {};

    std::vector<int> path;
    for (int at = goal; at != start; at = parent[at]) path.push_back(at);
    path.push_back(start);
    std::reverse(path.begin(), path.end());
    return path;
}

// DFS: pre-order visit sequence starting from `start`.
inline std::vector<int> dfs(const Graph &g, int start) {
    std::vector<int> order;
    std::unordered_map<int, bool> visited;
    std::vector<int> stack = {start};

    while (!stack.empty()) {
        int u = stack.back();
        stack.pop_back();
        if (visited[u]) continue;
        visited[u] = true;
        order.push_back(u);
        const auto &neighbors = g.neighbors(u);
        for (auto it = neighbors.rbegin(); it != neighbors.rend(); ++it) {
            if (!visited[it->first]) stack.push_back(it->first);
        }
    }
    return order;
}

// Dijkstra: shortest weighted distances from `start` to every reachable node.
inline std::unordered_map<int, double> dijkstra(const Graph &g, int start) {
    std::unordered_map<int, double> dist;
    dist[start] = 0.0;

    using QueueItem = std::pair<double, int>; // (distance, node)
    std::priority_queue<QueueItem, std::vector<QueueItem>, std::greater<>> pq;
    pq.push({0.0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (dist.count(u) && d > dist[u]) continue; // stale entry

        for (const auto &[v, weight] : g.neighbors(u)) {
            double nd = d + weight;
            if (!dist.count(v) || nd < dist[v]) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    return dist;
}

// Kahn's algorithm. Returns std::nullopt if the graph has a cycle.
inline std::optional<std::vector<int>> topological_sort(const Graph &g) {
    std::unordered_map<int, int> in_degree;
    for (int n : g.nodes()) in_degree[n] = 0;
    for (int n : g.nodes()) {
        for (const auto &[v, _] : g.neighbors(n)) in_degree[v]++;
    }

    std::queue<int> q;
    for (const auto &[n, deg] : in_degree) {
        if (deg == 0) q.push(n);
    }

    std::vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (const auto &[v, _] : g.neighbors(u)) {
            if (--in_degree[v] == 0) q.push(v);
        }
    }

    if (order.size() != in_degree.size()) return std::nullopt; // cycle detected
    return order;
}
