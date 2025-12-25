use std::io::{self, Read};

const SHAPE_DIM: usize = 3;
const FILLED_CELL: u8 = b'#';

fn rotate_grid<T: Copy>(grid: &[Vec<T>]) -> Vec<Vec<T>> {
    let n = grid.len();
    Vec::from_iter((0..n).map(|i| Vec::from_iter((0..n).map(|j| grid[j][n - 1 - i]))))
}

struct Shape {
    area: u32,
    masks: Vec<[u64; SHAPE_DIM]>,
}

impl Shape {
    fn parse(input: &str) -> Self {
        let area = input
            .as_bytes()
            .iter()
            .filter(|&&b| b == FILLED_CELL)
            .count() as u32;
        let mut grid: Vec<_> = input
            .lines()
            .skip(1)
            .map(|row| row.as_bytes().to_vec())
            .collect();
        let mut masks = Vec::new();
        for _ in 0..4 {
            let mut mask1 = [0; SHAPE_DIM];
            let mut mask2 = [0; SHAPE_DIM];
            for (i, row) in grid.iter().enumerate() {
                mask1[i] = row
                    .iter()
                    .fold(0, |acc, &cell| (acc << 1) | u64::from(cell == FILLED_CELL));
                mask2[i] = row
                    .iter()
                    .rfold(0, |acc, &cell| (acc << 1) | u64::from(cell == FILLED_CELL));
            }
            masks.push(mask1);
            masks.push(mask2);
            grid = rotate_grid(&grid);
        }
        masks.sort_unstable();
        masks.dedup();
        Shape { area, masks }
    }
}

struct Query {
    width: usize,
    height: usize,
    shape_counts: Vec<u32>,
}

impl Query {
    fn parse(input: &str) -> Option<Self> {
        let mut iter = input.split_ascii_whitespace();
        let (width, height) = iter.next()?.strip_suffix(':')?.split_once('x')?;
        let shape_counts: Vec<_> = iter.map(|x| x.parse().unwrap()).collect();
        Some(Query {
            width: width.parse().ok()?,
            height: height.parse().ok()?,
            shape_counts,
        })
    }
}

fn can_fit(shapes: &[Shape], query: &Query) -> bool {
    fn helper(
        shapes: &[Shape],
        width: usize,
        height: usize,
        shape_counts: &mut [u32],
        grid: &mut [u64],
        start_row: usize,
        start_col: usize,
    ) -> bool {
        if shape_counts.iter().all(|&count| count == 0) {
            return true;
        }
        for r in start_row..height - SHAPE_DIM + 1 {
            let start_c = if r == start_row { start_col } else { 0 };
            for c in start_c..width - SHAPE_DIM + 1 {
                for (i, shape) in shapes.iter().enumerate() {
                    if shape_counts[i] == 0 {
                        continue;
                    }
                    shape_counts[i] -= 1;
                    for shape_mask in &shape.masks {
                        let shape_blocked = grid[r..r + SHAPE_DIM]
                            .iter()
                            .zip(shape_mask)
                            .any(|(&row_mask, m)| row_mask & (m << c) != 0);
                        if shape_blocked {
                            continue;
                        }
                        for (row_mask, m) in grid[r..r + SHAPE_DIM].iter_mut().zip(shape_mask) {
                            *row_mask |= m << c;
                        }
                        if helper(shapes, width, height, shape_counts, grid, r, c + 1) {
                            return true;
                        }
                        for (row_mask, m) in grid[r..r + SHAPE_DIM].iter_mut().zip(shape_mask) {
                            *row_mask ^= m << c;
                        }
                    }
                    shape_counts[i] += 1;
                }
            }
        }
        false
    }
    helper(
        shapes,
        query.width,
        query.height,
        &mut query.shape_counts.clone(),
        &mut vec![0; query.height],
        0,
        0,
    )
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut input = String::new();
    stdin.lock().read_to_string(&mut input)?;
    let mut input_parts: Vec<_> = input.split("\n\n").collect();
    let queries = input_parts.pop().unwrap();
    let shapes: Vec<_> = input_parts.into_iter().map(Shape::parse).collect();

    let mut ans = 0;
    for query in queries.lines().map(Query::parse) {
        let query = query.unwrap();
        let total_shape_area = query
            .shape_counts
            .iter()
            .zip(&shapes)
            .fold(0, |acc, (&count, shape)| acc + count * shape.area);
        if ((query.width * query.height) as u32) < total_shape_area {
            continue;
        }
        let total_shapes = query.shape_counts.iter().sum();
        if ((query.width / SHAPE_DIM) * (query.height / SHAPE_DIM)) as u32 >= total_shapes {
            ans += 1;
            continue;
        }
        ans += u32::from(can_fit(&shapes, &query));
    }

    println!("{}", ans);
    Ok(())
}
