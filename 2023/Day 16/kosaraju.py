# Lengthy solution to solve part 2 without having to do a separate DFS for each starting state.
# Runs about 3 times faster than the main solution in CPython (~0.7s vs ~2.3s). In PyPy there is less of a
# difference, both run in about 0.7-0.8s.

# The idea is to construct a condensation graph of the original state graph, i.e. a directed acyclic
# graph of the strongly connected components (SCCs) in the original graph. Then we can use DP on this new
# graph to precompute the number of cells that would be energised starting from any state in each component.
# The key idea is that given a starting state, all states in the same SCC and the SCCs reachable from that
# first SCC will be reachable.
from enum import Enum
from itertools import product
import sys
from typing import NamedTuple

sys.setrecursionlimit(15000)

class Dir(Enum):
    U = (-1, 0)
    R = (0, 1)
    D = (1, 0)
    L = (0, -1)

class State(NamedTuple):
    r: int
    c: int
    d: Dir

VERTICAL_DIRS = (Dir.U, Dir.D)
HORIZONTAL_DIRS = (Dir.R, Dir.L)

def move(r: int, c: int, d: Dir) -> State:
    dr, dc = d.value
    return State(r + dr, c + dc, d)

def reflect_front_slash(d: Dir) -> Dir:
    return {
        Dir.U: Dir.R,
        Dir.R: Dir.U,
        Dir.D: Dir.L,
        Dir.L: Dir.D,
    }[d]

def reflect_back_slash(d: Dir) -> Dir:
    return {
        Dir.U: Dir.L,
        Dir.R: Dir.D,
        Dir.D: Dir.R,
        Dir.L: Dir.U,
    }[d]

def transitions(grid: list[str], state: State) -> list[State]:
    r, c, d = state
    match grid[r][c]:
        case '/':
            next_states = [move(r, c, reflect_front_slash(d))]
        case '\\':
            next_states = [move(r, c, reflect_back_slash(d))]
        case '|' if d in HORIZONTAL_DIRS:
            next_states = [move(r, c, d2) for d2 in VERTICAL_DIRS]
        case '-' if d in VERTICAL_DIRS:
            next_states = [move(r, c, d2) for d2 in HORIZONTAL_DIRS]
        case _:
            next_states = [move(r, c, d)]
    return [
        next_state for next_state in next_states
        if 0 <= next_state.r < len(grid) and 0 <= next_state.c < len(grid[0])
    ]

# Convert grid to a directed graph of states
def construct_state_graph(grid: list[str]) -> dict[State, list[State]]:
    N = len(grid)
    adj_list: dict[State, list[State]] = {}
    for state in map(State._make, product(range(N), range(N), Dir)):
        adj_list[state] = transitions(grid, state)
    return adj_list

def reversed_state_graph(adj_list: dict[State, list[State]]) -> dict[State, list[State]]:
    rev_adj_list: dict[State, list[State]] = {state: [] for state in adj_list}
    for state, adjs in adj_list.items():
        for adj in adjs:
            rev_adj_list[adj].append(state)
    return rev_adj_list

def reversed_comp_graph(adj_list: list[list[int]]) -> list[list[int]]:
    rev_adj_list: list[list[int]] = [[] for _ in adj_list]
    for state, adjs in enumerate(adj_list):
        for adj in adjs:
            rev_adj_list[adj].append(state)
    return rev_adj_list

def postorder_dfs(
    adj_list: dict[State, list[State]],
    states_seen: set[State],
    start_state: State,
    order: list[State] | None = None
) -> list[State]:
    if order is None:
        order = []
    states_seen.add(start_state)
    for next_state in adj_list[start_state]:
        if next_state not in states_seen:
            postorder_dfs(adj_list, states_seen, next_state, order)
    order.append(start_state)
    return order

