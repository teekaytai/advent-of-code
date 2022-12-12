#include <iostream>
#include <queue>
#include <vector>

int main() {
    const char kStartChar = 'S';
    const char kEndChar = 'E';
    const char kStartElevation = 'a';
    const char kEndElevation = 'z';
    const int kNotVisited = -1;
    const std::pair<int, int> kDirs[] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    std::vector<std::string> grid;
    std::string line;
    while (std::cin >> line) {
        grid.push_back(line);
    }
    int h = grid.size();
    int w = grid[0].size();

    int start_r, start_c, end_r, end_c;
    for (int r = 0; r < h; ++r) {
        int c = grid[r].find(kStartChar);
        if (c != std::string::npos) {
            start_r = r;
            start_c = c;
            grid[r][c] = kStartElevation;
            break;
        }
    }
    for (int r = 0; r < h; ++r) {
        int c = grid[r].find(kEndChar);
        if (c != std::string::npos) {
            end_r = r;
            end_c = c;
            grid[r][c] = kEndElevation;
            break;
        }
    }

    int *steps_needed[h];
    for (int r = 0; r < h; ++r) {
        int* row = new int[w];
        std::fill(row, row + w, kNotVisited);
        steps_needed[r] = row;
    }

    std::queue<std::pair<int, int>> pos_queue;
    // Part 1: Begin from start position 'S'
    // pos_queue.emplace(start_r, start_c);
    // steps_needed[start_r][start_c] = 0;
    // Part 2: Begin from end position 'E'
    pos_queue.emplace(end_r, end_c);
    steps_needed[end_r][end_c] = 0;

    bool target_reached = false;
    while (!target_reached && !pos_queue.empty()) {
        auto& [r, c] = pos_queue.front();
        pos_queue.pop();
        for (auto& [dr, dc] : kDirs) {
            int r2 = r + dr;
            int c2 = c + dc;
            if (r2 < 0 || r2 >= h || c2 < 0 || c2 >= w) {
                continue;
            }
            // Part 1: Check next position at most 1 level higher
            // bool elevation_unreachable = grid[r2][c2] - grid[r][c] > 1;
            // Part 2: Check current position at most 1 level higher, since we are travelling backwards
            bool elevation_unreachable = grid[r][c] - grid[r2][c2] > 1;
            if (elevation_unreachable) {
                continue;
            }

            if (steps_needed[r2][c2] == kNotVisited) {
                steps_needed[r2][c2] = steps_needed[r][c] + 1;
                pos_queue.emplace(r2, c2);
                // Part 1: Target is end position 'E'
                // bool is_target = r2 == end_r && c2 == end_c;
                // Part 2: Target is any position with the lowest elevation 'a'
                bool is_target = grid[r2][c2] == kStartElevation;
                if (is_target) {
                    target_reached = true;
                    std::cout << steps_needed[r2][c2] << "\n";
                    break;
                }
            }
        }
    }
}
