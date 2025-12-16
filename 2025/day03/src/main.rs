use std::io::{self, BufRead};

const PART_1_JOLTAGE_DIGITS: usize = 2;
const PART_2_JOLTAGE_DIGITS: usize = 12;

fn main() {
    let mut ans1 = 0;
    let mut ans2 = 0;
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        let digits = line.chars().map(|c| c.to_digit(10).unwrap());
        let mut num_digits_to_max_joltage = [0u64; PART_2_JOLTAGE_DIGITS + 1];
        for digit in digits {
            let digit = digit as u64;
            let mut prev_joltage = num_digits_to_max_joltage[0];
            for max_joltage in num_digits_to_max_joltage.iter_mut().skip(1) {
                let temp = (*max_joltage).max(prev_joltage * 10 + digit);
                prev_joltage = *max_joltage;
                *max_joltage = temp;
            }
        }
        ans1 += num_digits_to_max_joltage[PART_1_JOLTAGE_DIGITS];
        ans2 += num_digits_to_max_joltage[PART_2_JOLTAGE_DIGITS];
    }
    println!("{}\n{}", ans1, ans2);
}
