use std::io::{self, BufRead};

fn main() {
    let mut ans1 = 0;
    let mut intervals = Vec::new();
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        match line.split_once('-') {
            Some((lo, hi)) => {
                intervals.push((lo.parse::<u64>().unwrap(), hi.parse::<u64>().unwrap()));
            }
            None => {
                let x = line.parse::<u64>().unwrap();
                ans1 += u32::from(intervals.iter().any(|&(lo, hi)| lo <= x && x <= hi));
            }
        }
    }

    let mut ans2 = 0;
    intervals.sort_unstable();
    let mut last_hi = 0;
    for (lo, hi) in intervals {
        let new_lo = lo.max(last_hi + 1);
        ans2 += if hi >= new_lo { hi - new_lo + 1 } else { 0 };
        last_hi = last_hi.max(hi);
    }

    println!("{}\n{}", ans1, ans2);
}
