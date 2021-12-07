import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Day3 {
    public static void part1() {
        Scanner sc = new Scanner(System.in);
        int[] counts = new int[12];
        Arrays.fill(counts, 0);
        while (sc.hasNext()) {
            String bin = sc.nextLine();
            for (int i = 0; i < 12; i++) {
                counts[i] += bin.charAt(i) == '1' ? 1 : -1;
            }
        }

        int gamma = 0;
        int epsilon = 0;
        for (int i = 0; i < 12; i++) {
            if (counts[i] >= 0) {
                gamma += 1;
            } else {
                epsilon += 1;
            }
            if (i < 11) {
                gamma = gamma << 1;
                epsilon = epsilon << 1;
            }
        }

        System.out.println(gamma * epsilon);
        
        sc.close();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<String> o2Bins = new ArrayList<String>();
        while (sc.hasNext()) {
            o2Bins.add(sc.nextLine());
        }
        ArrayList<String> co2Bins = new ArrayList<String>(o2Bins);
        
        for (int i = 0; o2Bins.size() > 1; i++) {
            int count = 0;
            int j = i;
            for (String bin : o2Bins) {
                count += bin.charAt(i) == '1' ? 1 : -1;
            }
            char keepBit = count >= 0 ? '1' : '0';
            o2Bins.removeIf(bin -> bin.charAt(j) != keepBit);
        }
        
        for (int i = 0; co2Bins.size() > 1; i++) {
            int count = 0;
            int j = i;
            for (String bin : co2Bins) {
                count += bin.charAt(i) == '1' ? 1 : -1;
            }
            char keepBit = count >= 0 ? '0' : '1';
            co2Bins.removeIf(bin -> bin.charAt(j) != keepBit);
        }
        
        System.out.println(Integer.parseInt(o2Bins.get(0), 2) * Integer.parseInt(co2Bins.get(0), 2));
        
        sc.close();
    }
}