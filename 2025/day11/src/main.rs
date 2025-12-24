use std::{
    collections::HashMap,
    io::{self, BufRead},
};

const PART1_START: &str = "you";
const PART2_START: &str = "svr";
const PART2_MIDDLE_NODES: [&str; 2] = ["dac", "fft"];
const END: &str = "out";

#[derive(Default)]
struct DpNode {
    part1_paths: u32,
    part2_paths: [u64; 3], // Number of paths from start passing through 0, 1, or 2 of the middle nodes
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut adj_list: HashMap<_, Vec<_>> = HashMap::new();
    let mut indegrees: HashMap<_, usize> = HashMap::new();
    for line in stdin.lock().lines() {
        let line = line?;
        let mut nodes = line.split_ascii_whitespace();
        let u = nodes.next().unwrap().strip_suffix(':').unwrap().to_owned();
        let vs: Vec<_> = nodes.map(str::to_owned).collect();
        for v in &vs {
            *indegrees.entry(v.to_owned()).or_default() += 1;
        }
        adj_list.insert(u, vs);
    }
    let mut dp = HashMap::new();
    dp.insert(
        PART1_START.to_owned(),
        DpNode {
            part1_paths: 1,
            part2_paths: [0, 0, 0],
        },
    );
    dp.insert(
        PART2_START.to_owned(),
        DpNode {
            part1_paths: 0,
            part2_paths: [1, 0, 0],
        },
    );
    let mut stack = Vec::new();
    for u in adj_list.keys() {
        if !indegrees.contains_key(u) {
            stack.push(u.to_owned());
        }
    }
    while let Some(u) = stack.pop() {
        let (part1_paths_u, part2_paths_u) = {
            let dp_node_u = dp.entry(u.clone()).or_default();
            let part2_paths = &mut dp_node_u.part2_paths;
            if PART2_MIDDLE_NODES.contains(&u.as_str()) {
                for i in (1..part2_paths.len()).rev() {
                    part2_paths[i] = part2_paths[i - 1];
                }
            }
            (dp_node_u.part1_paths, dp_node_u.part2_paths)
        };
        if let Some(vs) = adj_list.get(&u) {
            for v in vs {
                let dp_node_v = dp.entry(v.to_owned()).or_default();
                dp_node_v.part1_paths += part1_paths_u;
                for (paths_v, paths_u) in dp_node_v.part2_paths.iter_mut().zip(part2_paths_u) {
                    *paths_v += paths_u;
                }
                let indegree_v = indegrees.get_mut(v).unwrap();
                *indegree_v -= 1;
                if *indegree_v == 0 {
                    stack.push(v.to_owned());
                }
            }
        }
    }

    let dp_node_end = &dp[END];
    println!(
        "{}\n{}",
        dp_node_end.part1_paths,
        dp_node_end.part2_paths.last().unwrap()
    );
    Ok(())
}