def bfs(
    adj_list: dict[State, list[State]], states_seen: set[State], start_state: State
) -> list[State]:
    states_seen.add(start_state)
    component = [start_state]
    for state in component:
        for next_state in adj_list[state]:
            if next_state not in states_seen:
                states_seen.add(next_state)
                component.append(next_state)
    return component

# Condense the state graph into a directed acyclic graph of the strongly connected
# components using Kosaraju's algorithm. Returns the adjacency list of the condensed
# graph and the mapping from states to component ids.
def condense_graph(adj_list: dict[State, list[State]]) -> tuple[list[list[int]], dict[State, int]]:
    states_seen: set[State] = set()
    state_order: list[State] = []
    for state in adj_list:
        if state not in states_seen:
            state_order.extend(postorder_dfs(adj_list, states_seen, state))
    state_order.reverse()

    states_seen.clear()
    rev_adj_list = reversed_state_graph(adj_list)
    component_ids: dict[State, int] = {}
    component_count = 0
    for state in state_order:
        if state in states_seen:
            continue
        component = bfs(rev_adj_list, states_seen, state)
        component_id = component_count
        component_count += 1
        for comp_state in component:
            component_ids[comp_state] = component_id

    comp_adj_list: list[set[int]] = [set() for _ in component_ids]
    for state, adjs in adj_list.items():
        comp_id1 = component_ids[state]
        for adj in adjs:
            comp_id2 = component_ids[adj]
            if comp_id1 != comp_id2:
                comp_adj_list[comp_id1].add(comp_id2)

    return [list(adj_set) for adj_set in comp_adj_list], component_ids

# Use DP on the condensed graph to count the number of cells that would be energised
# starting from a state in each component
def count_cells_energised(
    rev_comp_adj_list: list[list[int]],
    component_ids: dict[State, int]
) -> list[int]:
    num_components = len(rev_comp_adj_list)
    indegrees = [0] * num_components
    for vs in rev_comp_adj_list:
        for v in vs:
            indegrees[v] += 1
    comp_cell_sets: list[set[tuple[int, int]]] = [set() for _ in range(num_components)]
    for state, comp_id in component_ids.items():
        comp_cell_sets[comp_id].add((state.r, state.c))

    comp_energised_sets: list[set[tuple[int, int]] | None] = [None] * num_components
    comp_energised_counts = [0] * num_components
    stack = [v for v, indegree in enumerate(indegrees) if indegree == 0]
    while stack:
        u = stack.pop()
        energised_set = comp_energised_sets[u]
        # Much finagling to minimise copying of set contents, especially those of big sets
        if energised_set is None:
            energised_set = comp_cell_sets[u]
        else:
            energised_set |= comp_cell_sets[u]
        comp_energised_counts[u] = len(energised_set)

        copy_needed = False
        for v in rev_comp_adj_list[u]:
            if comp_energised_sets[v] is None:
                comp_energised_sets[v] = energised_set.copy() if copy_needed else energised_set
                copy_needed = True
            else:
                comp_energised_sets[v] |= energised_set
            indegrees[v] -= 1
            if indegrees[v] == 0:
                stack.append(v)
        # Delete references to sets after use to help limit memory consumption and improve performance
        comp_energised_sets[u] = None
    return comp_energised_counts


grid = [line.strip() for line in sys.stdin]
N = len(grid)
adj_list = construct_state_graph(grid)
comp_adj_list, component_ids = condense_graph(adj_list)
rev_comp_adj_list = reversed_comp_graph(comp_adj_list)
comp_energised_counts = count_cells_energised(rev_comp_adj_list, component_ids)

# Part 1
print(comp_energised_counts[component_ids[State(0, 0, Dir.R)]])

# Part 2
print(max(max(
    comp_energised_counts[component_ids[state]]
    for state in (
        State(N - 1, i, Dir.U),
        State(i, 0, Dir.R),
        State(0, i, Dir.D),
        State(i, N - 1, Dir.L)
    )
) for i in range(N)))
