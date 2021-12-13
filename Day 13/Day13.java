import java.util.*;
import java.util.stream.Collectors;

public class Day13 {
    public static class Point {
        int x;
        int y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public static class SorterByX implements Comparator<Point> {
            @Override
            public int compare(Point p1, Point p2) {
                int cmp = Integer.compare(p1.x, p2.x);
                return cmp != 0 ? cmp : Integer.compare(p1.y, p2.y);
            }
        }

        public static class SorterByY implements Comparator<Point> {
            @Override
            public int compare(Point p1, Point p2) {
                int cmp = Integer.compare(p1.y, p2.y);
                return cmp != 0 ? cmp : Integer.compare(p1.x, p2.x);
            }
        }

        public Point reflect(char axis, int z) {
            if (axis == 'x') {
                if (this.x > z) {
                    return new Point(z * 2 - this.x, this.y);
                }
            } else {
                if (this.y > z) {
                    return new Point(this.x, z * 2 - this.y);
                }
            }

            return this;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        TreeSet<Point> dotsByX = new TreeSet<>(new Point.SorterByX());
        TreeSet<Point> dotsByY = new TreeSet<>(new Point.SorterByY());
        while (true) {
            String input = sc.nextLine();
            if (input.equals("")) {
                break;
            }
            String[] coords = input.split(",");
            Point p = new Point(Integer.parseInt(coords[0]), Integer.parseInt(coords[1]));
            dotsByX.add(p);
            dotsByY.add(p);
        }

        // Dimensions of the paper at the end
        int smallestX = Integer.MAX_VALUE;
        int smallestY = Integer.MAX_VALUE;

        while (sc.hasNext()) {
            String[] fold = sc.nextLine().split("=");
            char axis = fold[0].charAt(11);  // fold along _
            int z = Integer.parseInt(fold[1]);
            ArrayList<Point> toReplace;
            if (axis == 'x') {
                smallestX = z;
                toReplace = new ArrayList<>(dotsByX.tailSet(new Point(z, 0)));
            } else {
                smallestY = z;
                toReplace = new ArrayList<>(dotsByY.tailSet(new Point(0, z)));
            }
            for (Point p : toReplace) {
                Point reflected = p.reflect(axis, z);
                dotsByX.add(reflected);
                dotsByX.remove(p);
                dotsByY.add(reflected);
                dotsByY.remove(p);
            }
        }

        // System.out.println(dotsByX.size());

        String[][] paper = new String[smallestY][smallestX];
        for (String[] row : paper) {
            Arrays.fill(row, ".");
        }
        for (Point dot : dotsByX) {
            paper[dot.y][dot.x] = "#";
        }

        System.out.println(
            Arrays.stream(paper)
                .map(row -> String.join("", row))
                .collect(Collectors.joining("\n"))
        );
    }
}
