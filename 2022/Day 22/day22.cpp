#include <iostream>
#include <vector>

using namespace std;

int main() {
    const pair<int, int> kDirs[4]{{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

    vector<string> board;
    vector<int> boundaries[4]; // Contains row/cols of positions you'd be at if you walked off board in each dir
    string row;
    for (int r = 0; getline(cin, row) && !row.empty(); ++r) {
        board.push_back(row);
        if (row.size() > boundaries[1].size()) {
            boundaries[1].resize(row.size(), -1);
            boundaries[3].resize(row.size(), -1);
        }
        int leftmost = -1;
        int rightmost;
        for (int c = 0; c < row.size(); ++c) {
            if (row[c] == ' ') {
                continue;
            }
            if (leftmost == -1) {
                leftmost = c;
            }
            if (boundaries[1][c] == -1) {
                boundaries[1][c] = r;
            }
            rightmost = c;
            boundaries[3][c] = r;
        }
        boundaries[0].push_back(leftmost);
        boundaries[2].push_back(rightmost);
    }

    int curr_r = 0;
    int curr_c = boundaries[0][0];
    int dir_index = 0;
    int steps;
    char rotation;
    while (cin >> steps) {
        auto [dr, dc] = kDirs[dir_index];
        for (int i = 0; i < steps; ++i) {
            int new_r = curr_r + dr;
            int new_c = curr_c + dc;
            if (dir_index % 2 == 0) {
                if (new_c < 0 || new_c >= board[new_r].size() || board[new_r][new_c] == ' ') {
                    new_c = boundaries[dir_index][new_r];
                }
            } else {
                if (new_r < 0 || new_r >= board.size() || new_c >= board[new_r].size() || board[new_r][new_c] == ' ') {
                    new_r = boundaries[dir_index][new_c];
                }
            }
            if (board[new_r][new_c] == '#') {
                break;
            }
            curr_r = new_r;
            curr_c = new_c;
        }

        if (cin >> rotation) {
            dir_index += rotation == 'R' ? 1 : 3;
            dir_index %= 4;
        }
    }
    cout << 1000 * (curr_r + 1) + 4 * (curr_c + 1) + dir_index << "\n";
}
