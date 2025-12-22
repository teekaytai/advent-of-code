use itertools::Itertools;
use std::{
    collections::HashMap,
    io::{self, BufRead},
};

struct Tile {
    x: u32,
    y: u32,
}

impl Tile {
    fn parse(line: &str) -> Self {
        let (x, y) = line.split_once(',').unwrap();
        Tile {
            x: x.parse().unwrap(),
            y: y.parse().unwrap(),
        }
    }
}

fn compress_coordinates(it: impl Iterator<Item = u32>) -> HashMap<u32, usize> {
    let mut coords: Vec<_> = it.collect();
    coords.sort_unstable();
    coords.dedup();
    let mut coords_to_index = HashMap::with_capacity(coords.len());
    for (idx, x) in coords.into_iter().enumerate() {
        // Double indices to handle empty space between otherwise adjacent tiles.
        // This is necessary to tell when regions are not completely filled for edge cases such as:
        // #XX#
        // ##.X
        // ##.X
        // #XX#
        coords_to_index.insert(x, 2 * idx);
    }
    coords_to_index
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let corners: Vec<_> = stdin
        .lock()
        .lines()
        .map(|line| line.map(|l| Tile::parse(&l)))
        .collect::<io::Result<_>>()?;
    let x_to_idx = compress_coordinates(corners.iter().map(|corner| corner.x));
    let y_to_idx = compress_coordinates(corners.iter().map(|corner| corner.y));
    let nx = x_to_idx.len();
    let ny = y_to_idx.len();

    // Create a grid that marks all tiles inside the loop.
    // The grid is doubled to preserve gaps between adjacent coordinates, so each tile maps to a 2×2 block.
    // Boundary tiles partially fill their 2x2 blocks, allowing us to accuratlely detect gaps.
    // For example, if one row of the loop's area spans x-coordinates 1-2 and 3-5 (after
    // coordinate compression but before doubling), the row in the grid looks like:
    // [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    //  <-0-> <-1-> <-2-> <-3-> <-4-> <-5-> <-6->
    // Note the gap formed between 2 and 3 to show the area does not fully span 1-5.
    let mut inside_loop = vec![vec![0; 2 * nx]; 2 * ny];
    for (corner1, corner2) in corners.iter().zip(corners.iter().cycle().skip(1)) {
        if corner1.y != corner2.y {
            // Skip vertical edges
            continue;
        }
        let yi = y_to_idx[&corner1.y];
        let xi1 = x_to_idx[&corner1.x];
        let xi2 = x_to_idx[&corner2.x];
        // Mark points where we move into/out of the loop
        inside_loop[yi + 1][xi1 + 1] = 1;
        inside_loop[yi + 1][xi2 + 1] = 1;
    }
    for yi in 1..2 * ny {
        for xi in 1..2 * nx {
            inside_loop[yi][xi] ^=
                inside_loop[yi][xi - 1] ^ inside_loop[yi - 1][xi] ^ inside_loop[yi - 1][xi - 1];
        }
    }

    let mut area_prefix_sums = inside_loop;
    for yi in 1..2 * ny {
        for xi in 1..2 * nx {
            area_prefix_sums[yi][xi] += area_prefix_sums[yi][xi - 1] + area_prefix_sums[yi - 1][xi]
                - area_prefix_sums[yi - 1][xi - 1];
        }
    }

    let mut ans1 = 0;
    let mut ans2 = 0;
    for (corner1, corner2) in corners.iter().tuple_combinations() {
        let (mut x1, mut x2) = (corner1.x, corner2.x);
        let (mut y1, mut y2) = (corner1.y, corner2.y);
        if x1 > x2 {
            std::mem::swap(&mut x1, &mut x2);
        }
        if y1 > y2 {
            std::mem::swap(&mut y1, &mut y2);
        }
        let rect_area = u64::from(x2 - x1 + 1) * u64::from(y2 - y1 + 1);
        ans1 = ans1.max(rect_area);
        let xi1 = x_to_idx[&x1];
        let xi2 = x_to_idx[&x2];
        let yi1 = y_to_idx[&y1];
        let yi2 = y_to_idx[&y2];
        let compressed_area = (xi2 - xi1) * (yi2 - yi1);
        let area_intersecting_loop = area_prefix_sums[yi2][xi2] + area_prefix_sums[yi1][xi1]
            - area_prefix_sums[yi2][xi1]
            - area_prefix_sums[yi1][xi2];
        if area_intersecting_loop == compressed_area {
            ans2 = ans2.max(rect_area);
        }
    }

    println!("{}\n{}", ans1, ans2);
    Ok(())
}
