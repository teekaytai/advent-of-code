#include <iostream>
#include <regex>

/*
 * This improved solution is inspired by this Python solution:
 * https://www.reddit.com/r/adventofcode/comments/zmcn64/comment/j0b90nr/
 *
 * To address the mentioned edge case where the point to be found is at the edge of the area and
 * not at an intersection of sensor boundaries, additional boundaries can be added for x = 0,
 * x = 4000000, y = 0, and y = 4000000 and new intersections can be found.
 *
 * My previous solution runs in O(nklogk) time, where n is the size of the region (4000000) and
 * k is the number of sensors (30+). Since the region is huge, iterating through every row takes
 * a few seconds. This solution runs in O(k^3) time instead and finishes instantaneously.
 */

int dist(int x1, int y1, int x2, int y2) {
    return abs(x1 - x2) + abs(y1 - y2);
}

int main() {
    std::regex numbers_regex("\\d+");
    std::vector<std::pair<int, int>> sensors;
    std::vector<std::pair<int, int>> beacons;
    std::string line;
    while (getline(std::cin, line) && !line.empty()) {
        auto numbers_iterator = std::sregex_iterator(line.begin(), line.end(), numbers_regex);
        auto x = numbers_iterator->str();
        int sensor_x = stoi(numbers_iterator->str());
        ++numbers_iterator;
        int sensor_y = stoi(numbers_iterator->str());
        ++numbers_iterator;
        int beacon_x = stoi(numbers_iterator->str());
        ++numbers_iterator;
        int beacon_y = stoi(numbers_iterator->str());
        ++numbers_iterator;
        sensors.emplace_back(sensor_x, sensor_y);
        beacons.emplace_back(beacon_x, beacon_y);
    }

    int n = sensors.size();
    std::vector<int> ranges;
    std::vector<int> upward_boundaries; // store the y-intercepts of the lines that slope toward top right
    std::vector<int> downward_boundaries; // store the y-intercepts of the lines that slope toward bottom right
    for (int i = 0; i < n; ++i) {
        auto [sensor_x, sensor_y] = sensors[i];
        auto [beacon_x, beacon_y] = beacons[i];
        int range = dist(sensor_x, sensor_y, beacon_x, beacon_y);
        ranges.push_back(range);
        upward_boundaries.push_back(sensor_y + range + 1 - sensor_x);
        upward_boundaries.push_back(sensor_y - range - 1 - sensor_x);
        downward_boundaries.push_back(sensor_y + range + 1 + sensor_x);
        downward_boundaries.push_back(sensor_y - range - 1 + sensor_x);
    }

    int kMaxCoord = 4000000;
    int m = n * 2;
    for (int i = 0; i < m; ++i) {
        int c1 = upward_boundaries[i];
        for (int j = 0; j < m; ++j) {
            int c2 = downward_boundaries[j];
            // y = x + c1 = -x + c2  =>  x = (c2 - c1) / 2
            int diff = c2 - c1;
            if (diff % 2 != 0) {
                continue;
            }
            int x = diff / 2;
            int y = x + c1;
            if (x < 0 || x > kMaxCoord || y < 0 || y > kMaxCoord) {
                continue;
            }

            bool detected = false;
            for (int k = 0; k < n; ++k) {
                auto [sensor_x, sensor_y] = sensors[k];
                int range = ranges[k];
                if (dist(sensor_x, sensor_y, x, y) <= range) {
                    detected = true;
                    break;
                }
            }
            if (!detected) {
                long long tuning_frequency = (long long) x * kMaxCoord + y;
                std::cout << tuning_frequency << "\n";
                i = m;
                break;
            }
        }
    }
}
