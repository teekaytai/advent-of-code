import java.util.Scanner;
import java.util.Arrays;
public class Day2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int pos = 0;
        int depth = 0;
        int aim = 0;
        while (sc.hasNext()) {
            String[] arr = sc.nextLine().split(" ");
            String dir = arr[0];
            int amt = Integer.parseInt(arr[1]);
            if (dir.equals("forward")) {
                pos += amt;
                depth += aim * amt;
            } else {
                aim += dir.equals("down") ? amt : -amt;
            }
        }
        System.out.println(pos * depth);
        sc.close();
    }
}