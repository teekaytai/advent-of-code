use std::io::{self, BufRead};

const START_DIAL_POS: i32 = 50;
const DIAL_SIZE: i32 = 100;

fn main() {
    let mut ans1 = 0;
    let mut ans2 = 0;
    let mut dial_pos = START_DIAL_POS;
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        let rotation_dir = if line.starts_with('R') { 1 } else { -1 };
        let rotation_amt = line[1..].parse::<i32>().unwrap();
        let new_dial_pos = (dial_pos + rotation_dir * rotation_amt).rem_euclid(DIAL_SIZE);
        if new_dial_pos == 0 {
            ans1 += 1;
        }
        ans2 += rotation_amt / DIAL_SIZE;
        if dial_pos != 0 && (new_dial_pos == 0 || (rotation_dir == 1) ^ (new_dial_pos > dial_pos)) {
            ans2 += 1;
        }
        dial_pos = new_dial_pos;
    }
    println!("{}\n{}", ans1, ans2);
}
