#include <array>
#include <iostream>
#include <regex>

using namespace std;

int ceildiv(int dividend, int divisor) {
    return (dividend + divisor - 1) / divisor;
}

void find_max_geodes(const array<array<int, 3>, 4>& costs, const array<int, 4>& max_bots,
                     array<int, 4>& bots, array<int, 4>& minerals, int turns, int& alpha) {
    static array<int, 4> temp_bots;
    static array<int, 4> temp_minerals;

    // Prune this branch if it cannot possibly generate more geodes than previously seen.
    // To get an easy-to-compute upper bound, these assumptions were made:
    // - Assume every type of robot can be built each turn (at most one of each type)
    // - Assume every bot only requires the previous mineral to build.
    // - Assume that an ore bot can be built every turn for free
    temp_bots = bots;
    temp_minerals = minerals;
    for (int i = 0; i < turns; ++i) {
        for (int j = minerals.size() - 1; j > 0; --j) {
            temp_minerals[j] += temp_bots[j];
            if (temp_minerals[j - 1] >= costs[j][j - 1]) {
                ++temp_bots[j];
                temp_minerals[j - 1] -= costs[j][j - 1];
            }
        }
        temp_minerals[0] += temp_bots[0];
        ++temp_bots[0];
    }
    if (temp_minerals.back() <= alpha) {
        return;
    }

    // Result if no more bots built for the remaining turns
    alpha = max(alpha, minerals.back() + bots.back() * turns);

    // Consider which type of bot to build next (as opposed to using turns as a time step which would be slower)
    for (int i = bots.size() - 1; i >= 0; --i) {
        if (bots[i] >= max_bots[i]) {
            continue;
        }

        int turns_to_wait = 0;
        for (int j = 0; j < costs[i].size(); ++j) {
            if (costs[i][j] == 0) {
                continue;
            }
            if (bots[j] == 0) {
                // No bot harvesting required mineral, impossible to build this type of bot next
                turns_to_wait = turns;
                break;
            } else {
                turns_to_wait = max(turns_to_wait, ceildiv(costs[i][j] - minerals[j], bots[j]));
            }
        }
        ++turns_to_wait; // One turn to build bot
        if (turns_to_wait >= turns) {
            continue;
        }

        for (int j = 0; j < bots.size(); ++j) {
            minerals[j] += bots[j] * turns_to_wait;
        }
        for (int j = 0; j < costs[i].size(); ++j) {
            minerals[j] -= costs[i][j];
        }
        ++bots[i];

        find_max_geodes(costs, max_bots, bots, minerals, turns - turns_to_wait, alpha);

        // Backtrack
        --bots[i];
        for (int j = 0; j < costs[i].size(); ++j) {
            minerals[j] += costs[i][j];
        }
        for (int j = 0; j < bots.size(); ++j) {
            minerals[j] -= bots[j] * turns_to_wait;
        }
    }
}

int main() {
    const int kMaxBlueprints = 3; // Set to INT32_MAX for part 1
    const int kMaxTurns = 32; // Set to 24 for part 1

    int result = 1; // Start with 0 for part 1
    array<array<int, 3>, 4> costs{0};
    array<int, 4> bots{1};
    array<int, 4> minerals{0};
    regex number_regex("\\d+");
    string line;
    for (int i = 1; i <= kMaxBlueprints && getline(cin, line); ++i) {
        auto nums_iterator = sregex_iterator(line.begin(), line.end(), number_regex);
        costs[0][0] = stoi((++nums_iterator)->str());
        costs[1][0] = stoi((++nums_iterator)->str());
        costs[2][0] = stoi((++nums_iterator)->str());
        costs[2][1] = stoi((++nums_iterator)->str());
        costs[3][0] = stoi((++nums_iterator)->str());
        costs[3][2] = stoi((++nums_iterator)->str());

        // Build as many geode bots as desired.
        // For other bots, no reason to harvest mineral faster than you can spend it
        array<int, 4> max_bots{0, 0, 0, INT32_MAX};
        for (const auto& mineral_costs : costs) {
            for (int k = 0; k < mineral_costs.size(); ++k) {
                max_bots[k] = max(max_bots[k], mineral_costs[k]);
            }
        }

        int max_possible_geodes = 0;
        find_max_geodes(costs, max_bots, bots, minerals, kMaxTurns, max_possible_geodes);
        // result += i * max_possible_geodes; // Part 1
        result *= max_possible_geodes; // Part 2
    }
    cout << result << "\n";
}
