import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Day8 {
    public static void part1() {
        Scanner sc = new Scanner(System.in);
        int total = 0;

        while (sc.hasNext()) {
            String outSignals = sc.nextLine().split(" \\| ")[1];
            total += Arrays.stream(outSignals.split(" ")).filter(v -> {
                int L = v.length();
                return L == 2 || L == 3 || L == 4 || L == 7;
            }).count();
        }

        System.out.println(total);
    }

    public static class Segments {
        // These 4 segments are the only ones I will identify and use
        private char topLeftSeg;  // Appears 6 times
        private char topRightSeg;  // Appears 8 times AND in the pattern for one
        private char bottomLeftSeg;  // Appears 4 times
        private char bottomRightSeg;  // Appears 9 times

        HashMap<Character, Integer> segCounts = new HashMap<>();

        public Segments(String[] patterns) {
            String onePattern = "";
            for (String pattern : patterns) {
                if (pattern.length() == 2) {
                    onePattern = pattern;
                }
                for (int i = 0, L = pattern.length(); i < L; i++) {
                    segCounts.merge(pattern.charAt(i), 1, Integer::sum);  // Increment count
                }
            }

            for (Map.Entry<Character, Integer> entry : segCounts.entrySet()) {
                char seg = entry.getKey();
                int count = entry.getValue();
                if (count == 6) {
                    topLeftSeg = seg;
                } else if (count == 4) {
                    bottomLeftSeg = seg;
                } else if (count == 9) {
                    bottomRightSeg = seg;
                } else if (count == 8 && onePattern.indexOf(seg) != -1) {
                    topRightSeg = seg;
                }
            }
        }

        public String identifyDigit(String pattern) {
            return switch (pattern.length()) {
                case 2 -> "1";
                case 3 -> "7";
                case 4 -> "4";
                case 7 -> "8";
                case 5 -> pattern.indexOf(bottomRightSeg) == -1
                        ? "2"
                        : pattern.indexOf(topLeftSeg) == -1
                        ? "3"
                        : "5";
                // length 6
                default -> pattern.indexOf(bottomLeftSeg) == -1
                        ? "9"
                        : pattern.indexOf(topRightSeg) == -1
                        ? "6"
                        : "0";
            };
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int total = 0;

        while (sc.hasNext()) {
            String[] line = sc.nextLine().split(" \\| ");
            Segments segments = new Segments(line[0].split(" "));
            String[] outSignals = line[1].split(" ");
            String output = Arrays.stream(outSignals).map(segments::identifyDigit).collect(Collectors.joining());
            total += Integer.parseInt(output);
        }

        System.out.println(total);
    }
}
