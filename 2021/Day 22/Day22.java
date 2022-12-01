import java.util.*;
import java.util.stream.IntStream;

public class Day22 {
    public static class Pair<T1, T2> {
        private final T1 head;
        private final T2 tail;

        public Pair(T1 head, T2 tail) {
            this.head = head;
            this.tail = tail;
        }

        public T1 head() {
            return head;
        }

        public T2 tail() {
            return tail;
        }
    }

    // Method holder, not to be instantiated
    public static class Interval {
        public static boolean intersects(int pMin, int pMax, int qMin, int qMax) {
            return pMin <= qMax && qMin <= pMax;
        }

        // Given intersecting intervals [pMin, pMax] and [qMin, qMax], determines which part(s) of interval p do or do
        // not intersect interval q. Returns a pair where the head is a list of sub-intervals of p not intersecting q
        // (may have 0, 1 or 2 sub-intervals) and the tail is the sub-interval of p intersecting q
        public static Pair<ArrayList<Pair<Integer, Integer>>, Pair<Integer, Integer>>
        partition(int pMin, int pMax, int qMin, int qMax) {
            ArrayList<Pair<Integer, Integer>> notIntersecting = new ArrayList<>();
            if (qMin <= pMin) {
                if (qMax >= pMax) {
                    // Interval p is contained entirely in interval q
                    return new Pair<>(notIntersecting, new Pair<>(pMin, pMax));
                } else {
                    // Interval q contains left portion of interval p
                    notIntersecting.add(new Pair<>(qMax + 1, pMax));
                    return new Pair<>(notIntersecting, new Pair<>(pMin, qMax));
                }
            } else {
                notIntersecting.add(new Pair<>(pMin, qMin - 1));
                if (qMax >= pMax) {
                    // Interval q contains right portion of interval p
                    return new Pair<>(notIntersecting, new Pair<>(qMin, pMax));
                } else {
                    // Interval q is contained entirely in interval p (and there are non-intersecting gaps on both sides)
                    notIntersecting.add(new Pair<>(qMax + 1, pMax));
                    return new Pair<>(notIntersecting, new Pair<>(qMin, qMax));
                }
            }
        }
    }

    public static class Cuboid {
        private final int xMin;
        private final int xMax;
        private final int yMin;
        private final int yMax;
        private final int zMin;
        private final int zMax;

        public Cuboid(int xMin, int xMax, int yMin, int yMax, int zMin, int zMax) {
            this.xMin = xMin;
            this.xMax = xMax;
            this.yMin = yMin;
            this.yMax = yMax;
            this.zMin = zMin;
            this.zMax = zMax;
        }

        @Override
        public String toString() {
            return "{(" + xMin + ", " + xMax + ") (" + yMin + ", " + yMax + ") (" + zMin + ", " + zMax + ")}";
        }

        public long size() {
            long dx = xMax - xMin + 1;
            long dy = yMax - yMin + 1;
            long dz = zMax - zMin + 1;
            return dx * dy * dz;
        }

        public boolean intersects(Cuboid cuboid) {
            return Interval.intersects(xMin, xMax, cuboid.xMin, cuboid.xMax) &&
                   Interval.intersects(yMin, yMax, cuboid.yMin, cuboid.yMax) &&
                   Interval.intersects(zMin, zMax, cuboid.zMin, cuboid.zMax);
        }

        // Returns a list of cuboids that together form the portion of this cuboid not overlapping the input cuboid.
        // To find these cuboids, consider 1 dimension at a time. Add cuboids spanning the x range(s) of this cuboid
        // not covered by the input. Then, further consider the portion of this cuboid within the covered x interval.
        // Repeat with the y and z dimensions.
        public ArrayList<Cuboid> minus(Cuboid cuboid) {
            ArrayList<Cuboid> leftovers = new ArrayList<>();

            Pair<ArrayList<Pair<Integer, Integer>>, Pair<Integer, Integer>>
                partitionX = Interval.partition(xMin, xMax, cuboid.xMin, cuboid.xMax);
            for (Pair<Integer, Integer> leftoverX : partitionX.head()) {
                leftovers.add(new Cuboid(leftoverX.head(), leftoverX.tail(), yMin, yMax, zMin, zMax));
            }
            Pair<Integer, Integer> overlapX = partitionX.tail();
            int newXMin = overlapX.head();
            int newXMax = overlapX.tail();

            Pair<ArrayList<Pair<Integer, Integer>>, Pair<Integer, Integer>>
                partitionY = Interval.partition(yMin, yMax, cuboid.yMin, cuboid.yMax);
            for (Pair<Integer, Integer> leftoverY : partitionY.head()) {
                leftovers.add(new Cuboid(newXMin, newXMax, leftoverY.head(), leftoverY.tail(), zMin, zMax));
            }
            Pair<Integer, Integer> overlapY = partitionY.tail();
            int newYMin = overlapY.head();
            int newYMax = overlapY.tail();

            Pair<ArrayList<Pair<Integer, Integer>>, Pair<Integer, Integer>>
                partitionZ = Interval.partition(zMin, zMax, cuboid.zMin, cuboid.zMax);
            for (Pair<Integer, Integer> leftoverZ : partitionZ.head()) {
                leftovers.add(new Cuboid(newXMin, newXMax, newYMin, newYMax, leftoverZ.head(), leftoverZ.tail()));
            }

            return leftovers;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // reactor stores cuboids of cubes that are on and the cuboids never overlap
        LinkedList<Cuboid> reactor = new LinkedList<>();
        while (sc.hasNext()) {
            String[] input = sc.nextLine().split(" x=|,y=|,z=|\\.\\.");
            int[] coords = IntStream.range(1, 7).map(i -> Integer.parseInt(input[i])).toArray();

            // Part 1
            // if (Math.abs(coords[0]) > 50) {
            //    break;
            // }

            Cuboid cuboid = new Cuboid(coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]);
            // Replace any stored cuboid that overlaps the new cuboid with other cuboids to make up the leftover volume
            ListIterator<Cuboid> it = reactor.listIterator();
            while (it.hasNext()) {
                Cuboid c = it.next();
                if (c.intersects(cuboid)) {
                    it.remove();
                    for (Cuboid newCuboid : c.minus(cuboid)) {
                        it.add(newCuboid);
                    }
                }
            }

            if (input[0].equals("on")) {
                reactor.add(cuboid);
            }
        }

        System.out.println(reactor.stream().mapToLong(Cuboid::size).sum());
    }
}
