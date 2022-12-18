#include <iostream>
#include <stack>
#include <unordered_set>

using namespace std;

struct IntTupleHash {
    size_t operator()(const tuple<int, int, int>& t) const {
        size_t h = hash<int>{}(get<0>(t));
        h = hash<int>{}(get<1>(t)) + 0x9e3779b9 + (h << 6) + (h >> 2);
        h = hash<int>{}(get<2>(t)) + 0x9e3779b9 + (h << 6) + (h >> 2);
        return h;
    }
};

int main() {
    tuple<int, int, int> kDirs[] = {{-1, 0 ,0}, {1, 0, 0}, {0, -1, 0}, {0, 1, 0}, {0, 0, -1}, {0, 0, 1}};

    unordered_set<tuple<int, int, int>, IntTupleHash> cubes;
    char ignored;
    int x, y, z;
    int min_x = INT32_MAX;
    int max_x = INT32_MIN;
    int min_y = INT32_MAX;
    int max_y = INT32_MIN;
    int min_z = INT32_MAX;
    int max_z = INT32_MIN;
    int total_sides = 0; // Part 1
    while (cin >> x >> ignored >> y >> ignored >> z) {
        total_sides += 6;
        for (const auto [dx, dy, dz] : kDirs) {
            int x2 = x + dx;
            int y2 = y + dy;
            int z2 = z + dz;
            if (cubes.contains({x2, y2, z2})) {
                total_sides -= 2;
            }
        }
        cubes.emplace(x, y, z);
        min_x = min(min_x, x);
        max_x = max(max_x, x);
        min_y = min(min_y, y);
        max_y = max(max_y, y);
        min_z = min(min_z, z);
        max_z = max(max_z, z);
    }
    cout << total_sides << "\n";

    // Part 2
    --min_x, ++max_x;
    --min_y, ++max_y;
    --min_z, ++max_z;
    int total_exposed_sides = 0;
    stack<tuple<int, int, int>> st;
    unordered_set<tuple<int, int, int>, IntTupleHash> visited;
    st.emplace(min_x, min_y, min_z);
    visited.emplace(min_x, min_y, min_z);
    while (!st.empty()) {
        auto [x1, y1, z1] = st.top();
        st.pop();
        for (const auto [dx, dy, dz] : kDirs) {
            int x2 = x1 + dx;
            int y2 = y1 + dy;
            int z2 = z1 + dz;
            if (x2 < min_x || x2 > max_x || y2 < min_y || y2 > max_y || z2 < min_z || z2 > max_z) {
                continue;
            }
            if (visited.contains({x2, y2, z2})) {
                continue;
            }
            if (cubes.contains({x2, y2, z2})) {
                ++total_exposed_sides;
            } else {
                st.emplace(x2, y2, z2);
                visited.emplace(x2, y2, z2);
            }
        }
    }
    cout << total_exposed_sides << "\n";
}
