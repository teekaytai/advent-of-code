import java.util.*;

public class Day17 {
    public static class Velocity {
        int vx;
        int vy;

        public Velocity(int vx, int vy) {
            this.vx = vx;
            this.vy = vy;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Velocity pair = (Velocity) o;
            return vx == pair.vx && vy == pair.vy;
        }

        @Override
        public int hashCode() {
            return Objects.hash(vx, vy);
        }
    }

    // For part 1, as long as the X range contains a triangle number T(n), a horizontal speed can be chosen such that
    // the probe finishes after n steps in the target area with 0 horizontal speed.
    // Then, any vertical speed that hits the target area after at least n steps would work.
    // Given a target area with negative y value, to reach maximum height, select a vertical speed of -targetMinY - 1.
    // The probe will go up and down, and there will be a step where the probe exactly hits y = 0 again, before moving
    // to targetMinY on its next step.
    // Hence, the maximum height would be T(-targetMinY - 1)

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // target area: x= targetMinX .. targetMaxX , y= targetMinY .. targetMaxY
        String[] input = sc.nextLine().split("=|\\.\\.|,");
        int targetMinX = Integer.parseInt(input[1]);
        int targetMaxX = Integer.parseInt(input[2]);
        int targetMinY = Integer.parseInt(input[4]);
        int targetMaxY = Integer.parseInt(input[5]);

        // Maps number of steps taken to a list of possible vertical speeds that end in target range
        // after that many steps
        HashMap<Integer, ArrayList<Integer>> stepsToVertSpeeds = new HashMap<>();

        int vy = -targetMinY - 1;  // the probe's starting y velocity, initially set to the maximum (see part 1)
        int maxStepsY = (vy + 1) * 2;   // maximum steps the probe can move while staying above targetMinY
        int endMinY = targetMinY;       // the probe's final y value after moving maxStepsY
        int minStepsY = maxStepsY;      // minimum steps the probe must move to go below targetMaxY
        int endMaxY = targetMinY;       // the probe's final y value after moving minStepsY
        while (vy >= targetMinY) {
            for (int i = minStepsY; i <= maxStepsY; i++) {
                if (!stepsToVertSpeeds.containsKey(i)) {
                    stepsToVertSpeeds.put(i, new ArrayList<>());
                }
                stepsToVertSpeeds.get(i).add(vy);
            }

            vy--;

            // New endYs after decreasing vy by 1 and fixing steps
            endMinY -= maxStepsY;
            endMaxY -= minStepsY;
            while (endMinY < targetMinY) {
                endMinY -= vy - maxStepsY + 1;  // Undo last step to raise endMinY above targetMinY
                maxStepsY--;
            }
            while (endMaxY - (vy - minStepsY + 1) <= targetMaxY) {
                endMaxY -= vy - minStepsY + 1;  // Undo last step to raise endMaxY while staying below targetMaxY
                minStepsY--;
            }
        }


        // Maps number of steps taken to a list of possible horizontal speeds that end in target range
        // after that many steps, excluding those that eventually finish with 0 speed within the range
        HashMap<Integer, ArrayList<Integer>> stepsToHorizSpeeds = new HashMap<>();

        // Maps number of steps to a list of possible horizontal speeds that stop in the target range.
        // Each speed is stored under its minimum number of steps required to reach the range
        HashMap<Integer, ArrayList<Integer>> stepsToHaltingHorizSpeeds = new HashMap<>();

        int vx = targetMaxX;        // the probe's starting x velocity, initially set to the maximum possible
        int maxStepsX = 1;          // maximum steps the probe can move while staying behind targetMaxX
        int endMaxX = targetMaxX;   // the probe's final x value after moving maxStepsX
        int minStepsX = 1;          // minimum steps the probe must move to go beyond targetMinX
        int endMinX = targetMaxX;   // the probe's final x value after moving minStepsX

        while (endMinX >= targetMinX) { // Stop when probe is finishing with 0 speed before target area
            if (maxStepsX >= vx) {
                // Probe stops moving in target range
                if (!stepsToHaltingHorizSpeeds.containsKey(minStepsX)) {
                    stepsToHaltingHorizSpeeds.put(minStepsX, new ArrayList<>());
                }
                stepsToHaltingHorizSpeeds.get(minStepsX).add(vx);
            } else {
                for (int i = minStepsX; i <= maxStepsX; i++) {
                    if (!stepsToHorizSpeeds.containsKey(i)) {
                        stepsToHorizSpeeds.put(i, new ArrayList<>());
                    }
                    stepsToHorizSpeeds.get(i).add(vx);
                }
            }

            vx--;

            // Only happens in later phase when probe is stopping within the target x range
            if (maxStepsX > vx) {
                endMaxX -= 1;
                maxStepsX--;
            }

            // New endXs after decreasing vx by 1 and fixing steps
            endMaxX -= maxStepsX;
            endMinX -= minStepsX;
            while (maxStepsX < vx && endMaxX + (vx - maxStepsX) <= targetMaxX) {
                endMaxX += vx - maxStepsX;  // Add step to increase endMaxX while staying behind targetMaxX
                maxStepsX++;
            }
            while (minStepsX < vx && endMinX < targetMinX) {
                endMinX += vx - minStepsX;  // Add step to increase endMinX beyond targetMinX
                minStepsX++;
            }
        }


        // Steps taken for horizontal and vertical position to reach target must be equal.
        // 2 types of shots: Those where the horizontal velocity hits 0 and those where it doesn't
        HashSet<Velocity> possibleSpeedPairs = new HashSet<>();

        // Probe's horizontal speed reaches 0 beyond target x range => steps need to match up
        for (Map.Entry<Integer, ArrayList<Integer>> entry : stepsToHorizSpeeds.entrySet()) {
            int steps = entry.getKey();
            ArrayList<Integer> vxs = entry.getValue();
            for (int vY : stepsToVertSpeeds.get(steps)) {
                for (int vX : vxs) {
                    possibleSpeedPairs.add(new Velocity(vX, vY));
                }
            }
        }

        // Probe's horizontal speed reaches 0 within target X range => any greater or equal number of steps works
        for (Map.Entry<Integer, ArrayList<Integer>> entryX : stepsToHaltingHorizSpeeds.entrySet()) {
            int stepsX = entryX.getKey();
            ArrayList<Integer> vxs = entryX.getValue();
            for (Map.Entry<Integer, ArrayList<Integer>> entryY : stepsToVertSpeeds.entrySet()) {
                int stepsY = entryY.getKey();
                ArrayList<Integer> vys = entryY.getValue();
                if (stepsY >= stepsX) {
                    for (int vX : vxs) {
                        for (int vY : vys) {
                            possibleSpeedPairs.add(new Velocity(vX, vY));
                        }
                    }
                }
            }
        }

        System.out.println(possibleSpeedPairs.size());
    }
}
