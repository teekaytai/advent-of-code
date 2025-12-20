use std::{
    collections::HashMap,
    io::{self, BufRead},
};

const START: u8 = b'S';
const SPLITTER: u8 = b'^';

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let first_line = lines.next().unwrap()?;
    let start_col = first_line.bytes().position(|b| b == START).unwrap();
    let mut cols_to_beams = HashMap::new();
    cols_to_beams.insert(start_col, 1u64);
    let mut cols_to_new_beams: HashMap<_, u64> = HashMap::new();

    let mut ans1 = 0;
    for line in lines {
        for (col, b) in line?.bytes().enumerate() {
            if b == SPLITTER
                && let Some(beam_count) = cols_to_beams.remove(&col)
            {
                *cols_to_new_beams.entry(col - 1).or_default() += beam_count;
                *cols_to_new_beams.entry(col + 1).or_default() += beam_count;
                ans1 += 1;
            }
        }
        for (col, new_beams) in cols_to_new_beams.drain() {
            *cols_to_beams.entry(col).or_default() += new_beams;
        }
    }
    let ans2 = cols_to_beams.values().sum::<u64>();

    println!("{}\n{}", ans1, ans2);
    Ok(())
}
