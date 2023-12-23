# This solution uses DP instead of plain brute force, but takes ~1.4s in pypy3 for part 2, about twice as long as the brute force solution.
# This is probably due to the large amount of memory being used to store memoised results.
import sys
from typing import NamedTuple

FOREST = '#'
SLOPES = '^>v<'
DIRS = [-1, 1j, 1, -1j]

Point = complex
Node = int
NodeSet = int  # Bitmask

class Edge(NamedTuple):
    v: Node
    weight: int

def get_neighbours(points_map: dict[Point, str], z: Point) -> list[Point]:
    adjs: list[Point] = []
    for dz in DIRS:
        adj: Point = z + dz
        cell = points_map.get(adj, None)
        if cell is not None and cell != FOREST:
            adjs.append(adj)
    return adjs

def is_upslope(points_map: dict[Point, str], curr: Point, adj: Point) -> bool:
    cell = points_map[adj]
    return cell in SLOPES and adj + DIRS[SLOPES.index(cell)] == curr

# Perform DFS and compress graph into a weighted graph in adj_list
def compress_graph(
    points_map: dict[Point, str], start: Point, end: Point, allow_upslope: bool
) -> tuple[list[list[Edge]], int, int, Node, Node]:
    adj_list: list[list[Edge]] = []
    start_steps: int  # Steps from starting point to first junction
    end_steps: int  # Steps from last junction to ending point
    start_node_id: int  # Node id for the first junction in the compressed graph
    end_node_id: int  # Node id for the last junction in the compressed graph

    node_ids: dict[Point, int] = {}
    visited: set[Point] = set()
    stack: list[tuple[Point, Point, Node, int]] = [(start, start, -1, 0)]
    while stack:
        curr, prev, last_node, dist = stack.pop()
        if curr == end:
            end_steps = dist
            end_node_id = last_node
            continue

        adjs = get_neighbours(points_map, curr)
        if len(adjs) > 2:
            # Convert junction to node in compressed graph
            v = node_ids.get(curr, None)
            if v is None:
                v = node_ids[curr] = len(node_ids)
                adj_list.append([])
            if last_node == -1:
                start_steps = dist
                start_node_id = v
            else:
                adj_list[last_node].append(Edge(v, dist))
                # Ignore slope direction for part 2
                if allow_upslope:
                    adj_list[v].append(Edge(last_node, dist))
            last_node = v
            dist = 0

        if curr not in visited:
            visited.add(curr)
            for adj in adjs:
                # Avoid going up slopes for part 1
                if not allow_upslope and is_upslope(points_map, curr, adj):
                    continue
                if adj != prev:
                    stack.append((adj, curr, last_node, dist + 1))
    return adj_list, start_steps, end_steps, start_node_id, end_node_id

# Find longest paths using DP based on current node and nodes already visited.
# DP cuts down states searched by about 60% compared to plain brute force.
def find_longest_path(adj_list: list[list[Edge]], start: Node, end: Node) -> int:
    start_node_set = 1 << start
    # Traverse using BFS order to ensure correct order of solving subproblems.
    # Subproblems depend on smaller subproblems with fewer nodes visited.
    queue: list[tuple[Node, NodeSet]] = [(start, start_node_set)]
    next_queue: list[tuple[Node, NodeSet]] = []
    longest_dists: list[dict[NodeSet, int]] = [{} for _ in range(len(adj_list))]
    longest_dists[start][start_node_set] = 0
    longest_path = 0
    while queue:
        while queue:
            # Popping as we go rather than just iterating over the queue doubles the speed, probably by keeping memory usage down
            curr, nodes_visited = queue.pop()
            # Memoised result only needed once, so pop from dict to keep memory usage down and improve performance
            dist = longest_dists[curr].pop(nodes_visited)
            if curr == end:
                longest_path = max(longest_path, dist)
                continue
            for adj, weight in adj_list[curr]:
                adj_node_bit = 1 << adj
                if nodes_visited & adj_node_bit:
                    continue
                new_nodes_visited = nodes_visited | adj_node_bit
                new_dist = dist + weight
                memo = longest_dists[adj].get(new_nodes_visited, None)
                if memo is None:
                    longest_dists[adj][new_nodes_visited] = new_dist
                    queue.append((adj, new_nodes_visited))
                else:
                    longest_dists[adj][new_nodes_visited] = max(memo, new_dist)
        queue, next_queue = next_queue, queue
    return longest_path


grid = [line.strip() for line in sys.stdin]
N = len(grid)
START: Point = 1j
END: Point = N-1 + (N-2)*1j
points_map = {r + c*1j: cell for r, row in enumerate(grid) for c, cell in enumerate(row)}

# Allow upslope for part 2, disallow for part 1
allow_upslope = True

adj_list, start_steps, end_steps, start_node_id, end_node_id = compress_graph(
    points_map, START, END, allow_upslope
)
print(start_steps + find_longest_path(adj_list, start_node_id, end_node_id) + end_steps)
