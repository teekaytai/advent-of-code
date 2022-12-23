#include <array>
#include <iostream>
#include <unordered_map>

using namespace std;

struct IntPairHash {
    size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<long long>{}(((long long) p.first << 32) + p.second);
    }
};

int main() {
    const int kPart1Round = 10;
    const int kDontMove = -1;
    constexpr array<pair<int, int>, 8> kNeighbours{
        {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}}};
    constexpr array<pair<int, int>, 4> kDirs{{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}};
    constexpr array<array<pair<int, int>, 3>, 4> kDirAdjacents{{
        {{{-1, -1}, {-1, 0}, {-1, 1}}},
        {{{1, -1}, {1, 0}, {1, 1}}},
        {{{-1, -1}, {0, -1}, {1, -1}}},
        {{{-1, 1}, {0, 1}, {1, 1}}}}};

    // Map elf positions to their intended movement direction
    unordered_map<pair<int, int>, int, IntPairHash> elves;
    string line;
    for (int r = 0; getline(cin, line); ++r) {
        for (int c = 0; c < line.length(); ++c) {
            if (line[c] == '#') {
                elves[{r, c}] = kDontMove;
            }
        }
    }

    unordered_map<pair<int, int>, int, IntPairHash> next_elves;
    int start_dir_index = 0;
    bool elf_moved = true;
    int num_rounds;
    for (num_rounds = 0; elf_moved; ++num_rounds) {
        elf_moved = false;
        // Elves propose movement
        for (const auto& [pos, _] : elves) {
            // Check if elf has any neighbours and needs to move
            bool has_neighbours = false;
            for (const auto [dr, dc] : kNeighbours) {
                if (elves.contains({pos.first + dr, pos.second + dc})) {
                    has_neighbours = true;
                    break;
                }
            }
            if (!has_neighbours) {
                continue;
            }


            for (int i = 0; i < kDirs.size(); ++i) {
                bool blocked = false;
                int dir_index = (start_dir_index + i) % 4;
                for (const auto [dr, dc] : kDirAdjacents[dir_index]) {
                    if (elves.contains({pos.first + dr, pos.second + dc})) {
                        blocked = true;
                        break;
                    }
                }
                if (!blocked) {
                    elves[pos] = dir_index;
                    break;
                }
            }
        }

        // Elves move at the same time if unhindered.
        // Only way to be blocked now is if elf 2 spaces away moves in opposite direction onto same position
        for (const auto& [pos, dir_index] : elves) {
            if (dir_index == kDontMove) {
                next_elves[pos] = kDontMove;
                continue;
            }
            auto [dr, dc] = kDirs[dir_index];
            auto it = elves.find({pos.first + 2 * dr, pos.second + 2 * dc});
            if (it != elves.end() && it->second != kDontMove) {
                auto [dr2, dc2] = kDirs[it->second];
                if (dr == -dr2 && dc == -dc2) {
                    next_elves[pos] = kDontMove;
                    continue;
                }
            }
            next_elves[{pos.first + dr, pos.second + dc}] = kDontMove;
            elf_moved = true;
        }

        elves.swap(next_elves);
        next_elves.clear();
        start_dir_index = (start_dir_index + 1) % 4;

        if (num_rounds == kPart1Round) {
            int min_r = INT32_MAX;
            int max_r = INT32_MIN;
            int min_c = INT32_MAX;
            int max_c = INT32_MIN;
            for (const auto& [pos, _] : elves) {
                min_r = min(min_r, pos.first);
                max_r = max(max_r, pos.first);
                min_c = min(min_c, pos.second);
                max_c = max(max_c, pos.second);
            }
            cout << (max_r - min_r + 1) * (max_c - min_c + 1) - elves.size() << "\n";
        }
    }

    cout << num_rounds << "\n";
}
