from collections import defaultdict
import sys

INF = 100000
NEG_INF = -100000
CUT_SIZE = 3

# Find the global min cut in a graph using the Stoer-Wagner algorithm.
# If provided, the algorithm terminates early when a cut with the provided size or smaller is found.
# This version uses an adjacency matrix to achieve O(V^3) time complexity.
# The implementation with the adjacency list and PQ runs much faster than this one since the graph is sparse.
def global_min_cut(adj_list: dict[str, list[str]], target_cut_size: int = 0) -> tuple[set[str], set[str]]:
    n = len(adj_list)
    weights_matrix: dict[str, dict[str, int]] = {u: {v: 0 for v in adj_list} for u in adj_list}
    for u, vs in adj_list.items():
        for v in vs:
            weights_matrix[u][v] = 1
    combined_nodes = {v: [v] for v in adj_list}
    start = next(iter(adj_list))
    min_cut_size = INF
    min_cut: list[str] = []
    for i in range(1, n):
        frontier_weights = weights_matrix[start].copy()
        prev = start
        curr = start
        for _ in range(n - i):
            frontier_weights[curr] = NEG_INF
            prev = curr
            curr = max(frontier_weights, key=frontier_weights.get)
            for nxt, w in weights_matrix[curr].items():
                frontier_weights[nxt] += w

        if frontier_weights[curr] < min_cut_size:
            min_cut_size = frontier_weights[curr]
            min_cut = combined_nodes[curr]
            if min_cut_size <= target_cut_size:
                break

        # Merge last 2 nodes together (curr node into prev node)
        combined_nodes[prev].extend(combined_nodes[curr])
        for node in weights_matrix:
            weights_matrix[prev][node] += weights_matrix[curr][node]
            weights_matrix[node][prev] = weights_matrix[prev][node]
            weights_matrix[node][curr] = 0
            weights_matrix[curr][node] = 0
        weights_matrix[prev][prev] = 0

    sink_cut = set(min_cut)
    source_cut = set(adj_list) - sink_cut
    return source_cut, sink_cut


adj_list: dict[str, list[str]] = defaultdict(list)
for line in sys.stdin:
    u, vs = line.split(': ')
    vs_list = vs.split()
    for v in vs_list:
        adj_list[u].append(v)
        adj_list[v].append(u)

source_cut, sink_cut = global_min_cut(adj_list, CUT_SIZE)
print(len(source_cut) * len(sink_cut))
