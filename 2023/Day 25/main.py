from collections import defaultdict, deque
import sys

INF = 100000
CUT_SIZE = 3

# BFS
def find_augmenting_path(
    adj_list: dict[str, list[str]],
    capacities: dict[str, dict[str, int]],
    source: str,
    sink: str,
) -> tuple[int, dict[str, str]]:
    parents: dict[str, str] = {}
    parents[source] = source
    queue: deque[tuple[str, int]] = deque([(source, INF)])
    while queue:
        u, flow = queue.popleft()
        for v in adj_list[u]:
            if v not in parents and capacities[u][v] > 0:
                parents[v] = u
                new_flow = min(flow, capacities[u][v])
                if v == sink:
                    return new_flow, parents
                queue.append((v, new_flow))
    return 0, parents

# Find max flow using Edmonds-Karp. Then on the last iteration when there are no more
# augmenting paths, partition the vertices into those reachable from the source and those
# reachable from the sink in the residual graph.
def find_min_cut(
    adj_list: dict[str, list[str]], source: str, sink: str
) -> tuple[int, tuple[set[str], set[str]]]:
    capacities: dict[str, dict[str, int]] = {u: {v: 1 for v in vs} for u, vs in adj_list.items()}
    total_flow = 0
    while True:
        flow, node_parents = find_augmenting_path(adj_list, capacities, source, sink)
        if flow == 0:
            source_cut = set(node_parents)
            sink_cut = set(adj_list) - source_cut
            return total_flow, (source_cut, sink_cut)

        total_flow += flow
        curr = sink
        while curr != source:
            prev = node_parents[curr]
            capacities[prev][curr] -= flow
            capacities[curr][prev] += flow
            curr = prev

# Find a min cut with a given size in a graph.
# Do this by arbitrarily picking a source and trying every other vertex as sinks,
# then run max flow on each pair until a min cut with the correct size is found.
def find_min_cut_with_size(adj_list: dict[str, list[str]], cut_size: int) -> tuple[set[str], set[str]]:
    source = next(iter(adj_list))
    for sink in adj_list:
        if sink == source:
            continue
        max_flow, cut = find_min_cut(adj_list, source, sink)
        if max_flow == cut_size:
            return cut
    raise RuntimeError(f'Cut of size {cut_size} not found.')


adj_list: dict[str, list[str]] = defaultdict(list)
for line in sys.stdin:
    u, vs = line.split(': ')
    vs_list = vs.split()
    for v in vs_list:
        adj_list[u].append(v)
        adj_list[v].append(u)

source_cut, sink_cut = find_min_cut_with_size(adj_list, 3)
print(len(source_cut) * len(sink_cut))
