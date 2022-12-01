#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> totals;
    int total;
    while (!std::cin.eof()) {
        std::string line;
        getline(std::cin, line);
        if (line.empty()) {
            totals.push_back(total);
            total = 0;
        } else {
            total += stoi(line);
        }
    }
    sort(totals.begin(), totals.end(), std::greater<>());
    std::cout << totals[0] + totals[1] + totals[2] << '\n';
    return 0;
}
