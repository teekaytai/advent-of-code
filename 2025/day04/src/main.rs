use std::io::{self, BufRead};

const ROLL: u8 = b'@';
const ACCESSIBLE_ROLL_LIMIT: u8 = 3;
const DIRS: [(isize, isize); 8] = [
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
];

fn neighbours(
    height: usize,
    width: usize,
    r: usize,
    c: usize,
) -> impl Iterator<Item = (usize, usize)> {
    DIRS.iter().filter_map(move |(dr, dc)| {
        let r2 = r as isize + dr;
        let c2 = c as isize + dc;
        (r2 >= 0 && r2 < height as isize && c2 >= 0 && c2 < width as isize)
            .then_some((r2 as usize, c2 as usize))
    })
}

fn main() {
    let mut grid = Vec::new();
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        grid.push(line.unwrap().into_bytes());
    }
    let height = grid.len();
    let width = grid[0].len();
    let mut num_adjacent = vec![vec![0; width]; height];
    let mut stack = Vec::new();
    for (r, row) in grid.iter().enumerate() {
        for (c, cell) in row.iter().enumerate() {
            if *cell != ROLL {
                continue;
            }
            for (r2, c2) in neighbours(height, width, r, c) {
                num_adjacent[r][c] += (grid[r2][c2] == ROLL) as u8;
            }
            if num_adjacent[r][c] <= ACCESSIBLE_ROLL_LIMIT {
                stack.push((r, c));
            }
        }
    }

    let ans1 = stack.len();
    let mut ans2 = ans1;
    while let Some((r, c)) = stack.pop() {
        for (r2, c2) in neighbours(height, width, r, c) {
            if grid[r2][c2] != ROLL {
                continue;
            }
            num_adjacent[r2][c2] -= 1;
            if num_adjacent[r2][c2] == ACCESSIBLE_ROLL_LIMIT {
                stack.push((r2, c2));
                ans2 += 1;
            }
        }
    }
    println!("{}\n{}", ans1, ans2);
}
