import math

# Part 1
# times = [int(x) for x in input().split()[1:]]
# distances = [int(x) for x in input().split()[1:]]

# Part 2
times = [int(''.join(input().split()[1:]))]
distances = [int(''.join(input().split()[1:]))]

product = 1
for time, dist in zip(times, distances):
    # Since the distance traveled is (time - x) * x where x is the time the button is held,
    # we can directly solve for when (time - x) * x > dist, giving:
    # (time - (time**2 - 4*dist) ** 0.5) / 2 < x < (time + (time**2 - 4*dist) ** 0.5) / 2
    D = (time**2 - 4*dist) ** 0.5
    product *= math.ceil((time + D) / 2) - math.floor((time - D) / 2) - 1
print(product)
