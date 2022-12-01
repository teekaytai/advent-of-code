import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Day20 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int[] enhanceRule = sc.nextLine().chars().map(c -> c == '#' ? 1 : 0).toArray();
        sc.nextLine();

        ArrayList<int[]> rowList = new ArrayList<>();
        while (sc.hasNext()) {
            rowList.add(sc.nextLine().chars().map(c -> c == '#' ? 1 : 0).toArray());
        }
        int[][] picture = rowList.toArray(new int[0][]);

        int surroundings = 0;  // Every pixel outside picture starts out dark

        final int STEPS = 50;

        for (int i = 0; i < STEPS; i++) {
            int oldHeight = picture.length;
            int oldWidth = picture[0].length;
            int[][] newPicture = new int[oldHeight + 2][oldWidth + 2];  // Pixels bordering old picture can change too

            for (int r = 0; r < newPicture.length; r++) {
                for (int c = 0; c < newPicture[r].length; c++) {
                    int index = 0;
                    // Obtain 9 pixels in a 3x3 square and combine the bits into index for image enhancement rule
                    // Remember that newPicture is bigger and offset by 1 from old picture
                    // (i.e. newPicture[1][1] is the same pixel as picture[0][0])
                    for (int R = r - 2; R <= r; R++) {
                        for (int C = c - 2; C <= c; C++) {
                            index <<= 1;
                            if (R >= 0 && R < oldHeight && C >= 0 && C < oldWidth) {
                                index += picture[R][C];
                            } else {
                                index += surroundings;
                            }
                        }
                    }

                    newPicture[r][c] = enhanceRule[index];
                }
            }

            surroundings = enhanceRule[surroundings == 1 ? 511 : 0];
            picture = newPicture;
        }

        System.out.println(Arrays.stream(picture).mapToInt(row -> Arrays.stream(row).sum()).sum());
    }
}
