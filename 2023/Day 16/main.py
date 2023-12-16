from enum import Enum
import sys

class Dir(Enum):
    U = (-1, 0)
    R = (0, 1)
    D = (1, 0)
    L = (0, -1)

VERTICAL_DIRS = (Dir.U, Dir.D)
HORIZONTAL_DIRS = (Dir.R, Dir.L)

def move(r: int, c: int, d: Dir) -> tuple[int, int, Dir]:
    dr, dc = d.value
    return r + dr, c + dc, d

def reflect_front_slash(d: Dir) -> Dir:
    return {
        Dir.U: Dir.R,
        Dir.R: Dir.U,
        Dir.D: Dir.L,
        Dir.L: Dir.D
    }[d]

def reflect_back_slash(d: Dir) -> Dir:
    return {
        Dir.U: Dir.L,
        Dir.R: Dir.D,
        Dir.D: Dir.R,
        Dir.L: Dir.U
    }[d]


grid = [line.strip() for line in sys.stdin]
N = len(grid)

def find_num_energized(start_row: int, start_col: int, start_dir: Dir) -> int:
    start_state = (start_row, start_col, start_dir)
    is_energized = [[False] * N for _ in range(N)]
    is_energized[start_row][start_col] = True
    seen = {start_state}
    stack = [start_state]
    while stack:
        r, c, d = stack.pop()
        next_states: list[tuple[int, int, int]]
        cell = grid[r][c]
        if cell == '/':
            next_states = [move(r, c, reflect_front_slash(d))]
        elif cell == '\\':
            next_states = [move(r, c, reflect_back_slash(d))]
        elif cell == '|' and d in HORIZONTAL_DIRS:
            next_states = [move(r, c, d2) for d2 in VERTICAL_DIRS]
        elif cell == '-' and d in VERTICAL_DIRS:
            next_states = [move(r, c, d2) for d2 in HORIZONTAL_DIRS]
        else:
            next_states = [move(r, c, d)]
        for next_state in next_states:
            r2, c2, _ = next_state
            if r2 < 0 or r2 >= N or c2 < 0 or c2 >= N or next_state in seen:
                continue
            is_energized[r2][c2] = True
            seen.add(next_state)
            stack.append(next_state)
    return sum(sum(row) for row in is_energized)

# Part 1
print(find_num_energized(0, 0, Dir.R))

# Part 2
print(max(max(
    find_num_energized(N - 1, i, Dir.U),
    find_num_energized(i, 0, Dir.R),
    find_num_energized(0, i, Dir.D),
    find_num_energized(i, N - 1, Dir.L)
) for i in range(N)))