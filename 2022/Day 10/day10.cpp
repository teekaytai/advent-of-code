#include <iostream>

int main() {
    int totalSignal = 0;
    int reg = 1;
    int value;
    std::string instruction;
    std::cin >> instruction;
    for (int i = 1; i <= 240; ++i) {
        // Part 1
        if ((i - 20) % 40 == 0) {
            totalSignal += i * reg;
        }

        // Part 2
        std::cout << (abs((i - 1) % 40 - reg) <= 1 ? "#" : ".");
        if (i % 40 == 0) {
            std::cout << "\n";
        }

        if (instruction == "addx") {
            instruction = "addx2";
        } else if (instruction == "addx2") {
            std::cin >> value;
            reg += value;
            std::cin >> instruction;
        } else { // noop
            std::cin >> instruction;
        }
    }
    std::cout << totalSignal << "\n";
}
