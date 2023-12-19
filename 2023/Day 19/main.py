from abc import ABC, abstractmethod
from collections import defaultdict
from math import prod
import sys
from typing import NamedTuple, Optional

Label = str
Category = str

START_LABEL = 'in'
ACCEPT = 'A'
REJECT = 'R'
CONTINUE = 'C'  # Special label to denote continuing on the same workflow
DECISION_LABELS = [ACCEPT, REJECT]
CATEGORIES: list[Category] = ['x', 'm', 'a', 's']
MIN_FIELD_VALUE = 1
MAX_FIELD_VALUE = 4000


class Interval(NamedTuple):
    lo: int  # Inclusive
    hi: int  # Exclusive

    def size(self) -> int:
        return self.hi - self.lo


class Part:
    def __init__(self, fields: dict[Category, int]) -> None:
        self.fields = fields

    @classmethod
    def from_str(cls, part_str: str) -> 'Part':
        # fields = eval(f'dict({part_str.strip("{}")})')  # Tempting
        fields: dict[Category, int] = {}
        for field in part_str.strip('{}').split(','):
            category, value = field.split('=')
            fields[category] = int(value)
        return cls(fields)

    def __getitem__(self, category: Category) -> int:
        return self.fields[category]

    def value_sum(self) -> int:
        return sum(self.fields.values())


class PartRange:
    def __init__(self, field_ranges: dict[Category, Interval]) -> None:
        self.field_ranges = field_ranges

    @classmethod
    def from_bounds(cls, lo: int, hi: int) -> 'PartRange':
        interval = Interval(lo, hi)
        return cls({category: interval for category in CATEGORIES})

    # split will end up in the higher interval
    def partition(self, category: Category, split: int) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        lo, hi = self.field_ranges[category]
        lo_range: Optional[PartRange] = None
        hi_range: Optional[PartRange] = None
        if split > lo:
            lo_range = PartRange({**self.field_ranges, category: Interval(lo, min(split, hi))})
        if split < hi:
            hi_range = PartRange({**self.field_ranges, category: Interval(max(split, lo), hi)})
        return lo_range, hi_range

    def combination_count(self) -> int:
        return prod(map(Interval.size, self.field_ranges.values()))


class Rule(ABC):
    def __init__(self, label: Label) -> None:
        self.label = label

    @staticmethod
    def from_str(rule_str: str) -> 'Rule':
        if ':' in rule_str:
            return BoundRule.from_str(rule_str)
        return FixedRule.from_str(rule_str)

    @abstractmethod
    def process_part(self, part: Part) -> Label: ...

    # Process a PartRange and return a PartRange with a resulting label and
    # a PartRange that would continue being processed by the workflow
    @abstractmethod
    def process_part_range(self, part_range: PartRange) -> tuple[Label, Optional[PartRange], Optional[PartRange]]: ...


class FixedRule(Rule):
    def __init__(self, label: Label) -> None:
        super().__init__(label)

    @classmethod
    def from_str(cls, rule_str: str) -> 'FixedRule':
        return cls(rule_str)

    def process_part(self, _: Part) -> Label:
        return self.label

    def process_part_range(self, part_range: PartRange) -> tuple[Label, PartRange, None]:
        return self.label, part_range, None


class BoundRule(Rule):
    def __init__(self, category: Category, is_upper_bound: bool, bound: int, label: Label) -> None:
        super().__init__(label)
        self.category: Category = category
        self.is_upper_bound = is_upper_bound
        self.bound = bound

    @classmethod
    def from_str(cls, rule_str: str) -> 'BoundRule':
        condition, label = rule_str.split(':')
        category = condition[0]
        is_upper_bound = condition[1] == '<'
        bound = int(condition[2:])
        return cls(category, is_upper_bound, bound, label)

    def process_part(self, part: Part) -> Label:
        value = part[self.category]
        cond = value < self.bound if self.is_upper_bound else value > self.bound
        return self.label if cond else CONTINUE

    def process_part_range(self, part_range: PartRange) -> tuple[Label, Optional[PartRange], Optional[PartRange]]:
        if self.is_upper_bound:
            return self.label, *part_range.partition(self.category, self.bound)
        else:
            return self.label, *part_range.partition(self.category, self.bound + 1)[::-1]


class Workflow:
    def __init__(self, rules: list[Rule]) -> None:
        self.rules = rules

    @classmethod
    def from_str(cls, workflow_str: str) -> 'Workflow':
        rules = [Rule.from_str(rule_str) for rule_str in workflow_str.split(',')]
        return cls(rules)

    def process_part(self, part: Part) -> Label:
        for rule in self.rules:
            label = rule.process_part(part)
            if label != CONTINUE:
                return label
        # Should not be reached if all workflows constructed with FixedRules at the end
        raise RuntimeError('Unexpected condition: Workflow cannot process part')

    def process_part_range(self, part_range: PartRange) -> dict[Label, list[PartRange]]:
        results: defaultdict[Label, list[PartRange]] = defaultdict(list)
        curr_part_range = part_range
        for rule in self.rules:
            label, done_range, continue_range = rule.process_part_range(curr_part_range)
            if done_range is not None:
                results[label].append(done_range)
            if continue_range is None:
                break
            curr_part_range = continue_range
        return results


class WorkflowCollection:
    def __init__(self, workflows: dict[Label, Workflow]) -> None:
        self.workflows = workflows

    @classmethod
    def from_str(cls, workflow_collection_str: str) -> 'WorkflowCollection':
        workflows: dict[Label, Workflow] = {}
        for named_workflow_str in workflow_collection_str.split():
            name, workflow_str = named_workflow_str.rstrip('}').split('{')
            workflows[name] = Workflow.from_str(workflow_str)
        return cls(workflows)

    def is_accepted(self, part: Part) -> bool:
        label: Label = START_LABEL
        while label not in DECISION_LABELS:
            label = self.workflows[label].process_part(part)
        return label == ACCEPT

    def find_accepted(self, part_range: PartRange, label: Label = START_LABEL) -> list[PartRange]:
        accepted_ranges: list[PartRange] = []
        results = self.workflows[label].process_part_range(part_range)
        for result_label, part_ranges in results.items():
            if result_label == ACCEPT:
                accepted_ranges.extend(part_ranges)
                continue
            if result_label == REJECT:
                continue
            for part_range in part_ranges:
                accepted_ranges.extend(self.find_accepted(part_range, result_label))
        return accepted_ranges


workflows_section, parts_section = sys.stdin.read().split('\n\n')
workflows = WorkflowCollection.from_str(workflows_section)
parts = [Part.from_str(part_str) for part_str in parts_section.split()]

# Part 1
print(sum(part.value_sum() for part in parts if workflows.is_accepted(part)))

# Part 2
complete_part_range = PartRange.from_bounds(MIN_FIELD_VALUE, MAX_FIELD_VALUE + 1)
print(sum(part_range.combination_count() for part_range in workflows.find_accepted(complete_part_range)))
