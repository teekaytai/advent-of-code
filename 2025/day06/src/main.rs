use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut grid: Vec<_> = stdin.lock().lines().collect::<Result<Vec<_>, _>>()?;
    let ops_line = grid.pop().unwrap();
    let ops = ops_line.replace(' ', "").into_bytes();

    let mut column_answers: Vec<u64> = ops.iter().map(|&o| if o == b'+' { 0 } else { 1 }).collect();
    for line in &grid {
        let nums = line
            .split_ascii_whitespace()
            .map(|x| x.parse::<u32>().unwrap());
        for ((num, &op), column_answer) in nums.zip(ops.iter()).zip(&mut column_answers) {
            if op == b'+' {
                *column_answer += num as u64;
            } else {
                *column_answer *= num as u64;
            }
        }
    }
    let ans1: u64 = column_answers.iter().sum();

    let mut ans2 = 0;
    let num_cols = grid.iter().map(String::len).max().unwrap();
    let mut vals = Vec::new();
    let mut skip_col = false;
    for c in (0..num_cols).rev() {
        if skip_col {
            skip_col = false;
            continue;
        }
        let mut val: u64 = 0;
        for line in &grid {
            match line.as_bytes().get(c) {
                None | Some(b' ') => {}
                Some(digit) => val = val * 10 + u64::from(digit - b'0'),
            };
        }
        vals.push(val);
        match ops_line.as_bytes().get(c) {
            None | Some(b' ') => {}
            Some(&op) => {
                ans2 += if op == b'+' {
                    vals.iter().sum::<u64>()
                } else {
                    vals.iter().product()
                };
                vals.clear();
                skip_col = true;
            }
        }
    }

    println!("{}\n{}", ans1, ans2);
    Ok(())
}
