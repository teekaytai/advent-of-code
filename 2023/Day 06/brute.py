# Part 1
# times = [int(x) for x in input().split()[1:]]
# distances = [int(x) for x in input().split()[1:]]

# Part 2
times = [int(''.join(input().split()[1:]))]
distances = [int(''.join(input().split()[1:]))]

product = 1
for time, dist in zip(times, distances):
    num_ways = 0
    for i in range(time):
        if (time - i) * i > dist:
            num_ways += 1
    product *= num_ways
print(product)
