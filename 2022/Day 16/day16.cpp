#include <iostream>
#include <regex>
#include <unordered_map>
#include <unordered_set>

using namespace std;

/**
 * Returns the distances between the start node and the provided end nodes
 * as a vector of node, distance pairs.
 */
vector<pair<string, int>> bfs(const unordered_map<string, vector<string>>& adj_list,
                              const unordered_set<string>& ends, const string& start) {
    vector<pair<string, int>> dists;
    unordered_map<string, bool> visited;
    visited[start] = true;
    vector<string> nodes{start};
    vector<string> next_nodes;
    int steps = 1;
    while (!nodes.empty()) {
        for (const string& node : nodes) {
            for (const string& adj_node : adj_list.at(node)) {
                if (visited[adj_node]) {
                    continue;
                }
                visited[adj_node] = true;
                if (ends.contains(adj_node)) {
                    dists.emplace_back(adj_node, steps);
                }
                next_nodes.push_back(adj_node);
            }
        }
        swap(nodes, next_nodes);
        next_nodes.clear();
        ++steps;
    }
    return dists;
}

/**
 * Updates the max_pressures vector such that index i contains the maximum
 * total pressure that can be released while opening the corresponding set of valves.
 * Given an index i, the corresponding set of valves is given by the set bits in i.
 * For example, at index 11 (0b1011), the maximum pressure that can be released while
 * opening valves 0, 1 and 3 will be stored.
 * If the exact set of valves cannot be opened, the value is not updated.
 */
void dfs(const unordered_map<int, vector<pair<int, int>>>& adj_list,
         const vector<int>& flow_rates, vector<int>& max_pressures, int total_pressure,
         int valves_open, int total_flow_rate, int curr_node, int steps_left) {
    max_pressures[valves_open] = max(max_pressures[valves_open], total_pressure + total_flow_rate * steps_left);
    for (auto [adj_node, dist] : adj_list.at(curr_node)) {
        int valve_bit = 1 << adj_node;
        if (valves_open & valve_bit || steps_left <= dist) {
            // Valve already opened or too far away to reach in time
            continue;
        }
        int steps_needed = dist + 1; // One more step to open the valve after moving there
        int new_total_pressure = total_pressure + total_flow_rate * steps_needed;
        int new_valves_open = valves_open | valve_bit;
        int new_flow_rate = total_flow_rate + flow_rates.at(adj_node);
        dfs(adj_list, flow_rates, max_pressures, new_total_pressure, new_valves_open,
            new_flow_rate, adj_node, steps_left - steps_needed);
    }
}

int main() {
    const string kStartValve = "AA";

    unordered_map<string, vector<string>> adj_list;
    unordered_set<string> valves_with_flow;
    unordered_map<string, int> valve_flow_rates;
    regex number_regex("\\d+");
    regex valves_regex("[A-Z]{2}");
    auto valves_end = sregex_iterator();
    string line;
    while (getline(cin, line) && !line.empty()) {
        auto valves_iterator = sregex_iterator(line.begin(), line.end(), valves_regex);
        string valve = valves_iterator->str();
        ++valves_iterator;
        while (valves_iterator != valves_end) {
            adj_list[valve].push_back(valves_iterator->str());
            ++valves_iterator;
        }
        smatch number_match;
        regex_search(line, number_match, number_regex);
        int flow = stoi(number_match[0]);
        if (flow > 0) {
            valves_with_flow.insert(valve);
            valve_flow_rates[valve] = flow;
        }
    }

    // Transform graph to only include valves with positive flow rate and have weighted edges between them.
    // Also give each valve a number id
    int num_valves = valves_with_flow.size();
    unordered_map<string, int> valve_to_id;
    for (const string& valve : valves_with_flow) {
        valve_to_id[valve] = valve_to_id.size();
    }
    unordered_map<int, vector<pair<int, int>>> condensed_adj_list; // vertex -> {adj_vertex, edge_weight}
    for (const string& valve : valves_with_flow) {
        int valve_id = valve_to_id[valve];
        for (auto [other_valve, dist] : bfs(adj_list, valves_with_flow, valve)) {
            condensed_adj_list[valve_id].emplace_back(valve_to_id[other_valve], dist);
        }
    }
    vector<int> flow_rates(num_valves);
    for (auto [valve, flow] : valve_flow_rates) {
        flow_rates[valve_to_id[valve]] = flow;
    }

    // The first move will be from the start node to one of the valves
    vector<pair<string, int>> possible_starts = bfs(adj_list, valves_with_flow, kStartValve);


    // Part 1
    const int kMaxSteps1 = 30;
    vector<int> max_pressures1(1 << num_valves, 0);
    for (auto [valve, dist] : possible_starts) {
        int id = valve_to_id[valve];
        dfs(condensed_adj_list, flow_rates, max_pressures1, 0, 1 << id,
            valve_flow_rates[valve], id, kMaxSteps1 - dist - 1);
    }
    cout << *max_element(max_pressures1.begin(), max_pressures1.end()) << "\n";


    // Part 2
    const int kMaxSteps2 = 26;
    int N = 1 << num_valves;
    vector<int> max_pressures2(N, 0);
    for (auto [valve, dist] : possible_starts) {
        int id = valve_to_id[valve];
        dfs(condensed_adj_list, flow_rates, max_pressures2, 0, 1 << id,
            valve_flow_rates[valve], id, kMaxSteps2 - dist - 1);
    }

    // Currently max_pressures requires the exact set of valves that corresponds to the index to be opened.
    // This procedure updates it such that each position stores the max pressure attainable using any subset
    // of the corresponding valves.
    for (int num_open_valves = 1; num_open_valves < num_valves; ++num_open_valves) {
        int p = (1 << num_open_valves) - 1;
        while (p < N) {
            for (int bit = 1; bit < N; bit <<= 1) {
                // Consider set with one more valve
                int q = p | bit;
                max_pressures2[q] = max(max_pressures2[q], max_pressures2[p]);
            }
            // Compute the lexicographically next bit permutation with num_open_valves set bits.
            // Credit: http://graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation
            int t = (p | (p - 1)) + 1;
            p = t | ((((t & -t) / (p & -p)) >> 1) - 1);
        }
    }

    // Consider every partition of the valves into two sets.
    // Calculate the total pressure that can be released if I work on one set and
    // the elephant works on the other
    int max_total_pressure = 0;
    for (int i = 0, j = N - 1; i < N; ++i, --j) {
        max_total_pressure = max(max_total_pressure, max_pressures2[i] + max_pressures2[j]);
    }
    cout << max_total_pressure << "\n";
}
