import java.util.*;
import java.util.function.Function;

public class Day19 {
    public static class Vector {
        // A rotation function maps a vector to another vector by rotating the axes around while maintaining chirality
        private static final ArrayList<Function<Vector, Vector>> ROTATION_FNS = new ArrayList<>(
                Arrays.asList(
                        v -> new Vector(v.x, v.y, v.z),
                        v -> new Vector(v.x, v.z, -v.y),
                        v -> new Vector(v.x, -v.y, -v.z),
                        v -> new Vector(v.x, -v.z, v.y),
                        v -> new Vector(-v.x, v.y, -v.z),
                        v -> new Vector(-v.x, -v.z, -v.y),
                        v -> new Vector(-v.x, -v.y, v.z),
                        v -> new Vector(-v.x, v.z, v.y),
                        v -> new Vector(v.y, v.x, -v.z),
                        v -> new Vector(v.y, -v.z, -v.x),
                        v -> new Vector(v.y, -v.x, v.z),
                        v -> new Vector(v.y, v.z, v.x),
                        v -> new Vector(-v.y, v.x, v.z),
                        v -> new Vector(-v.y, v.z, -v.x),
                        v -> new Vector(-v.y, -v.x, -v.z),
                        v -> new Vector(-v.y, -v.z, v.x),
                        v -> new Vector(v.z, v.x, v.y),
                        v -> new Vector(v.z, v.y, -v.x),
                        v -> new Vector(v.z, -v.x, -v.y),
                        v -> new Vector(v.z, -v.y, v.x),
                        v -> new Vector(-v.z, v.x, -v.y),
                        v -> new Vector(-v.z, -v.y, -v.x),
                        v -> new Vector(-v.z, -v.x, v.y),
                        v -> new Vector(-v.z, v.y, v.x)
                ));

        private final int x;
        private final int y;
        private final int z;

        public Vector(int x, int y, int z) {
            this.x = x;
            this.y = y;
            this.z = z;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Vector vector = (Vector) o;
            return x == vector.x && y == vector.y && z == vector.z;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y, z);
        }

        public Vector plus(Vector v) {
            return new Vector(x + v.x, y + v.y, z + v.z);
        }
        
        public Vector minus(Vector v) {
            return new Vector(x - v.x, y - v.y, z - v.z);
        }

        public int manDist(Vector v) {
            return Math.abs(x - v.x) + Math.abs(y - v.y) + Math.abs(z - v.z);
        }
    }

    public static class VectorSet implements Iterable<Vector> {
        HashSet<Vector> vectors = new HashSet<>();

        public void add(Vector v) {
            vectors.add(v);
        }

        public void addVectorSet(VectorSet vectorSet) {
            for (Vector v : vectorSet) {
                vectors.add(v);
            }
        }

        public int size() {
            return vectors.size();
        }

        @Override
        public Iterator<Vector> iterator() {
            return vectors.iterator();
        }

        // Returns a new VectorSet where every vector has been replaced with one viewed from a different orientation
        public VectorSet rotate(Function<Vector, Vector> rotationFn) {
            VectorSet newVectorSet = new VectorSet();
            vectors.forEach(vector -> newVectorSet.add(rotationFn.apply(vector)));
            return newVectorSet;
        }

        // Returns a new VectorSet by adding the input vector to each vector
        public VectorSet translate(Vector v) {
            VectorSet newVectors = new VectorSet();
            vectors.forEach(vector -> newVectors.add(vector.plus(v)));
            return newVectors;
        }
    }

    public static class Detector {
        private VectorSet beacons;
        private Vector position;

        public Detector(VectorSet beacons) {
            this.beacons = beacons;
        }

        public VectorSet getBeacons() {
            return beacons;
        }

        public void setBeacons(VectorSet beacons) {
            this.beacons = beacons;
        }

        public Vector getPosition() {
            return position;
        }

        public void setPosition(Vector position) {
            this.position = position;
        }

        // Attempts to calibrate another detector using this calibrated detector.
        // Returns true iff there are at least 12 overlapping beacons and the calibration is successful
        // Once calibrated, a detector's beacons will reflect absolute coordinates (relative to detector 0)
        // and the detector will also store its absolute position
        public boolean calibrate(Detector detector) {
            VectorSet otherBeacons = detector.getBeacons();

            // Try all 24 possible detector orientations
            for (Function<Vector, Vector> rotationFn : Vector.ROTATION_FNS) {
                VectorSet rotatedVectorSet = otherBeacons.rotate(rotationFn);

                // Count the offset vectors between every pair of beacons
                HashMap<Vector, Integer> offsetCounts = new HashMap<>();
                for (Vector p : beacons) {
                    for (Vector q : rotatedVectorSet) {
                        offsetCounts.merge(p.minus(q), 1, Integer::sum);
                    }
                }

                // If at least 12 pairs of beacons are the same vector apart, they must be the overlap
                // between the 2 detectors
                for (Map.Entry<Vector, Integer> entry : offsetCounts.entrySet()) {
                    int count = entry.getValue();
                    if (count >= 12) {
                        Vector offset = entry.getKey();
                        VectorSet translatedVectorSet = rotatedVectorSet.translate(offset);
                        detector.setBeacons(translatedVectorSet);
                        detector.setPosition(offset);

                        return true;
                    }
                }
            }

            return false;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Detector> detectors = new ArrayList<>();
        while (sc.hasNext()) {
            sc.nextLine();  // "--- scanner n ---"
            VectorSet beacons = new VectorSet();
            while (sc.hasNext()) {
                String input = sc.nextLine();
                if (input.equals("")) {
                    break;
                }
                String[] coords = input.split(",");
                int x = Integer.parseInt(coords[0]);
                int y = Integer.parseInt(coords[1]);
                int z = Integer.parseInt(coords[2]);
                beacons.add(new Vector(x, y, z));
            }
            detectors.add(new Detector(beacons));
        }

        LinkedList<Detector> uncalibratedDetectors = new LinkedList<>(detectors);
        LinkedList<Detector> calibrationQueue = new LinkedList<>();  // Detectors ready to use for calibrating others
        Detector detector0 = detectors.get(0);
        uncalibratedDetectors.remove(detector0);
        calibrationQueue.add(detector0);
        detector0.setPosition(new Vector(0, 0, 0));

        // Calibrate every detector to use absolute coordinates (relative to detector 0)
        while (!uncalibratedDetectors.isEmpty() && !calibrationQueue.isEmpty()) {
            Detector calibrator = calibrationQueue.remove();
            ListIterator<Detector> it = uncalibratedDetectors.listIterator();
            while (it.hasNext()) {
                Detector detector = it.next();
                if (calibrator.calibrate(detector)) {
                    it.remove();
                    calibrationQueue.add(detector);
                }
            }
        }

        // Part 1
        VectorSet allBeacons = new VectorSet();
        for (Detector detector : detectors) {
            allBeacons.addVectorSet(detector.getBeacons());
        }

        System.out.println(allBeacons.size());

        // Part 2
        int maxDist = 0;
        for (int i = 0; i < detectors.size(); i++) {
            for (int j = i + 1; j < detectors.size(); j++) {
                Vector pos1 = detectors.get(i).getPosition();
                Vector pos2 = detectors.get(j).getPosition();
                maxDist = Math.max(pos1.manDist(pos2), maxDist);
            }
        }

        System.out.println(maxDist);
    }
}
