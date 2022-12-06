#include <iostream>
#include <queue>

int main() {
    const int MARKER_LENGTH = 14; // Set to 4 for part 1
    std::queue<char> queue;
    int counts[26] = {0};
    int correctCount = 0;
    char c;
    for (int i = 0; i < MARKER_LENGTH; ++i) {
        std::cin >> c;
        queue.push(c);
        int id = c - 'a';
        if (++counts[id] == 1) {
            ++correctCount;
        } else if (counts[id] == 2) {
            --correctCount;
        }
    }
    int charIndex = MARKER_LENGTH;
    while (correctCount < MARKER_LENGTH) {
        std::cin >> c;
        int addedId = c - 'a';
        if (++counts[addedId] == 1) {
            ++correctCount;
        } else if (counts[addedId] == 2) {
            --correctCount;
        }
        queue.push(c);

        int removedId = queue.front() - 'a';
        if (--counts[removedId] == 1) {
            ++correctCount;
        } else if (counts[removedId] == 0) {
            --correctCount;
        }
        queue.pop();
        ++charIndex;
    }
    std::cout << charIndex << "\n";
}
