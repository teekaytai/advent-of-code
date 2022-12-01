import java.util.*;
import java.util.stream.IntStream;

public class Day22IntervalST {
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

        public int getXMin() {
            return xMin;
        }

        public int getXMax() {
            return xMax;
        }
    }

    // Works like a 1d interval search tree, where the x range of the cuboid will be used as the interval.
    // The cuboids are sorted by their xMin value, and each node also stores the max xMax value of the cuboids
    // in that node and the nodes below to aid in interval search.
    // The cuboids stored in the tree will always not overlap one another.
    public static class CuboidST {
        Node root;

        // Returns a list of every cuboid stored in the tree
        public ArrayList<Cuboid> getCuboids() {
            ArrayList<Cuboid> cuboids = new ArrayList<>();
            getCuboids(cuboids, root);
            return cuboids;
        }

        private void getCuboids(ArrayList<Cuboid> cuboidsList, Node curr) {
            if (curr != null) {
                cuboidsList.add(curr.getCuboid());
                getCuboids(cuboidsList, curr.getLeft());
                getCuboids(cuboidsList, curr.getRight());
            }
        }

        public void on(Cuboid cuboid) {
            replaceOverlaps(cuboid);
            add(cuboid);
        }

        public void off(Cuboid cuboid) {
            replaceOverlaps(cuboid);
        }

        // Adds a cuboid to the tree that is guaranteed not to overlap any other cuboid in the tree
        private void add(Cuboid cuboid) {
            Node newNode = new Node(cuboid);

            if (root == null) {
                root = newNode;
                return;
            }

            // Only the x interval is considered for this interval search tree
            int xMin = cuboid.getXMin();
            int xMax = cuboid.getXMax();

            Node curr = root;
            while (true) {
                curr.setMaxEndpoint(Math.max(curr.getMaxEndpoint(), xMax));
                int currCuboidXMin = curr.getCuboid().getXMin();
                // If the xMins match, randomly pick a direction to help keep tree balanced
                if (xMin > currCuboidXMin || (xMin == currCuboidXMin && Math.random() < 0.5)) {
                    if (curr.getRight() == null) {
                        curr.setRight(newNode);
                        newNode.setParent(curr);
                        newNode.setIsLeftChild(false);
                        break;
                    }
                    curr = curr.getRight();
                } else {
                    if (curr.getLeft() == null) {
                        curr.setLeft(newNode);
                        newNode.setParent(curr);
                        newNode.setIsLeftChild(true);
                        break;
                    }
                    curr = curr.getLeft();
                }
            }
        }

        // Replace any stored cuboid that overlaps the new cuboid with other cuboids to make up the leftover volume
        private void replaceOverlaps(Cuboid cuboid) {
            for (Cuboid toReplace : removeOverlaps(cuboid)) {
                for (Cuboid newCuboid : toReplace.minus(cuboid)) {
                    add(newCuboid);
                }
            }
        }

        // Removes every cuboid which overlaps the input cuboid and returns them in a list
        private ArrayList<Cuboid> removeOverlaps(Cuboid cuboid) {
            ArrayList<Cuboid> removedList = new ArrayList<>();
            removeOverlaps(cuboid, removedList, root);
            return removedList;
        }

        private void removeOverlaps(Cuboid cuboid, ArrayList<Cuboid> removedList, Node curr) {
            if (curr == null || curr.getMaxEndpoint() < cuboid.getXMin()) {
                return;
            }

            Cuboid currCuboid = curr.getCuboid();

            removeOverlaps(cuboid, removedList, curr.getLeft());
            if (cuboid.getXMax() >= currCuboid.getXMin()) {
                removeOverlaps(cuboid, removedList, curr.getRight());
                if (currCuboid.intersects(cuboid)) {
                    removedList.add(currCuboid);
                    remove(curr);
                }
            }
        }

        // Removes the input node from the tree
        private void remove(Node node) {
            if (node.getLeft() == null) {
                removeMin(node);
                return;
            }
            if (node.getRight() == null) {
                removeMax(node);
                return;
            }

            // Randomly choose which side to find replacement from to help keep tree balanced
            Node replacement = Math.random() < 0.5 ? removeMax(node.getLeft()) : removeMin(node.getRight());
            Node parent = node.getParent();

            Node left = node.getLeft();
            int leftMaxEndpoint = Integer.MIN_VALUE;
            replacement.setLeft(left);
            if (left != null) {
                left.setParent(replacement);
                leftMaxEndpoint = left.getMaxEndpoint();
            }

            Node right = node.getRight();
            int rightMaxEndpoint = Integer.MIN_VALUE;
            replacement.setRight(right);
            if (right != null) {
                right.setParent(replacement);
                rightMaxEndpoint = right.getMaxEndpoint();
            }

            replacement.setParent(parent);
            int xMax = replacement.getCuboid().getXMax();
            replacement.setMaxEndpoint(Math.max(Math.max(leftMaxEndpoint, rightMaxEndpoint), xMax));

            if (parent != null) {
                replacement.setIsLeftChild(node.isLeftChild());
                if (node.isLeftChild()) {
                    parent.setLeft(replacement);
                } else {
                    parent.setRight(replacement);
                }
                updateAncestorsMaxEndpoint(parent);
            } else {
                root = replacement;
            }
        }

        // Removes and returns the minimum node in the subtree rooted at input node
        private Node removeMin(Node node) {
            while (node.getLeft() != null) {
                node = node.getLeft();
            }

            Node parent = node.getParent();
            Node child = node.getRight();
            if (child != null) {
                child.setParent(parent);
                if (parent != null) {
                    child.setIsLeftChild(node.isLeftChild());
                }
            }
            if (parent != null) {
                if (node.isLeftChild()) {
                    parent.setLeft(child);
                } else {
                    parent.setRight(child);
                }
                updateAncestorsMaxEndpoint(parent);
            } else {
                root = child;
            }

            return node;
        }

        // Removes and returns the maximum node in the subtree rooted at input node
        private Node removeMax(Node node) {
            while (node.getRight() != null) {
                node = node.getRight();
            }

            Node parent = node.getParent();
            Node child = node.getLeft();
            if (child != null) {
                child.setParent(parent);
                if (parent != null) {
                    child.setIsLeftChild(node.isLeftChild());
                }
            }
            if (parent != null) {
                if (node.isLeftChild()) {
                    parent.setLeft(child);
                } else {
                    parent.setRight(child);
                }
                updateAncestorsMaxEndpoint(parent);
            } else {
                root = child;
            }

            return node;
        }

        // Recalculates the maxEndpoint value of input node and all its ancestors
        private void updateAncestorsMaxEndpoint(Node node) {
            while (node != null) {
                Node left = node.getLeft();
                int leftMaxEndpoint = left != null ? left.getMaxEndpoint() : Integer.MIN_VALUE;
                Node right = node.getRight();
                int rightMaxEndpoint = right != null ? right.getMaxEndpoint() : Integer.MIN_VALUE;
                int xMax = node.getCuboid().getXMax();
                int newMaxEndpoint = Math.max(Math.max(leftMaxEndpoint, rightMaxEndpoint), xMax);
                if (node.getMaxEndpoint() != newMaxEndpoint) {
                    node.setMaxEndpoint(newMaxEndpoint);
                    node = node.getParent();
                } else {
                    // Node's maxEndpoint value did not change, no need to traverse upwards further
                    break;
                }
            }
        }

        private static class Node {
            private final Cuboid cuboid;
            private Node left;
            private Node right;
            private Node parent;
            private boolean isLeftChild;
            private int maxEndpoint;  // The maximum xMax of any cuboid from this node down

            public Node(Cuboid cuboid) {
                this.cuboid = cuboid;
                this.maxEndpoint = cuboid.getXMax();
            }

            public Cuboid getCuboid() {
                return cuboid;
            }

            public Node getLeft() {
                return left;
            }

            public void setLeft(Node left) {
                this.left = left;
            }

            public Node getRight() {
                return right;
            }

            public void setRight(Node right) {
                this.right = right;
            }

            public Node getParent() {
                return parent;
            }

            public void setParent(Node parent) {
                this.parent = parent;
            }

            public boolean isLeftChild() {
                return isLeftChild;
            }

            public void setIsLeftChild(boolean isLeftChild) {
                this.isLeftChild = isLeftChild;
            }

            public int getMaxEndpoint() {
                return maxEndpoint;
            }

            public void setMaxEndpoint(int maxEndpoint) {
                this.maxEndpoint = maxEndpoint;
            }
        }
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // reactor stores cuboids of cubes that are on and the cuboids never overlap
        CuboidST reactor = new CuboidST();
        while (sc.hasNext()) {
            String[] input = sc.nextLine().split(" x=|,y=|,z=|\\.\\.");
            int[] coords = IntStream.range(1, 7).map(i -> Integer.parseInt(input[i])).toArray();

            // Part 1
            // if (Math.abs(coords[0]) > 50) {
            //     break;
            // }

            Cuboid cuboid = new Cuboid(coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]);

            if (input[0].equals("on")) {
                reactor.on(cuboid);
            } else {
                reactor.off(cuboid);
            }
        }

        System.out.println(reactor.getCuboids().stream().mapToLong(Cuboid::size).sum());
    }
}
