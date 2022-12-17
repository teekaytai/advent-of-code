#include <deque>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <stack>
#include <vector>

using namespace std;

struct IntPairHash {
    size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<long long>{}(((long long) p.first << 32) + p.second);
    }
};

class Board {
  public:
    [[nodiscard]] long long total_height() const {
        return total_height_;
    }

    void add_total_height(long long h) {
        total_height_ += h;
    }

    [[nodiscard]] int height() const {
        return height_;
    }

    [[nodiscard]] bool IsBlocked(int x, int y) const {
        if (x < 0 || x >= kBoardWidth || y < 0) {
            return true;
        }
        if (y >= height_) {
            return false;
        }
        return grid_[x][y];
    }

    void AddShape(const vector<pair<int, int>>& shape_spaces, int x, int y) {
        for (const auto& [dx, dy] : shape_spaces) {
            int y2 = y + dy;
            while (height_ <= y2) {
                for (deque<bool>& column : grid_) {
                    column.push_back(false);
                }
                ++total_height_;
                ++height_;
            }

            grid_[x + dx][y2] = true;
        }

        // Part of grid_ at the bottom blocked by shapes cannot be reached.
        // Can safely pop rows below.
        int height_drop = MinReachableHeight();
        if (height_drop > 0) {
            height_ -= height_drop;
            for (deque<bool>& column : grid_) {
                column.erase(column.begin(), column.begin() + height_drop);
            }
        }
    }

    bool operator==(const Board& other) const {
        if (height_ != other.height_) {
            return false;
        }
        for (int i = 0; i < kBoardWidth; ++i) {
            for (int j = 0; j < height_; ++j) {
                if (grid_[i][j] != other.grid_[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

  private:
    friend struct BoardHash;
    constexpr static pair<int, int> kDirs[4] = {{0, 1}, {-1, 0}, {1, 0}, {0, -1}};
    constexpr static int kBoardWidth = 7;

    /**
     * Returns the lowest height that a new shape could potentially reach
     * falling down from above.
     */
    [[nodiscard]] int MinReachableHeight() const {
        int min_height = height_;
        stack<pair<int, int>> cell_stack;
        unordered_set<pair<int, int>, IntPairHash> visited;
        for (int i = 0; i < kBoardWidth; ++i) {
            if (!grid_[i][height_ - 1]) {
                cell_stack.emplace(i, height_ - 1);
                visited.emplace(i, height_ - 1);
                min_height = height_ - 1;
            }
        }

        while (!cell_stack.empty()) {
            auto [x, y] = cell_stack.top();
            cell_stack.pop();
            for (auto [dx, dy] : kDirs) {
                int x2 = x + dx;
                int y2 = y + dy;
                if (x2 < 0 || x2 >= kBoardWidth || y2 < 0 || y2 >= height_ || grid_[x2][y2]) {
                    continue;
                }
                if (visited.contains({x2, y2})) {
                    continue;
                }
                cell_stack.emplace(x2, y2);
                visited.emplace(x2, y2);
                min_height = min(min_height, y2);
            }
        }
        return min_height;
    }

    long long total_height_ = 0;
    int height_ = 0; // The apparent height of the shape stack ignoring unreachable portion at bottom
    deque<bool> grid_[kBoardWidth];
};

struct BoardHash {
    size_t operator()(const Board& board) const {
        size_t h1 = board.height_;
        for (const deque<bool>& column : board.grid_) {
            size_t h2 = column.size();
            for (bool b : column) {
                h2 = h2 * 101 + b;
            }
            h1 ^= h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2);
        }
        return h1;
    }
};

class Shape {
  public:
    explicit Shape(Board& board, const vector<pair<int, int>>& cells_occupied)
        : board_(board),
          kCellsOccupied_(cells_occupied) {
        x_ = kSpawnXOffset;
        y_ = board_.height() + kSpawnYOffset;
    }

    void MoveLeft() {
        for (const auto& [dx, dy] : kCellsOccupied_) {
            if (board_.IsBlocked(x_ + dx - 1, y_ + dy)) {
                return;
            }
        }
        --x_;
    }

    void MoveRight() {
        for (const auto& [dx, dy] : kCellsOccupied_) {
            if (board_.IsBlocked(x_ + dx + 1, y_ + dy)) {
                return;
            }
        }
        ++x_;
    }

    /**
     * Attempts to move this shape down a step.
     * If the shape has been blocked, adds the shape to the board
     * and returns true.
     */
    bool MoveDown() {
        for (const auto& [dx, dy] : kCellsOccupied_) {
            if (board_.IsBlocked(x_ + dx, y_ + dy - 1)) {
                board_.AddShape(kCellsOccupied_, x_, y_);
                return true;
            }
        }
        --y_;
        return false;
    }

  private:
    constexpr static int kSpawnXOffset = 2;
    constexpr static int kSpawnYOffset = 3;

    Board& board_;
    const vector<pair<int, int>>& kCellsOccupied_;
    // Coordinates refer to the bottom left corner of the shape.
    // This cell may be outside the shape itself for concave shapes
    int x_, y_;
};

// A state consists of the movement index and the Board
typedef pair<int, Board> State;

struct StateHash {
    BoardHash board_hash;
    size_t operator()(const State& state) const {
        return board_hash(state.second) ^ hash<int>{}(state.first);
    }
};

int main() {
    const long long kNumShapesDropped = 1000000000000; // Set to 2022 for part 1
    const int kNumShapeTypes = 5;
    const vector<pair<int, int>> kShapeCells[kNumShapeTypes]{
        {{0, 0}, {1, 0}, {2, 0}, {3, 0}},
        {{1, 0}, {0, 1}, {1, 1}, {2, 1}, {1, 2}},
        {{0, 0}, {1, 0}, {2, 0}, {2, 1}, {2, 2}},
        {{0, 0}, {0, 1}, {0, 2}, {0, 3}},
        {{0, 0}, {1, 0}, {0, 1}, {1, 1}}
    };

    string move_sequence;
    cin >> move_sequence;
    int move_index = 0;

    Board board;
    bool cache_hit = false;
    // Map a state to the number of shapes dropped so far to calculate cycle length
    unordered_map<State, long long, StateHash> states_cache;
    for (long long i = 0; i < kNumShapesDropped; ++i) {
        if (!cache_hit && i % kNumShapeTypes == 0) {
            State state = {move_index, board};
            auto it = states_cache.find(state);
            if (it != states_cache.end()) {
                cache_hit = true;
                long long cycle_length = i - it->second;
                long long height_change = board.total_height() - it->first.second.total_height();
                long long num_cycles = (kNumShapesDropped - i - 1) / cycle_length;
                i += num_cycles * cycle_length;
                board.add_total_height(num_cycles * height_change);
            } else {
                states_cache[state] = i;
            }
        }

        Shape shape(board, kShapeCells[i % kNumShapeTypes]);
        bool shape_stopped = false;
        while (!shape_stopped) {
            move_sequence[move_index] == '<' ? shape.MoveLeft() : shape.MoveRight();
            move_index = (move_index + 1) % move_sequence.size();
            shape_stopped = shape.MoveDown();
        }
    }

    cout << board.total_height() << "\n";
}
