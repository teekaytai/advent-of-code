#include <iostream>
#include <regex>
#include <unordered_set>

std::vector<std::pair<int, int>> merge_intervals(std::vector<std::pair<int, int>>& intervals) {
    std::sort(intervals.begin(), intervals.end());
    std::vector<std::pair<int, int>> merged_intervals;
    auto [curr_lo, curr_hi] = intervals[0];
    for (auto [lo, hi] : intervals) {
        if (lo <= curr_hi) {
            curr_hi = std::max(curr_hi, hi);
        } else {
            merged_intervals.emplace_back(curr_lo, curr_hi);
            curr_lo = lo;
            curr_hi = hi;
        }
    }
    merged_intervals.emplace_back(curr_lo, curr_hi);
    return merged_intervals;
}

/**
 * Given a list of sensors and their corresponding closest beacons,
 * return a list of intervals in row y that cannot contain beacons
 * (or already contain known beacons)
 */
std::vector<std::pair<int, int>> find_coverage(std::vector<std::pair<int, int>>& sensors,
                                               std::vector<std::pair<int, int>>& beacons,
                                               int y) {
    int n = sensors.size();
    std::vector<std::pair<int, int>> intervals;
    for (int i = 0; i < n; ++i) {
        auto [sensor_x, sensor_y] = sensors[i];
        auto [beacon_x, beacon_y] = beacons[i];
        int dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y);
        int dx = dist - abs(sensor_y - y);
        if (dx >= 0) {
            intervals.emplace_back(sensor_x - dx, sensor_x + dx);
        }
    }
    return merge_intervals(intervals);
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

    // Part 1
    const int kTargetY = 2000000;

    int total = 0;
    std::vector<std::pair<int, int>> intervals = find_coverage(sensors, beacons, kTargetY);
    for (auto [lo, hi] : intervals) {
        total += hi - lo + 1;
    }

    std::unordered_set<int> beacons_in_target_row;
    for (std::pair<int, int> beacon : beacons) {
        if (beacon.second == kTargetY) {
            beacons_in_target_row.insert(beacon.first);
        }
    }
    total -= beacons_in_target_row.size();

    std::cout << total << "\n";

    // Part 2
    const int kMaxCoord = 4000000;
    for (int y = 0; y <= kMaxCoord; ++y) {
        std::vector<std::pair<int, int>> covered_intervals = find_coverage(sensors, beacons, y);
        if (intervals.size() > 1) {
            // The single gap in the coverage is in this row
            int x = intervals[0].second + 1;
            long long tuning_frequency = (long long) x * kMaxCoord + y;
            std::cout << tuning_frequency << "\n";
            break;
        }
    }
}
