from math import lcm
import sys

instruction_order = input()
L = len(instruction_order)
input()

# Part 1
# start_nodes: list[str] = ['AAA']
start_nodes: list[str] = []
adj_list: dict[str, tuple[str, str]] = {}
for line in sys.stdin:
    node, adjs = line.strip().split(' = ')
    left_adj, right_adj = adjs[1:-1].split(', ')
    adj_list[node] = (left_adj, right_adj)

    # Part 2
    if node.endswith('A'):
        start_nodes.append(node)

# This solution requires certain special properties about the input highlighted below
cycle_lengths = []
for start_node in start_nodes:
    curr = start_node
    steps = 0
    while not curr.endswith('Z'):
        curr = adj_list[curr][instruction_order[steps % L] == 'R']
        steps += 1
    cycle_lengths.append(steps)

    # The path taken from an end node always cycles back to the same end node.
    # This cycle has the same length as the path from the start node to the end node.
    # Also, the path length is divisible by the length of the instructions, so the state
    # always resets back to the first instruction after the end node is reached.
    assert steps % L == 0
    end_node = curr
    for i in range(steps):
        curr = adj_list[curr][instruction_order[i % L] == 'R']
    assert curr == end_node

print(lcm(*cycle_lengths))
