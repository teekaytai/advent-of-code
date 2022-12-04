#include <iostream>

int main() {
    int totalInclusions = 0; // Part 1
    int totalOverlaps = 0; // Part 2
    int l1, r1, l2, r2;
    while (std::cin >> l1) {
        std::cin.ignore();
        std::cin >> r1;
        std::cin.ignore();
        std::cin >> l2;
        std::cin.ignore();
        std::cin >> r2;
        std::cin.ignore();
        totalInclusions += l1 <= l2 && r1 >= r2 || l1 >= l2 && r1 <= r2;
        totalOverlaps += l1 <= r2 && r1 >= l2;
    }
    std::cout << totalInclusions << "\n";
    std::cout << totalOverlaps << "\n";
    return 0;
}
