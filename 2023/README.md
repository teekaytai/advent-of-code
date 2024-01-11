Python is easily my strongest programming language, so for an extra challenge I'll make golf solutions in addition to writing proper, clean solutions for each day. Where possible, I'll also try solving problems in more *interesting* ways.

Some notes about my golf solutions:
* All golf solutions take input via stdin and print out the answer in stdout. So if you have the input in a file called `input.txt`, you can run the solution in bash/zsh using `python golf_part_x.py < input.txt`
* All solutions accept the input from the website as is without needing any manual preprocessing
* I'm avoiding using any third party libraries
* A few solutions rely on the input having Unix line endings (`'\n'`), not Windows line endings (`'\r\n'`)
* A few solutions rely on there being a newline character at the end of the input
* Yes those abominations really do run, and give the correct answers

| Day | Golf Sizes (bytes) | Tags | Remarks |
|:---:|:------------------:|------|---------|
| [1](Day%2001) | [69](Day%2001/golf_part1.py), [188](Day%2001/golf_part2.py) | Brute Force, Rabin Karp | |
| [2](Day%2002) | [117](Day%2002/golf_part1.py), [136](Day%2002/golf_part2.py) | Parsing, Regex | |
| [3](Day%2003) | [215](Day%2003/golf_part1.py), [300](Day%2003/golf_part2.py) | 2D Array | |
| [4](Day%2004) | [63](Day%2004/golf_part1.py), [114](Day%2004/golf_part2.py) | DP | Really like how *simple* the golf solution for part 1 turned out to be |
| [5](Day%2005) | [189](Day%2005/golf_part1.py), [292](Day%2005/golf_part2.py) | Intervals | |
| [6](Day%2006) | [105](Day%2006/golf_part1.py), [88](Day%2006/golf_part2.py) | Brute Force, Binary Search, Peak Finding, Mathematics | |
| [7](Day%2007) | [222](Day%2007/golf_part1.py), [276](Day%2007/golf_part2.py) | Sorting, Greedy, Horner's Method | Super proud of how the card scoring functions turned out (especially the golfed ones 😈) |
| [8](Day%2008) | [130](Day%2008/golf_part1.py), [199](Day%2008/golf_part2.py) | Mathematics | |
| [9](Day%2009) | [103](Day%2009/golf_part1.py), [102](Day%2009/golf_part2.py) | Mathematics, Method of Finite Differences | I've got a solution which estimates the answer by using NumPy to approximate the polynomials that produce the given sequences. I've also written a solution which directly calculates the answers with an explicit formula involving binomial coefficients |
| [10](Day%2010) | [245](Day%2010/golf_part1.py), [290](Day%2010/golf_part2.py) | BFS/DFS, Ray Casting Algorithm, Jordan Curve Theorem, Shoelace Formula, Pick's Theorem | Realizing that I can flatten the grid into 1D to access elements with a single index saved more than 100 characters! Absolutely nuts.<br>UPDATE: Unsurprisingly, the shoelace formula helped shorten the golf solution for part 2 even further. I've kept the old solution around too since it'd be a shame to get rid of it after all the time I'd already sunk into it... The enclosed-tile-counting logic fits in one line! |
| [11](Day%2011) | [205](Day%2011/golf_part1.py), [212](Day%2011/golf_part2.py) | Prefix Sums | |
| [12](Day%2012) | [224](Day%2012/golf_part1.py), [273](Day%2012/golf_part2.py) | DP, Suffix Sums | |
| [13](Day%2013) | [168](Day%2013/golf_part1.py), [200](Day%2013/golf_part2.py) | Palindromes, Bitmasks, Manacher's | |
| [14](Day%2014) | [101](Day%2014/golf_part1.py), [245](Day%2014/golf_part2.py) | Hashing, Simulation | |
| [15](Day%2015) | [82](Day%2015/golf_part1.py), [178](Day%2015/golf_part2.py) | Hashing, OOP | Part 1's got 2 equally good one-liner golf solutions |
| [16](Day%2016) | [258](Day%2016/golf_part1.py), [353](Day%2016/golf_part2.py) | DFS/BFS, Simulation, Condensation Graphs, Kosaraju's Algorithm, DP | Would I make my code run 10 times slower, just so I can save 20 characters? Of course I would. I'd do it for just 1 character even... as long as it doesn't become *too* slow. Be warned that part 2's golf solution takes about 16s to run in pypy3. More interested in something fast? Then have a look at the solution using DP and Kosaraju's algorithm for finding strongly connected components |
| [17](Day%2017) | [278](Day%2017/golf_part1.py), [290](Day%2017/golf_part2.py) | Dijkstra, A* Search | |
| [18](Day%2018) | [120](Day%2018/golf_part1.py), [121](Day%2018/golf_part2.py) | Flood Fill, Sweep Line, Intervals, Shoelace Formula, Pick's Theorem | If I had known about the Shoelace formula beforehand, this would have been way easier... On the bright side, I can now confirm that an alternative solution using a sweep line algorithm exists |
| [19](Day%2019) | [257](Day%2019/golf_part1.py), [345](Day%2019/golf_part2.py) | DFS/BFS, Intervals, OOP | OOP is... long |
| [20](Day%2020) | [357](Day%2020/golf_part1.py), [196](Day%2020/golf_part2.py) | BFS, Simulation, Reverse Engineering, Mathematics, OOP | Very long |
| [21](Day%2021) | [109](Day%2021/golf_part1.py), [169](Day%2021/golf_part2.py) | BFS, Mathematics | |
| [22](Day%2022) | [277](Day%2022/golf_part1.py), [268](Day%2022/golf_part2.py) | DP, Simulation | |
| [23](Day%2023) | [187](Day%2023/golf_part1.py), [391](Day%2023/golf_part2.py) | NP-hard, Brute Force, DP, Bitmasks, DFS/BFS, Graph Construction | Gave optimising this one a go and got part 2 down to ~0.7s in pypy3, which by Python standards I believe is great! Interestingly, the solution using DP explores ~60% less states and yet takes about twice as long |
| [24](Day%2024) | WIP | Mathematics, Computational Geometry | |
| [25](Day%2025) | WIP | Max-Flow Min-Cut, Edmonds-Karp, BFS | Merry Christmas! |
