# Reject OOP, return to Procedural
from math import prod
import sys

Label = str
Category = str
Rule = tuple[Category, bool, int, Label]
Part = dict[Category, int]
PartRange = dict[Category, tuple[int, int]]

START_LABEL = 'in'
ACCEPT = 'A'
REJECT = 'R'
DECISION_LABELS = [ACCEPT, REJECT]
CATEGORIES: list[Category] = ['x', 'm', 'a', 's']
MIN_FIELD_VALUE = 1
MAX_FIELD_VALUE = 4000


workflows_section, parts_section = sys.stdin.read().split('\n\n')
workflows: dict[Label, tuple[list[Rule], Label]] = {}
for workflow_str in workflows_section.split():
    label, steps = workflow_str.rstrip('}').split('{')
    *steps_list, final_label = steps.split(',')
    rules_list: list[Rule] = []
    for step in steps_list:
        test, result_label = step.split(':')
        category = test[0]
        is_upper_bound = test[1] == '<'
        bound = int(test[2:])
        rules_list.append((category, is_upper_bound, bound, result_label))
    workflows[label] = (rules_list, final_label)
parts: list[Part] = []
for part_str in parts_section.split():
    # part = eval(f'dict({part_str.strip("{}")})')  # Tempting
    part: Part = {}
    for field in part_str.strip('{}').split(','):
        category, value_str = field.split('=')
        part[category] = int(value_str)
    parts.append(part)

# Part 1
total = 0
for part in parts:
    curr_label = START_LABEL
    while curr_label not in DECISION_LABELS:
        rules_list, final_label = workflows[curr_label]
        for category, is_upper_bound, bound, label in rules_list:
            value = part[category]
            cond = value < bound if is_upper_bound else value > bound
            if cond:
                curr_label = label
                break
        else:
            curr_label = final_label
    if curr_label == ACCEPT:
        total += sum(part.values())
print(total)


# Part 2
def dfs(part_range: PartRange, label: Label) -> int:
    if label == REJECT:
        return 0
    if label == ACCEPT:
        return prod(hi - lo for lo, hi in part_range.values())

    total = 0
    curr_part_range = part_range
    rules_list, final_label = workflows[label]
    for category, is_upper_bound, bound, result_label in rules_list:
        lo, hi = curr_part_range[category]
        if is_upper_bound:
            if bound > lo:
                total += dfs({**curr_part_range, category: (lo, min(bound, hi))}, result_label)
            if bound >= hi:
                break
            curr_part_range = {**curr_part_range, category: (max(bound, lo), hi)}
        else:
            if bound + 1 < hi:
                total += dfs({**curr_part_range, category: (max(bound + 1, lo), hi)}, result_label)
            if bound < lo:
                break
            curr_part_range = {**curr_part_range, category: (lo, min(bound + 1, hi))}
    else:
        total += dfs(curr_part_range, final_label)

    return total

complete_part_range: PartRange = {category: (MIN_FIELD_VALUE, MAX_FIELD_VALUE + 1) for category in CATEGORIES}
print(dfs(complete_part_range, START_LABEL))
