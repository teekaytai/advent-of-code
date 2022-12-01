import java.util.ArrayList;
import java.util.Scanner;

public class Day11 {
    public static class Octopus {
        private static int totalFlashes = 0;

        private int energy;
        private boolean flashed = false;
        private ArrayList<Octopus> neighbours;

        public Octopus(int energy) {
            this.energy = energy;
        }

        public void setNeighbours(ArrayList<Octopus> neighbours) {
            this.neighbours = neighbours;
        }

        public static int getTotalFlashes() {
            return totalFlashes;
        }

        public static void resetTotalFlashes() {
            Octopus.totalFlashes = 0;
        }

        public void increment() {
            if (!this.flashed) {
                this.energy++;
                if (this.energy > 9) {
                    this.flashed = true;
                    this.flash();
                }
            }
        }

        private void flash() {
            totalFlashes++;
            for (Octopus neighbour : this.neighbours) {
                neighbour.increment();
            }
        }

        // Reset energy to 0 if this octopus flashed
        public void resetFlash() {
            if (this.flashed) {
                this.energy = 0;
                this.flashed = false;
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<ArrayList<Octopus>> grid = new ArrayList<>();
        while (sc.hasNext()) {
            String[] row = sc.nextLine().split("");
            ArrayList<Octopus> octopi = new ArrayList<>();
            for (String energy : row) {
                octopi.add(new Octopus(Integer.parseInt(energy)));
            }
            grid.add(octopi);
        }

        final int HEIGHT = grid.size();
        final int WIDTH = grid.get(0).size();

        // Link up neighbours
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                ArrayList<Octopus> neighbours = new ArrayList<>();

                for (int dy = -1; dy <= 1; dy++) {
                    for (int dx = -1; dx <= 1; dx++) {
                        int X = x + dx;
                        int Y = y + dy;
                        if (X >= 0 && X < WIDTH && Y >= 0 && Y < HEIGHT) {
                            neighbours.add(grid.get(Y).get(X));
                        }
                    }
                }

                grid.get(y).get(x).setNeighbours(neighbours);
            }
        }

        // Part 1
        /*
        int steps = 100;
        for (int i = 0; i < steps; i++) {
            for (ArrayList<Octopus> octopi : grid) {
                for (Octopus octopus : octopi) {
                    octopus.increment();
                }
            }

            for (ArrayList<Octopus> octopi : grid) {
                for (Octopus octopus : octopi) {
                    octopus.resetFlash();
                }
            }
        }

        System.out.println(Octopus.getTotalFlashes());
        */

        // Part 2
        int totalOctopi = HEIGHT * WIDTH;
        int steps;
        for (steps = 0; Octopus.getTotalFlashes() != totalOctopi; steps++) {
            Octopus.resetTotalFlashes();

            for (ArrayList<Octopus> octopi : grid) {
                for (Octopus octopus : octopi) {
                    octopus.increment();
                }
            }

            for (ArrayList<Octopus> octopi : grid) {
                for (Octopus octopus : octopi) {
                    octopus.resetFlash();
                }
            }
        }

        System.out.println(steps);
    }
}
