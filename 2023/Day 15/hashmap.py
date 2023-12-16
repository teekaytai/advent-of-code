from typing import Iterable

# This solution is probably the actual intended solution, where we implement our own hashmap with separate chaining
class HolidayHashMap:
    NUM_BOXES = 256

    def __init__(self) -> None:
        self.boxes: list[list[tuple[str, int]]] = [[] for _ in range(HolidayHashMap.NUM_BOXES)]

    @staticmethod
    def holiday_hash(key: str) -> int:
        h = 0
        for char in key:
            h = (h + ord(char)) * 17 % HolidayHashMap.NUM_BOXES
        return h

    def process_ops(self, ops: Iterable[str]) -> None:
        for op in ops:
            self.process_op(op)

    def process_op(self, op: str) -> None:
        if op[-1] == '-':
            self.remove_label(op[:-1])
        else:
            key, val = op.split('=')
            self.update_label(key, int(val))

    def remove_label(self, key: str) -> None:
        hsh = self.holiday_hash(key)
        box = self.boxes[hsh]
        for i, (curr_key, _) in enumerate(box):
            if curr_key == key:
                box.pop(i)
                break

    def update_label(self, key: str, val: int) -> None:
        hsh = self.holiday_hash(key)
        box = self.boxes[hsh]
        for i, (curr_key, _) in enumerate(box):
            if curr_key == key:
                box[i] = (key, val)
                break
        else:
            box.append((key, val))

    def get_summary_value(self) -> int:
        return sum(
            i * sum(j * val for j, (_, val) in enumerate(box, start=1))
            for i, box in enumerate(self.boxes, start=1)
        )


operations = input().split(',')

# Part 1
print(sum(map(HolidayHashMap.holiday_hash, operations)))

# Part 2
hash_map = HolidayHashMap()
hash_map.process_ops(operations)
print(hash_map.get_summary_value())
