from collections import defaultdict
import heapq
import sys

INF = 100000
NEG_INF = -100000
CUT_SIZE = 3

# Find the global min cut in a graph using the Stoer-Wagner algorithm.
# If provided, the algorithm terminates early when a cut with the provided size or smaller is found.
# This version uses an adjacency list and a priority queue to achieve O(VElog(V)) time complexity.
def global_min_cut(adj_list: dict[str, list[str]], target_cut_size: int = 0) -> tuple[set[str], set[str]]:
    n = len(adj_list)
    weighted_adj_list: dict[str, dict[str, int]] = {u: {v: 1 for v in vs} for u, vs in adj_list.items()}
    combined_nodes = {v: [v] for v in adj_list}
    start = next(iter(adj_list))
    min_cut_size = INF
    min_cut: list[str] = []
    for i in range(1, n):
        frontier_weights = {v: 0 for v in weighted_adj_list}
        pq: list[tuple[int, str]] = []
        for v, w in weighted_adj_list[start].items():
            frontier_weights[v] = w
            pq.append((-w, v))
        heapq.heapify(pq)
        prev = start
        curr = start
        for _ in range(n - i):
            frontier_weights[curr] = NEG_INF
            prev = curr
            curr = heapq.heappop(pq)[1]
            while frontier_weights[curr] < 0:
                curr = heapq.heappop(pq)[1]
            for nxt, w in weighted_adj_list[curr].items():
                if frontier_weights[nxt] >= 0:
                    frontier_weights[nxt] += w
                    heapq.heappush(pq, (-frontier_weights[nxt], nxt))

        if frontier_weights[curr] < min_cut_size:
            min_cut_size = frontier_weights[curr]
            min_cut = combined_nodes[curr]
            if min_cut_size <= target_cut_size:
                break

        # Merge last 2 nodes together (curr node into prev node)
        combined_nodes[prev].extend(combined_nodes[curr])
        for v, w in weighted_adj_list.pop(curr).items():
            weighted_adj_list[v].pop(curr)
            if v == prev:
                continue
            new_w = w + weighted_adj_list[prev].get(v, 0)
            weighted_adj_list[prev][v] = new_w
            weighted_adj_list[v][prev] = new_w

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
