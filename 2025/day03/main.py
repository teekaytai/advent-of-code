t1 = 0
t2 = 0
for l in map(str.strip, open(0)):
    dp = [0] * 13
    for d in map(int, l):
        for i in range(12, 0, -1):
            dp[i] = max(dp[i], dp[i - 1] * 10 + d)
    t1 += dp[2]
    t2 += dp[12]
print(t1)
print(t2)
