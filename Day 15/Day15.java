import java.util.*;

public class Day15 {
    public static class Dijkstra {
        private static final int[][] DIRS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

        private final int HEIGHT;
        private final int WIDTH;
        private final Node[][] grid;

        public Dijkstra(int[][] weights) {
            // Part 2
            int h = weights.length;
            int w = weights[0].length;
            HEIGHT = 5 * h;
            WIDTH = 5 * w;
            grid = new Node[HEIGHT][WIDTH];
            for (int r = 0; r < HEIGHT; r++) {
                for (int c = 0; c < WIDTH; c++) {
                    int weight = (weights[r % h][c % w] + (r / h) + (c / w)) % 9;
                    weight = weight == 0 ? 9 : weight;
                    grid[r][c] = new Node(r, c, weight);
                }
            }

            // Part 1
            /*
            HEIGHT = weights.length;
            WIDTH = weights[0].length;
            grid = new Node[HEIGHT][WIDTH];
            for (int r = 0; r < HEIGHT; r++) {
                for (int c = 0; c < WIDTH; c++) {
                    grid[r][c] = new Node(r, c, weights[r][c]);
                }
            }
            */
        }

        public int shortestPath() {
            final Node START = grid[0][0];
            final Node END = grid[HEIGHT - 1][WIDTH - 1];

            PriorityQueue<Node> fringe = new PriorityQueue<>();
            START.dist = 0;
            fringe.add(START);

            while (!END.seen) {
                Node currNode = fringe.remove();

                for (Node neighbour : currNode.neighbours()) {
                    // Important note: since the cost of entering a node is independent of which direction you come
                    // from, the first update to a node's dist is guaranteed to be the shortest path to that node.
                    // There is also no need to worry about modifying keys of nodes already in the PQ
                    if (!neighbour.seen) {
                        neighbour.seen = true;
                        neighbour.dist = currNode.dist + neighbour.weight;
                        fringe.add(neighbour);
                    }
                }
            }

            return END.dist;
        }

        private class Node implements Comparable<Node> {
            private final int r;
            private final int c;
            private final int weight;
            private boolean seen = false;  // Currently in PQ or already visited
            private int dist = Integer.MAX_VALUE;

            public Node(int r, int c, int weight) {
                this.r = r;
                this.c = c;
                this.weight = weight;
            }

            @Override
            public int compareTo(Node o) {
                return Integer.compare(this.dist, o.dist);
            }

            private ArrayList<Node> neighbours() {
                ArrayList<Node> neighbours = new ArrayList<>();
                for (int[] dir : DIRS) {
                    int R = r + dir[0];
                    int C = c + dir[1];
                    if (R >= 0 && R < HEIGHT && C >= 0 && C < WIDTH) {
                        neighbours.add(grid[R][C]);
                    }
                }

                return neighbours;
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<int[]> risks = new ArrayList<>();
        while (sc.hasNext()) {
            String[] row = sc.nextLine().split("");
            risks.add(Arrays.stream(row).mapToInt(Integer::parseInt).toArray());
        }
        Dijkstra cavern = new Dijkstra(risks.toArray(new int[0][]));

        System.out.println(cavern.shortestPath());
    }
}
