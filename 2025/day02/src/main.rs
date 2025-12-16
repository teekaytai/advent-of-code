use std::io::{self};

fn main() {
    let mut ans1 = 0;
    let mut ans2 = 0;
    let input = {
        let mut s = String::new();
        io::stdin().read_line(&mut s).unwrap();
        s.trim_end().to_owned()
    };
    for interval in input.split(',') {
        let (lo_str, hi_str) = interval.split_once('-').unwrap();
        let lo = lo_str.parse::<u64>().unwrap();
        let hi = hi_str.parse::<u64>().unwrap();
        for i in lo..=hi {
            let i_str = i.to_string();
            let k = i_str.len();
            if k % 2 == 0 && i_str[..k / 2].repeat(2) == i_str {
                ans1 += i;
            }
            if (1..=k / 2).any(|j| k % j == 0 && i_str[..j].repeat(k / j) == i_str) {
                ans2 += i;
            }
        }
    }
    println!("{}\n{}", ans1, ans2);
}
