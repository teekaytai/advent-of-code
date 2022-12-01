import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.LongStream;

public class Day6 {
    public static void main(String[] args) {
        final int adult_timer = 7;
        final int newborn_timer = 9;
        final int days = 256;
        // fishCounts[i] represents how many fish a single fish at newborn_timer-1 will become after i days
        long[] fishCounts = new long[days + newborn_timer];
        for (int i = 0; i < newborn_timer; i++) {
            fishCounts[i] = 1;
        }
        for (int i = newborn_timer; i < fishCounts.length; i++) {
            fishCounts[i] = fishCounts[i - newborn_timer] + fishCounts[i - adult_timer];
        }
        Scanner sc = new Scanner(System.in);
        String[] input = sc.nextLine().split(",");
        LongStream resultFishes = Arrays.stream(input).mapToLong(timer ->
                fishCounts[days + (newborn_timer - Integer.parseInt(timer) - 1)]
        );
        System.out.println(resultFishes.sum());
    }
}
