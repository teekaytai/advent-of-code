#include <iostream>
#include <vector>

using namespace std;

void cross_edge(int& face, int& r, int& c, int& dir_index) {
    constexpr static int kFaceSize = 50;
    constexpr static pair<int, int> kTransitions[6][4]{
        {{1, 0}, {2, 1}, {3, 0}, {5, 0}},
        {{4, 2}, {2, 2}, {0, 2}, {5, 3}},
        {{1, 3}, {4, 1}, {3, 1}, {0, 3}},
        {{4, 0}, {5, 1}, {0, 0}, {2, 0}},
        {{1, 2}, {5, 2}, {3, 2}, {2, 3}},
        {{4, 3}, {1, 1}, {0, 1}, {3, 3}},
    };

    auto [new_face, new_dir_index] = kTransitions[face][dir_index];
    int temp;
    int new_r, new_c;
    switch (dir_index) {
        case 0:
            temp = r;
            break;
        case 1:
            temp = kFaceSize - c - 1;
            break;
        case 2:
            temp = kFaceSize - r - 1;
            break;
        case 3:
            temp = c;
            break;
    }
    switch (new_dir_index) {
        case 0:
            new_r = temp;
            new_c = 0;
            break;
        case 1:
            new_r = 0;
            new_c = kFaceSize - temp - 1;
            break;
        case 2:
            new_r = kFaceSize - temp - 1;
            new_c = kFaceSize - 1;
            break;
        case 3:
            new_r = kFaceSize - 1;
            new_c = temp;
            break;
    }

    face = new_face;
    r = new_r;
    c = new_c;
    dir_index = new_dir_index;
}

int main() {
    constexpr int kFaceSize = 50;
    constexpr pair<int, int> kDirs[4]{{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    constexpr pair<int, int> kFacePositions[6]{{0, 50}, {0, 100}, {50, 50}, {100, 0}, {100, 50}, {150, 0}};

    vector<string> board;
    string row;
    for (int r = 0; getline(cin, row) && !row.empty(); ++r) {
        board.push_back(row);
    }

    int curr_face = 0;
    int curr_r = 0;
    int curr_c = 0;
    int curr_dir_index = 0;
    int steps;
    char rotation;
    while (cin >> steps) {
        for (int i = 0; i < steps; ++i) {
            auto [dr, dc] = kDirs[curr_dir_index];
            int new_face = curr_face;
            int new_r = curr_r + dr;
            int new_c = curr_c + dc;
            int new_dir_index = curr_dir_index;
            if (new_r < 0 || new_r >= kFaceSize || new_c < 0 || new_c >= kFaceSize) {
                new_r -= dr;
                new_c -= dc;
                cross_edge(new_face, new_r, new_c, new_dir_index);
            }
            int real_r = kFacePositions[new_face].first + new_r;
            int real_c = kFacePositions[new_face].second + new_c;
            if (board[real_r][real_c] == '#') {
                break;
            }
            curr_face = new_face;
            curr_r = new_r;
            curr_c = new_c;
            curr_dir_index = new_dir_index;
        }

        if (cin >> rotation) {
            curr_dir_index += rotation == 'R' ? 1 : 3;
            curr_dir_index %= 4;
        }
    }

    int final_real_r = kFacePositions[curr_face].first + curr_r;
    int final_real_c = kFacePositions[curr_face].second + curr_c;
    cout << 1000 * (final_real_r + 1) + 4 * (final_real_c + 1) + curr_dir_index << "\n";
}
