#include <iostream>
#include <unordered_set>
#include <vector>

using namespace std;

struct IntPairHash {
    size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<long long>{}(((long long) p.first << 32) + p.second);
    }
};

bool hits_cyclone(const vector<string>& grid, int H, int W, int r, int c, int turn) {
    static constexpr array<pair<int, int>, 4> kDirs{{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}};
    static constexpr array<char, 4> kCyclones{{'<', '^', '>', 'v'}}; // Opposite to movement directions

    for (int i = 0; i < kDirs.size(); ++i) {
        auto [dr, dc] = kDirs[i];
        // Find where cyclone must have started to reach my cell on this turn
        int r2 = ((r + turn * dr) % H + H) % H;
        int c2 = ((c + turn * dc) % W + W) % W;
        if (grid[r2][c2] == kCyclones[i]) {
            return true;
        }
    }
    return false;
}

int main() {
    constexpr array<pair<int, int>, 4> kDirs{{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}};

    vector<string> grid;
    string line;
    getline(cin, line);
    while (getline(cin, line) && line[1] != '#') {
        grid.push_back(line.substr(1, line.size() - 2)); // Remove walls on sides
    }
    int H = grid.size();
    int W = grid[0].size();

    pair<int, int> start_cell_inner{0, 0};
    pair<int, int> start_cell_outer{-1, 0};
    pair<int, int> end_cell_inner{H - 1, W - 1};
    pair<int, int> end_cell_outer{H, W - 1};
    // Set to {{end_cell_inner}} for part 1
    array<pair<int, int>, 3> target_cells{{end_cell_inner, start_cell_inner, end_cell_inner}};
    int target_cell_index = 0;

    unordered_set<pair<int, int>, IntPairHash> curr_cells;
    unordered_set<pair<int, int>, IntPairHash> next_cells;
    curr_cells.insert(start_cell_outer);
    int turn;
    for (turn = 1; !curr_cells.empty(); ++turn) {
        for (auto [r, c] : curr_cells) {
            for (auto [dr, dc] : kDirs) {
                int r2 = r + dr;
                int c2 = c + dc;
                if (r2 < 0 || r2 >= H || c2 < 0 || c2 >= W) {
                    continue;
                }
                if (hits_cyclone(grid, H, W, r2, c2, turn)) {
                    continue;
                }
                next_cells.emplace(r2, c2);
            }
            // Try waiting
            // r < 0 or r >= H only applicable when on the outer start or end cells outside grid
            if (r < 0 || r >= H || !hits_cyclone(grid, H, W, r, c, turn)) {
                next_cells.emplace(r, c);
            }
        }

        curr_cells.swap(next_cells);
        next_cells.clear();

        if (curr_cells.contains(target_cells[target_cell_index])) {
            curr_cells.clear();
            curr_cells.insert(target_cells[target_cell_index] == start_cell_inner ? start_cell_outer : end_cell_outer);
            ++turn;
            ++target_cell_index;
            if (target_cell_index >= target_cells.size()) {
                break;
            }
        }
    }
    cout << turn << "\n";
}
