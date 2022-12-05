#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> crateRows;
    std::string line;
    getline(std::cin, line);
    while (line[0] != ' ') {
        crateRows.push_back(line);
        getline(std::cin, line);
    }
    const int NUM_STACKS = 9;
    std::vector<char> crateStacks[NUM_STACKS];
    for (auto it = crateRows.rbegin(); it != crateRows.rend(); ++it) {
        std::string row = *it;
        for (size_t i = 1; i < row.length(); i += 4) {
            if (row[i] != ' ') {
                crateStacks[i / 4].push_back(row[i]);
            }
        }
    }

    std::cin.ignore();
    std::string ignoredWord;
    int numCrates, fromStackId, toStackId;
    while (std::cin >> ignoredWord >> numCrates >> ignoredWord >> fromStackId >> ignoredWord >> toStackId) {
        std::vector<char> &fromStack = crateStacks[fromStackId - 1];
        std::vector<char> &toStack = crateStacks[toStackId - 1];
        // Part 1
        // toStack.insert(toStack.end(), fromStack.rbegin(), fromStack.rbegin() + numCrates);
        // Part 2
        toStack.insert(toStack.end(), fromStack.end() - numCrates, fromStack.end());
        fromStack.resize(fromStack.size() - numCrates);
    }

    for (std::vector<char> crateStack : crateStacks) {
        std::cout << crateStack.back();
    }
    std::cout << "\n";
    return 0;
}
