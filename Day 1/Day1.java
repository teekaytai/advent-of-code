import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Day1 {
    public static void main(String[] args) throws FileNotFoundException {
        File file = new File("input.txt");
        Scanner sc = new Scanner(file);
        int count = 0;
        int a = sc.nextInt();
        int b = sc.nextInt();
        int c = sc.nextInt();
        while (sc.hasNextInt()) {
            int nextDepth = sc.nextInt();
            count += nextDepth > a ? 1 : 0;
            a = b;
            b = c;
            c = nextDepth;
        }
        System.out.println(count);
        sc.close();
    }
}