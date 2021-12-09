import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.util.Stack;

public class Day9 {
    public static void part1() {
        Scanner sc = new Scanner(System.in);
        ArrayList<int[]> heightMap = new ArrayList<>();
        while (sc.hasNext()) {
            heightMap.add(Arrays.stream(sc.nextLine().split("")).mapToInt(Integer::parseInt).toArray());
        }

        final int HEIGHT = heightMap.size();
        final int WIDTH = heightMap.get(0).length;
        final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int totalRisk = 0;

        for (int y = 0; y < HEIGHT; y++) {
            int[] row = heightMap.get(y);
            for (int x = 0; x < WIDTH; x++) {
                int cell = row[x];
                boolean isLowPoint = true;

                for (int[] dir : DIRS) {
                    int X = x + dir[0];
                    int Y = y + dir[1];
                    if (X >= 0 && X < WIDTH && Y >= 0 && Y < HEIGHT && heightMap.get(Y)[X] <= cell) {
                        isLowPoint = false;
                        break;
                    }
                }

                if (isLowPoint) {
                    totalRisk += cell + 1;
                }
            }
        }

        System.out.println(totalRisk);
    }


    public static class Cell {
        private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        public int x;
        public int y;

        public Cell(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public ArrayList<Cell> getNeighbours(int width, int height) {
            ArrayList<Cell> neighbours = new ArrayList<>();
            for (int[] dir : DIRS) {
                int X = this.x + dir[0];
                int Y = this.y + dir[1];
                if (X >= 0 && X < width && Y >= 0 && Y < height) {
                    neighbours.add(new Cell(X, Y));
                }
            }

            return neighbours;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<int[]> heightMap = new ArrayList<>();
        while (sc.hasNext()) {
            heightMap.add(Arrays.stream(sc.nextLine().split("")).mapToInt(Integer::parseInt).toArray());
        }

        final int HEIGHT = heightMap.size();
        final int WIDTH = heightMap.get(0).length;
        int[] biggestBasins = new int[3];

        Stack<Cell> basinCells = new Stack<>();  // Used to store cells of a single basin

        for (int y = 0; y < HEIGHT; y++) {
            int[] row = heightMap.get(y);
            for (int x = 0; x < WIDTH; x++) {
                if (row[x] == 9) {
                    // Cell not part of a basin or already part of an earlier basin
                    continue;
                }

                // New basin, flood fill basin with 9s to ensure basin visited only once
                int basinSize = 0;
                heightMap.get(y)[x] = 9;  // Never look at cell again
                basinCells.push(new Cell(x, y));
                while (!basinCells.empty()) {
                    basinSize++;
                    Cell cell = basinCells.pop();
                    for (Cell neighbour : cell.getNeighbours(WIDTH, HEIGHT)) {
                        if (heightMap.get(neighbour.y)[neighbour.x] < 9) {
                            heightMap.get(neighbour.y)[neighbour.x] = 9;
                            basinCells.push(neighbour);
                        }
                    }
                }

                // Check if basinSize gets into top 3 biggestBasins
                for (int i = 0; i < biggestBasins.length; i++) {
                    if (basinSize > biggestBasins[i]) {
                        int temp = biggestBasins[i];
                        biggestBasins[i] = basinSize;
                        basinSize = temp;
                    }
                }
            }
        }

        System.out.println(biggestBasins[0] * biggestBasins[1] * biggestBasins[2]);
    }
}
