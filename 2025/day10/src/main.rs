// Credit to this reddit post for finding a much more elegant solution that does not
// use linear algebra and looks far more likely to be the intended solution.
// https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

use std::{
    collections::HashMap,
    io::{self, BufRead},
    ops::{AddAssign, DivAssign, MulAssign, SubAssign},
};

struct Button {
    outputs: Vec<usize>,
}

impl Button {
    fn parse(s: &str) -> Self {
        let outputs = s[1..s.len() - 1]
            .split(',')
            .map(|x| x.parse().unwrap())
            .collect();
        Button { outputs }
    }
}

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct Joltages {
    counts: Vec<i32>,
}

impl Joltages {
    fn parse(s: &str) -> Self {
        let counts = s[1..s.len() - 1]
            .split(',')
            .map(|x| x.parse().unwrap())
            .collect();
        Joltages { counts }
    }

    fn len(&self) -> usize {
        self.counts.len()
    }

    fn is_valid(&self) -> bool {
        self.counts.iter().all(|&count| count >= 0)
    }

    fn parity_mask(&self) -> usize {
        self.counts
            .iter()
            .fold(0, |mask, &count| (mask << 1) | ((count & 1) as usize))
    }

    fn apply_button(&mut self, button: &Button) {
        for &x in &button.outputs {
            self.counts[x] += 1;
        }
    }

    fn unapply_button(&mut self, button: &Button) {
        for &x in &button.outputs {
            self.counts[x] -= 1;
        }
    }
}

impl AddAssign<&Joltages> for Joltages {
    fn add_assign(&mut self, other: &Joltages) {
        for (count, add_count) in self.counts.iter_mut().zip(other.counts.iter()) {
            *count += add_count;
        }
    }
}

impl SubAssign<&Joltages> for Joltages {
    fn sub_assign(&mut self, other: &Joltages) {
        for (count, sub_count) in self.counts.iter_mut().zip(other.counts.iter()) {
            *count -= sub_count;
        }
    }
}

impl MulAssign<i32> for Joltages {
    fn mul_assign(&mut self, x: i32) {
        for count in self.counts.iter_mut() {
            *count *= x;
        }
    }
}

impl DivAssign<i32> for Joltages {
    fn div_assign(&mut self, x: i32) {
        for count in self.counts.iter_mut() {
            *count /= x;
        }
    }
}

#[derive(Debug, Clone)]
struct ButtonSet {
    total_buttons: u32,
    joltage_changes: Joltages,
}

const LIGHT_ON: u8 = b'#';
const MAX_NUM_JOLTAGES: usize = 10;
const INF: u32 = u32::MAX / 4;

fn parse_light_diagram(light_diagram: &str) -> usize {
    let light_bytes = light_diagram.as_bytes();
    let mut mask = 0;
    for &c in &light_bytes[1..light_bytes.len() - 1] {
        mask = mask * 2 + ((c == LIGHT_ON) as usize)
    }
    mask
}

fn collect_button_sets_helper(
    parity_masks_to_button_sets: &mut Vec<Vec<ButtonSet>>,
    buttons: &[Button],
    curr_joltages: &mut Joltages,
    total_buttons_used: u32,
    button_idx: usize,
) {
    if button_idx == buttons.len() {
        return;
    }
    collect_button_sets_helper(
        parity_masks_to_button_sets,
        buttons,
        curr_joltages,
        total_buttons_used,
        button_idx + 1,
    );
    curr_joltages.apply_button(&buttons[button_idx]);
    let parity_mask = curr_joltages.parity_mask();
    let button_set = ButtonSet {
        total_buttons: total_buttons_used + 1,
        joltage_changes: curr_joltages.clone(),
    };
    parity_masks_to_button_sets[parity_mask].push(button_set);
    collect_button_sets_helper(
        parity_masks_to_button_sets,
        buttons,
        curr_joltages,
        total_buttons_used + 1,
        button_idx + 1,
    );
    curr_joltages.unapply_button(&buttons[button_idx]);
}

fn collect_button_sets(
    parity_masks_to_button_sets: &mut Vec<Vec<ButtonSet>>,
    buttons: &[Button],
    num_joltages: usize,
) {
    for button_sets in &mut parity_masks_to_button_sets[..1 << num_joltages] {
        button_sets.clear();
    }
    let mut curr_joltages = Joltages {
        counts: vec![0; num_joltages],
    };
    parity_masks_to_button_sets[0].push(ButtonSet {
        total_buttons: 0,
        joltage_changes: curr_joltages.clone(),
    });
    collect_button_sets_helper(
        parity_masks_to_button_sets,
        buttons,
        &mut curr_joltages,
        0,
        0,
    );
}

fn min_button_pushes_for_joltages(
    parity_masks_to_button_sets: &[Vec<ButtonSet>],
    target_joltages: &Joltages,
) -> u32 {
    let mut memo = HashMap::new();
    let zero_joltages = Joltages {
        counts: vec![0; target_joltages.len()],
    };
    memo.insert(zero_joltages, 0);
    fn helper(
        memo: &mut HashMap<Joltages, u32>,
        parity_masks_to_button_sets: &[Vec<ButtonSet>],
        joltages: &mut Joltages,
    ) -> u32 {
        match memo.get(joltages) {
            Some(&min_button_pushes) => min_button_pushes,
            None => {
                let parity_mask = joltages.parity_mask();
                let mut min_button_pushes = INF;
                for button_set in &parity_masks_to_button_sets[parity_mask] {
                    *joltages -= &button_set.joltage_changes;
                    if joltages.is_valid() {
                        *joltages /= 2;
                        min_button_pushes = min_button_pushes.min(
                            button_set.total_buttons
                                + 2 * helper(memo, parity_masks_to_button_sets, joltages),
                        );
                        *joltages *= 2;
                    }
                    *joltages += &button_set.joltage_changes;
                }
                memo.insert(joltages.clone(), min_button_pushes);
                min_button_pushes
            }
        }
    }
    helper(
        &mut memo,
        parity_masks_to_button_sets,
        &mut target_joltages.clone(),
    )
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut ans1 = 0;
    let mut ans2 = 0;
    let mut parity_masks_to_button_sets = vec![Vec::new(); 1 << MAX_NUM_JOLTAGES];
    for line in stdin.lock().lines() {
        let line = line?;
        let mut parts = line.split_ascii_whitespace();
        let lights_parity_mask = parse_light_diagram(parts.next().unwrap());
        let joltage_counters = Joltages::parse(parts.next_back().unwrap());
        let num_joltages = joltage_counters.len();
        let buttons: Vec<_> = parts.map(Button::parse).collect();
        collect_button_sets(&mut parity_masks_to_button_sets, &buttons, num_joltages);

        ans1 += parity_masks_to_button_sets[lights_parity_mask]
            .iter()
            .map(|button_set| button_set.total_buttons)
            .min()
            .unwrap();
        ans2 += min_button_pushes_for_joltages(&parity_masks_to_button_sets, &joltage_counters);
    }

    println!("{}\n{}", ans1, ans2);
    Ok(())
}
