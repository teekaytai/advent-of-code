# This solution improves on the main solution by using an admissible heuristic to inform an A* search.
# The heuristic based on taxicab distance to the goal decreases the time taken only by a small amount.
# The heuristic using actual distance measured using Dijkstra's algorithm is much more effective,
# cutting the time taken by about 50% for part 1 and about 40% for part 2 (that includes the time taken
# to perform the initial Dijkstra's too, which actually is fairly negligible compared to the actual search)
import heapq
import sys
from typing import Callable, Iterator, Literal, NamedTuple

class State(NamedTuple):
    row: int
    col: int
    dr: Literal[-1, 0, 1]
    dc: Literal[-1, 0, 1]
    consecutive: int

    def is_in_bounds(self, grid: list[list[int]]) -> bool:
        return 0 <= self.row < len(grid) and 0 <= self.col < len(grid[0])

    def move_straight(self) -> 'State':
        return State(self.row + self.dr, self.col + self.dc, self.dr, self.dc, self.consecutive + 1)

    def turn_cw(self) -> 'State':
        return State(self.row + self.dc, self.col - self.dr, self.dc, -self.dr, 1)

    def turn_ccw(self) -> 'State':
        return State(self.row - self.dc, self.col + self.dr, -self.dc, self.dr, 1)

    def transitions_part1(self, grid: list[list[int]]) -> Iterator['State']:
        next_states: list[State] = []
        if self.consecutive < 3:
            next_states.append(self.move_straight())
        next_states.append(self.turn_cw())
        next_states.append(self.turn_ccw())
        for next_state in next_states:
            if next_state.is_in_bounds(grid):
                yield next_state

    def transitions_part2(self, grid: list[list[int]]) -> Iterator['State']:
        next_states: list[State] = []
        if self.consecutive < 10:
            next_states.append(self.move_straight())
        if self.consecutive >= 4:
            next_states.append(self.turn_cw())
            next_states.append(self.turn_ccw())
        for next_state in next_states:
            if next_state.is_in_bounds(grid):
                yield next_state

    def is_end_state_part1(self, grid: list[list[int]]) -> bool:
        return self.row == len(grid) - 1 and self.col == len(grid[-1]) - 1

    def is_end_state_part2(self, grid: list[list[int]]) -> bool:
        return self.is_end_state_part1(grid) and self.consecutive >= 4

class PQNode(NamedTuple):
    f_score: int
    g_score: int
    state: State

# Using this heuristic would effectively result in a plain dijkstra search
def make_empty_heuristic(grid: list[list[int]]) -> Callable[[State], int]:
    return lambda state: 0

def make_taxicab_heuristic(grid: list[list[int]]) -> Callable[[State], int]:
    def h(state: State) -> int:
        return (len(grid) - 1 - state.row) + (len(grid[-1]) - 1 - state.col)
    return h

# Run dijkstra's once from the end cell to precompute the distance from every other cell
# to the end cell. Constraints like when the crucible can/can't turn are ignored
def make_true_dist_heuristic(grid: list[list[int]]) -> Callable[[State], int]:
    H = len(grid)
    W = len(grid[0])
    INF = 100000000
    DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))

    dists = [[INF] * W for _ in range(H)]
    dists[-1][-1] = 0
    pq: list[tuple[int, int, int]] = [(0, H - 1, W - 1)]
    while pq:
        dist, r, c = heapq.heappop(pq)
        new_dist = dist + grid[r][c]
        for dr, dc in DIRS:
            r2 = r + dr
            c2 = c + dc
            if r2 < 0 or r2 >= H or c2 < 0 or c2 >= W:
                continue
            if new_dist < dists[r2][c2]:
                dists[r2][c2] = new_dist
                heapq.heappush(pq, (new_dist, r2, c2))

    return lambda state: dists[state.row][state.col]


grid = [[int(x) for x in line.strip()] for line in sys.stdin]

# Choose heuristic function here
h = make_true_dist_heuristic(grid)

start_states = [
    State(row=0, col=0, dr=0, dc=1, consecutive=0),
    State(row=0, col=0, dr=1, dc=0, consecutive=0),
]
pq = [
    PQNode(f_score=h(start_state), g_score=0, state=start_state)
    for start_state in start_states
]
visited: set[State] = set()
states_examined = 0
while pq:
    f_score, g_score, state = heapq.heappop(pq)
    if state in visited:
        continue
    states_examined += 1
    # if state.is_end_state_part1(grid):
    if state.is_end_state_part2(grid):
        print('Heat loss:', g_score)
        print('States examined:', states_examined)
        break
    visited.add(state)
    # for adj_state in state.transitions_part1(grid):
    for adj_state in state.transitions_part2(grid):
        if adj_state not in visited:
            new_g_score = g_score + grid[adj_state.row][adj_state.col]
            new_pq_node = PQNode(new_g_score + h(adj_state), new_g_score, adj_state)
            heapq.heappush(pq, new_pq_node)
