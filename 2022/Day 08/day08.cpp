#include <algorithm>
#include <iostream>
#include <vector>
#include <stack>

int main() {
    std::string line;
    std::vector<std::string> grid;
    while (std::cin >> line) {
        grid.push_back(line);
    }
    int H = grid.size();
    int W = grid[0].size();
    std::vector<std::vector<bool>> visibilities(H, std::vector<bool>(W)); // Part 1
    std::vector<std::vector<int>> scenic_scores(H, std::vector<int>(W, 1)); // Part 2

    for (int r = 0; r < H; ++r) {
        // Monotonic non-increasing stack of tree heights and corresponding indices
        std::stack<std::pair<char, int>> trees;
        for (int c = 0; c < W; ++c) {
            char tree = grid[r][c];
            while (!trees.empty() && tree > trees.top().first) {
                trees.pop();
            }
            if (trees.empty()) {
                // Taller than every tree earlier
                visibilities[r][c] = true;
                scenic_scores[r][c] *= c;
            } else {
                scenic_scores[r][c] *= c - trees.top().second;
            }
            trees.emplace(tree, c);
        }

        trees = {};
        for (int c = W - 1; c >= 0; --c) {
            char tree = grid[r][c];
            while (!trees.empty() && tree > trees.top().first) {
                trees.pop();
            }
            if (trees.empty()) {
                // Taller than every tree earlier
                visibilities[r][c] = true;
                scenic_scores[r][c] *= W - c - 1;
            } else {
                scenic_scores[r][c] *= trees.top().second - c;
            }
            trees.emplace(tree, c);
        }
    }

    for (int c = 0; c < W; ++c) {
        // Monotonic non-increasing stack of tree heights and corresponding indices
        std::stack<std::pair<char, int>> trees;
        for (int r = 0; r < H; ++r) {
            char tree = grid[r][c];
            while (!trees.empty() && tree > trees.top().first) {
                trees.pop();
            }
            if (trees.empty()) {
                // Taller than every tree earlier
                visibilities[r][c] = true;
                scenic_scores[r][c] *= r;
            } else {
                scenic_scores[r][c] *= r - trees.top().second;
            }
            trees.emplace(tree, r);
        }

        trees = {};
        for (int r = H - 1; r >= 0; --r) {
            char tree = grid[r][c];
            while (!trees.empty() && tree > trees.top().first) {
                trees.pop();
            }
            if (trees.empty()) {
                // Taller than every tree earlier
                visibilities[r][c] = true;
                scenic_scores[r][c] *= H - r - 1;
            } else {
                scenic_scores[r][c] *= trees.top().second - r;
            }
            trees.emplace(tree, r);
        }
    }

    int total_visible = 0;
    int max_scenic_score = INT32_MIN;
    for (int r = 0; r < H; ++r) {
        total_visible += std::count(visibilities[r].begin(), visibilities[r].end(), true);
        max_scenic_score = std::max(max_scenic_score,
                                    *std::max_element(scenic_scores[r].begin(), scenic_scores[r].end()));
    }

    std::cout << total_visible << "\n" << max_scenic_score << "\n";
}
