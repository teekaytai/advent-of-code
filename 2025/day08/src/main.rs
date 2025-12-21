use itertools::Itertools;
use std::{
    io::{self, BufRead},
    mem::swap,
};

struct Point {
    x: i32,
    y: i32,
    z: i32,
}

impl Point {
    fn parse(line: &str) -> Self {
        let mut it = line.split(',').map(|x| x.parse().unwrap());
        let x = it.next().unwrap();
        let y = it.next().unwrap();
        let z = it.next().unwrap();
        Point { x, y, z }
    }

    fn dist2(&self, other: &Self) -> i64 {
        let dx = i64::from(self.x - other.x);
        let dy = i64::from(self.y - other.y);
        let dz = i64::from(self.z - other.z);
        dx * dx + dy * dy + dz * dz
    }
}

struct Dsu {
    parents: Vec<usize>,
    sizes: Vec<usize>,
    num_groups: usize,
}

impl Dsu {
    fn new(n: usize) -> Self {
        Dsu {
            parents: (0..n).collect(),
            sizes: vec![1; n],
            num_groups: n,
        }
    }

    fn find(&mut self, v: usize) -> usize {
        if self.parents[v] != v {
            self.parents[v] = self.find(self.parents[v])
        };
        self.parents[v]
    }

    fn union(&mut self, u: usize, v: usize) {
        let mut root1 = self.find(u);
        let mut root2 = self.find(v);
        if root1 == root2 {
            return;
        }
        if self.sizes[root1] > self.sizes[root2] {
            swap(&mut root1, &mut root2);
        }
        self.parents[root1] = root2;
        self.sizes[root2] += self.sizes[root1];
        self.num_groups -= 1;
    }

    fn group_sizes(&self) -> Vec<usize> {
        (0..self.parents.len())
            .filter(|&v| self.parents[v] == v)
            .map(|v| self.sizes[v])
            .collect()
    }
}

const PART1_STEPS: usize = 1000; // Set to 10 for sample input

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let points: Vec<_> = stdin
        .lock()
        .lines()
        .map(|line| Ok(Point::parse(&line?)))
        .collect::<io::Result<_>>()?;
    let n = points.len();
    let mut connections: Vec<_> = points
        .iter()
        .enumerate()
        .tuple_combinations()
        .map(|((u, p), (v, q))| (p.dist2(q), u, v))
        .collect();
    connections.sort_unstable_by_key(|&(dist, _, _)| dist);
    let mut dsu = Dsu::new(n);

    let mut ans1 = 0;
    let mut ans2 = 0;
    for (step, &(_, u, v)) in connections.iter().enumerate() {
        dsu.union(u, v);
        if step + 1 == PART1_STEPS {
            let mut group_sizes = dsu.group_sizes();
            group_sizes.sort_unstable();
            ans1 = group_sizes.iter().rev().take(3).product();
        }
        if dsu.num_groups == 1 {
            ans2 = i64::from(points[u].x) * i64::from(points[v].x);
            break;
        }
    }

    println!("{}\n{}", ans1, ans2);
    Ok(())
}
