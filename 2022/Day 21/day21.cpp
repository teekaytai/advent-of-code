#include <iostream>
#include <unordered_map>
#include <vector>
#include <stack>

using namespace std;

int main() {
    const long long kInf = INT64_MAX;
    const string kLastMonkeyName = "root";

    unordered_map<string, int> monkey_ids;
    unordered_map<string, vector<string>> temp_adj_list;
    vector<pair<string, string>*> temp_req_list;
    vector<char> ops;
    vector<long long> numbers;
    stack<int> visited;
    string monkey_name;
    for (int id = 0; cin >> monkey_name; ++id) {
        monkey_name = monkey_name.substr(0, 4); // Remove colon
        monkey_ids.emplace(monkey_name, id);
        cin.ignore(); // Ignore space
        if (isdigit(cin.peek())) {
            int num;
            cin >> num;
            temp_req_list.push_back(nullptr);
            ops.push_back(0);
            numbers.push_back(num);
            visited.push(id);
        } else {
            string monkey_name1, monkey_name2;
            char op;
            cin >> monkey_name1 >> op >> monkey_name2;
            temp_adj_list[monkey_name1].push_back(monkey_name);
            temp_adj_list[monkey_name2].push_back(monkey_name);
            temp_req_list.push_back(new pair<string, string>{monkey_name1, monkey_name2});
            ops.push_back(op);
            numbers.push_back(kInf);
        }
    }
    int N = monkey_ids.size();

    // Translate to use int ids instead of strings
    vector<vector<int>> adj_list(N);
    for (const auto& [monkey_name1, adjs] : temp_adj_list) {
        int id = monkey_ids[monkey_name1];
        for (const string& monkey_name2 : adjs) {
            adj_list[id].push_back(monkey_ids[monkey_name2]);
        }
    }
    vector<pair<int, int>*> req_list;
    for (auto ptr : temp_req_list) {
        if (ptr == nullptr) {
            req_list.push_back(nullptr);
        } else {
            req_list.push_back(new pair<int, int>{monkey_ids[ptr->first], monkey_ids[ptr->second]});
        }
    }

    while (!visited.empty()) {
        int id = visited.top();
        visited.pop();
        for (int adj_id : adj_list[id]) {
            auto [id1, id2] = *req_list[adj_id];
            long long num1 = numbers[id1];
            long long num2 = numbers[id2];
            if (num1 == kInf || num2 == kInf) {
                continue;
            }
            long long res;
            switch (ops[adj_id]) {
                case '+':
                    res = num1 + num2;
                    break;
                case '-':
                    res = num1 - num2;
                    break;
                case '*':
                    res = num1 * num2;
                    break;
                case '/':
                    res = num1 / num2;
                    break;
            }
            numbers[adj_id] = res;
            visited.push(adj_id);
        }
    }

    int last_id = monkey_ids[kLastMonkeyName];
    cout << numbers[last_id] << "\n";
}
