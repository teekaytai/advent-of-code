#include <iostream>
#include <unordered_set>
#include <sstream>
#include <stack>

struct IntPairHash {
    size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<long long>{}(((long long) p.first << 32) + p.second);
    }
};

int main() {
    const std::pair<int, int> kSource = {500, 0};
    const int kDirs[] = {0, -1, 1};

    std::unordered_set<std::pair<int, int>, IntPairHash> blocked_cells;
    int max_y = 0;
    std::string line;
    while (getline(std::cin, line) && !line.empty()) {
        std::stringstream ss(line);
        char ignored;
        int x, y;
        int x2, y2;
        ss >> x >> ignored >> y;
        max_y = std::max(max_y, y);
        blocked_cells.emplace(x, y);
        while (ss >> ignored >> ignored >> x2 >> ignored >> y2) { // " -> x,y"
            if (x2 != x) {
                int lo_x = std::min(x, x2);
                int hi_x = std::max(x, x2);
                for (int i = lo_x; i <= hi_x; ++i) {
                    blocked_cells.emplace(i, y);
                }
            } else { // y2 != y
                max_y = std::max(max_y, y2);
                int lo_y = std::min(y, y2);
                int hi_y = std::max(y, y2);
                for (int i = lo_y; i <= hi_y; ++i) {
                    blocked_cells.emplace(x, i);
                }
            }
            x = x2;
            y = y2;
        }
    }

    int total_sand = 0;
    std::stack<std::pair<int, int>> path;
    path.push(kSource);
    while (!path.empty()) {
        auto [x, y] = path.top();
        // Part 1
        // if (y >= max_y) {
        //     // Sand fallen past bottom-most rocks
        //     break;
        // }

        bool at_rest = true;
        if (y <= max_y) {
            // Sand has not reached floor level
            int y2 = y + 1;
            for (int dx : kDirs) {
                int x2 = x + dx;
                if (!blocked_cells.contains({x2, y2})) {
                    path.emplace(x2, y2);
                    at_rest = false;
                    break;
                }
            }
        }

        if (at_rest) {
            ++total_sand;
            blocked_cells.emplace(x, y);
            path.pop();
        }
    }
    std::cout << total_sand << "\n";
}
