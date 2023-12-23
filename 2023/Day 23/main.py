# Program finishes part 2 in ~0.7s in pypy3
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

# Find longest paths using brute force
def find_longest_path(adj_list: list[list[Edge]], start: Node, end: Node) -> int:
    start_node_set = 1 << start
    stack: list[tuple[Node, NodeSet, int]] = [(start, start_node_set, 0)]
    longest_path = 0
    while stack:
        curr, nodes_visited, dist = stack.pop()
        if curr == end:
            longest_path = max(longest_path, dist)
            continue
        for adj, weight in adj_list[curr]:
            adj_node_bit = 1 << adj
            if nodes_visited & adj_node_bit:
                continue
            stack.append((adj, nodes_visited | adj_node_bit, dist + weight))
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
