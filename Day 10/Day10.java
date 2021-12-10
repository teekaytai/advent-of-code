import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
import java.util.Stack;

public class Day10 {
    static final String OPEN_BRACKETS = "([{<";
    static final String CLOSE_BRACKETS = ")]}>";
    // static final int[] BRACKET_SCORES = {3, 57, 1197, 25137};  // Part 1

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Stack<Character> openBrackets = new Stack<>();
        // int totalScore = 0;  // Part 1
        ArrayList<Long> scores = new ArrayList<>();  // Part 2

        while (sc.hasNext()) {
            char[] brackets = sc.nextLine().toCharArray();
            boolean isCorrupted = false;  // Part 2
            for (char bracket : brackets) {
                if (OPEN_BRACKETS.indexOf(bracket) != -1) {
                    openBrackets.push(bracket);
                } else {
                    char openBracket = openBrackets.pop();
                    int bracketIndex = CLOSE_BRACKETS.indexOf(bracket);
                    if (OPEN_BRACKETS.charAt(bracketIndex) != openBracket) {
                        // totalScore += BRACKET_SCORES[bracketIndex];  // Part 1
                        isCorrupted = true;  // Part 2
                        break;
                    }
                }
            }

            // Part 2
            if (isCorrupted) {
                openBrackets.clear();
            } else {
                long score = 0;
                while (!openBrackets.empty()) {
                    score *= 5;
                    score += OPEN_BRACKETS.indexOf(openBrackets.pop()) + 1;
                }
                scores.add(score);
            }
        }

        // System.out.println(totalScore);  // Part 1

        // Part 2
        Collections.sort(scores);
        System.out.println(scores.get(scores.size() / 2));
    }
}
