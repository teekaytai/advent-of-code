#include <iostream>

int main() {
    char oppMove;
    char roundOutcome;
    int score = 0;
    while (std::cin >> oppMove) {
        std::cin >> roundOutcome;
        int myMoveId = (oppMove + roundOutcome + 2) % 3;
        // Score for shape
        score += myMoveId + 1;
        // Score for round outcome
        score += (roundOutcome - 1) % 3 * 3;
    }
    std::cout << score << "\n";

    /*
    // Part 1
    char oppMove;
    char myMove;
    int score = 0;
    while (std::cin >> oppMove) {
        std::cin >> myMove;
        int oppMoveId = (oppMove + 1) % 3;
        int myMoveId = (myMove + 2) % 3;
        // Score for shape
        score += myMoveId + 1;
        // Score for round outcome
        score += (myMoveId - oppMoveId + 4) % 3 * 3;
    }
    std::cout << score << "\n";
    */

    return 0;
}
