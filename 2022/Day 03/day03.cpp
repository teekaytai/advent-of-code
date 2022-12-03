#include <iostream>
#include <unordered_set>

// Part 2
int main() {
    std::string rucksack1;
    std::string rucksack2;
    std::string rucksack3;
    int totalPriority = 0;
    while (std::cin >> rucksack1) {
        std::cin >> rucksack2;
        std::cin >> rucksack3;
        std::unordered_set<char> items1;
        std::unordered_set<char> items1and2;
        for (char item : rucksack1) {
            items1.insert(item);
        }
        for (char item : rucksack2) {
            if (items1.find(item) != items1.end()) {
                items1and2.insert(item);
            }
        }
        for (char item : rucksack3) {
            if (items1and2.find(item) != items1and2.end()) {
                totalPriority += item <= 'Z' ? item - 'A' + 27 : item - 'a' + 1;
                break;
            }
        }
    }
    std::cout << totalPriority << '\n';
    return 0;
}


// Part 1
int main1() {
    std::string rucksack;
    int totalPriority = 0;
    while (std::cin >> rucksack) {
        size_t halfLen = rucksack.length() / 2;
        std::unordered_set<char> firstHalfItems;
        for (size_t i = 0; i < halfLen; i++) {
            firstHalfItems.insert(rucksack[i]);
        }
        for (size_t i = halfLen; i < rucksack.length(); i++) {
            char item = rucksack[i];
            if (firstHalfItems.find(item) != firstHalfItems.end()) {
                totalPriority += item <= 'Z' ? item - 'A' + 27 : item - 'a' + 1;
                break;
            }
        }
    }
    std::cout << totalPriority << '\n';
    return 0;
}
