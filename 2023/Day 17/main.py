import heapq
import sys
from typing import Iterator, Literal, NamedTuple

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
    heat_loss: int
    state: State


grid = [[int(x) for x in line.strip()] for line in sys.stdin]
pq = [
    PQNode(heat_loss=0, state=State(row=0, col=0, dr=0, dc=1, consecutive=0)),
    PQNode(heat_loss=0, state=State(row=0, col=0, dr=1, dc=0, consecutive=0))
]
visited: set[State] = set()
while pq:
    heat_loss, state = heapq.heappop(pq)
    if state in visited:
        continue
    # if state.is_end_state_part1(grid):
    if state.is_end_state_part2(grid):
        print(heat_loss)
        break
    visited.add(state)
    # for adj_state in state.transitions_part1(grid):
    for adj_state in state.transitions_part2(grid):
        if adj_state not in visited:
            heapq.heappush(pq, PQNode(heat_loss + grid[adj_state.row][adj_state.col], adj_state))
