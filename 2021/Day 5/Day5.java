import java.util.Arrays;
import java.util.Scanner;

public class Day5 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int[][] counts = new int[1000][1000];

        while (sc.hasNext()) {
            String[] input = sc.nextLine().split(",| -> ");
            int[] interval = Arrays.stream(input).mapToInt(Integer::parseInt).toArray();
            int x1, y1, x2, y2;
            // Ensure x1 <= x2
            if (interval[0] <= interval[2]) {
                x1 = interval[0];
                y1 = interval[1];
                x2 = interval[2];
                y2 = interval[3];
            } else {
                x1 = interval[2];
                y1 = interval[3];
                x2 = interval[0];
                y2 = interval[1];
            }

            if (x1 == x2) {
                if (y1 > y2) {
                    int temp = y1;
                    y1 = y2;
                    y2 = temp;
                }
                for (int y = y1; y <= y2; y++) {
                    counts[y][x1]++;
                }
            } else if (y1 == y2) {
                for (int x = x1; x <= x2; x++) {
                    counts[y1][x]++;
                }
            } else {
                int dy = y2 > y1 ? 1 : -1;
                for (int x = x1, y = y1; x <= x2; x++, y += dy) {
                    counts[y][x]++;
                }
            }
        }

        int overlaps = 0;
        for (int y = 0; y < 1000; y++) {
            for (int x = 0; x < 1000; x++) {
                if (counts[y][x] >= 2) {
                    overlaps += 1;
                }
            }
        }

        System.out.println(overlaps);
        sc.close();
    }
}