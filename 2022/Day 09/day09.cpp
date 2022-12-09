#include <iostream>
#include <unordered_map>
#include <unordered_set>

int sign(int x) {
    return (x > 0) - (x < 0);
}

struct IntPairHash {
    size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<long long>{}(((long long) p.first << 32) + p.second);
    }
};

int main() {
    std::unordered_map<char, std::pair<int, int>> directions =
            {{'U', {0, 1}}, {'R', {1, 0}}, {'D', {0, -1}}, {'L', {-1, 0}}};

    const int num_knots = 10; // Set to 2 for part 1
    std::pair<int, int> knot_positions[num_knots];
    std::unordered_set<std::pair<int, int>, IntPairHash> tail_positions;
    tail_positions.insert({0, 0});

    char dir;
    int steps;
    while (std::cin >> dir >> steps) {
        auto [dx, dy] = directions[dir];
        for (int i = 0; i < steps; ++i) {
            knot_positions[0].first += dx;
            knot_positions[0].second += dy;
            int j;
            for (j = 1; j < num_knots; ++j) {
                std::pair<int, int>& prev_knot = knot_positions[j - 1];
                std::pair<int, int>& curr_knot = knot_positions[j];
                int gap_x = prev_knot.first - curr_knot.first;
                int gap_y = prev_knot.second - curr_knot.second;
                if (abs(gap_x) > 1 || abs(gap_y) > 1) {
                    curr_knot.first += sign(gap_x);
                    curr_knot.second += sign(gap_y);
                } else {
                    // Current knot did not move, so the later knots will not either
                    break;
                }
            }
            if (j == num_knots) {
                // Tail moved. Add updated position to set
                tail_positions.insert(knot_positions[num_knots - 1]);
            }
        }
    }
    std::cout << tail_positions.size() << "\n";
}
