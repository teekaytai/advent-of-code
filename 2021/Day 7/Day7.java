import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.IntStream;

public class Day7 {
    public static void part1() {
        Scanner sc = new Scanner(System.in);
        IntStream intStream = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt);
        int[] xs = intStream.sorted().toArray();
        int median = xs[(int) (xs.length / 2.0)];
        System.out.println(Arrays.stream(xs).map(x -> Math.abs(x - median)).sum());
    }


    // Fuel needed to move between x1 and x2 (using part 2 logic)
    public static int fuelBetween(int x1, int x2) {
        int dx = Math.abs(x1 - x2);
        return dx * (dx + 1) / 2;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        IntStream intStream = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt);
        int[] xs = intStream.sorted().toArray();
        final int L = xs.length;

        // Start optimalPos at left-most crab and adjust rightwards step by step
        int optimalPos = xs[0];

        // marginalBenefit equals the net fuel savings from moving optimalPos one step to the right
        // fuelNeeded is the fuel required if we use the current optimalPos
        int marginalBenefit = Arrays.stream(xs).map(x -> x > xs[0] ? x - xs[0] : -1).sum();
        int fuelNeeded = Arrays.stream(xs).map(x -> fuelBetween(x, xs[0])).sum();

        // Index of left-most crab that is to the right of optimalPos
        int i = 0;
        while (xs[i] == optimalPos) {
            i++;
        }

        while (marginalBenefit > 0) {
            optimalPos++;
            fuelNeeded -= marginalBenefit;
            marginalBenefit -= L;
            while (xs[i] == optimalPos) {
                i++;
                marginalBenefit--; // When crossing over a crab, fuel savings jumps by 2 instead of 1 (from 1 to -1)
            }
        }

        System.out.println(fuelNeeded);
    }
}
