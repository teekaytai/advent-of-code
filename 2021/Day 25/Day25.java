import java.util.ArrayList;
import java.util.Scanner;

public class Day25 {
    public static class Cucumber {
        private int r;
        private int c;
        private boolean blocked;

        public Cucumber(int r, int c) {
            this.r = r;
            this.c = c;
        }

        public int getR() {
            return r;
        }

        public void setR(int r) {
            this.r = r;
        }

        public int getC() {
            return c;
        }

        public void setC(int c) {
            this.c = c;
        }

        public boolean isNotBlocked() {
            return !blocked;
        }

        public void setBlocked(boolean blocked) {
            this.blocked = blocked;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Cucumber[]> rowList = new ArrayList<>();
        ArrayList<Cucumber> rightCucumbersList = new ArrayList<>();
        ArrayList<Cucumber> downCucumbersList = new ArrayList<>();
        for (int r = 0; sc.hasNext(); r++) {
            String[] inputRow = sc.nextLine().split("");
            Cucumber[] cucumbersRow = new Cucumber[inputRow.length];
            for (int c = 0; c < inputRow.length; c++) {
                if (!inputRow[c].equals(".")) {
                    Cucumber cucumber = new Cucumber(r, c);
                    cucumbersRow[c] = cucumber;
                    if (inputRow[c].equals(">")) {
                        rightCucumbersList.add(cucumber);
                    } else {
                        downCucumbersList.add(cucumber);
                    }
                }
            }
            rowList.add(cucumbersRow);
        }

        Cucumber[][] grid = rowList.toArray(new Cucumber[0][]);
        Cucumber[] eastCucumbers = rightCucumbersList.toArray(new Cucumber[0]);
        Cucumber[] southCucumbers = downCucumbersList.toArray(new Cucumber[0]);
        final int HEIGHT = grid.length;
        final int WIDTH = grid[0].length;

        boolean cucumbersStopped = false;
        int steps = 0;
        while (!cucumbersStopped) {
            cucumbersStopped = true;
            steps++;

            for (Cucumber cucumber : eastCucumbers) {
                boolean blocked = grid[cucumber.getR()][(cucumber.getC() + 1) % WIDTH] != null;
                cucumber.setBlocked(blocked);
            }
            for (Cucumber cucumber : eastCucumbers) {
                if (cucumber.isNotBlocked()) {
                    cucumbersStopped = false;
                    int r = cucumber.getR();
                    int c = cucumber.getC();
                    int nextC = (c + 1) % WIDTH;
                    grid[r][c] = null;
                    grid[r][nextC] = cucumber;
                    cucumber.setC(nextC);
                }
            }

            for (Cucumber cucumber : southCucumbers) {
                boolean blocked = grid[(cucumber.getR() + 1) % HEIGHT][cucumber.getC()] != null;
                cucumber.setBlocked(blocked);
            }
            for (Cucumber cucumber : southCucumbers) {
                if (cucumber.isNotBlocked()) {
                    cucumbersStopped = false;
                    int r = cucumber.getR();
                    int c = cucumber.getC();
                    int nextR = (r + 1) % HEIGHT;
                    grid[r][c] = null;
                    grid[nextR][c] = cucumber;
                    cucumber.setR(nextR);
                }
            }
        }

        System.out.println(steps);
    }
}
