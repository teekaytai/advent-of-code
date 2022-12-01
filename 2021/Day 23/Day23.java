import java.util.*;

public class Day23 {
    public static class State {
        public static final int NUM_ROOMS = 4;
        public static final int ROOM_SIZE = 4;
        private static final int HALLWAY_LEN = 11;
        private static final int[] ROOM_X = {2, 4, 6, 8};  // Horizontal position of each room

        private static final int EMPTY_SPACE = -1;  // Empty spaces are represented by -1 in rooms and hallway
        private static final int ROOM_DONE = -1;  // The room state when it is filled with the correct amphipods
        private static final int ROOM_HAS_FOREIGN = -2;  // The room state when foreign amphipods are still inside

        private boolean done;
        private int energy;

        // Amphipods are represented as ints 0-3, empty spaces as -1
        private final int[][] rooms;  // Each row represents a room, starting at the outermost amphipod in room A
        private final int[] hallway;

        // A room's state is -1 if the room is already done, -2 if foreign amphipods are still in room,
        // and the next index of the room an amphipod should move into otherwise (max 3 if the room is empty)
        private final int[] roomStates;

        // Used for the starting state
        public State(int[][] rooms) {
            this.done = false;
            this.energy = 0;
            this.rooms = rooms;
            this.hallway = new int[HALLWAY_LEN];
            Arrays.fill(hallway, EMPTY_SPACE);
            roomStates = new int[NUM_ROOMS];
            for (int r = 0; r < NUM_ROOMS; r++) {
                updateRoomState(r);
            }
        }

        // Make a deep copy of the input state
        private State(State state) {
            this.done = state.done;
            this.energy = state.energy;
            this.rooms = new int[NUM_ROOMS][];
            for (int r = 0; r < NUM_ROOMS; r++) {
                this.rooms[r] = Arrays.copyOf(state.rooms[r], ROOM_SIZE);
            }
            this.hallway = Arrays.copyOf(state.hallway, HALLWAY_LEN);
            this.roomStates = Arrays.copyOf(state.roomStates, NUM_ROOMS);
        }

        public boolean isDone() {
            return done;
        }

        public int getEnergy() {
            return energy;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            State state = (State) o;
            return energy == state.energy && Arrays.deepEquals(rooms, state.rooms) && Arrays.equals(hallway, state.hallway);
        }

        @Override
        public int hashCode() {
            int result = Objects.hash(energy);
            result = 31 * result + Arrays.deepHashCode(rooms);
            result = 31 * result + Arrays.hashCode(hallway);
            return result;
        }

        public ArrayList<State> possibleNextStates() {
            ArrayList<State> nextStates = new ArrayList<>();
            moveOutOfRoom(nextStates);
            moveHallwayToRoom(nextStates);
            return nextStates;
        }

        // Try moving each amphipod in a room to the hallway or its proper room
        private void moveOutOfRoom(ArrayList<State> nextStates) {
            for (int r = 0; r < NUM_ROOMS; r++) {
                if (roomStates[r] != ROOM_HAS_FOREIGN) {
                    // Room is empty or only contains correct amphipods, no point moving them out
                    continue;
                }

                // Identify outermost amphipod in room r
                int c = 0;
                while (rooms[r][c] == EMPTY_SPACE) {
                    c++;
                }
                int amphipod = rooms[r][c];

                moveRoomToHallway(nextStates, r, c, amphipod);
                moveRoomToRoom(nextStates, r, c, amphipod);
            }
        }

        // Try moving an amphipod from room r to the hallway
        private void moveRoomToHallway(ArrayList<State> nextStates, int r, int c, int amphipod) {
            // Moving left
            for (int h = ROOM_X[r]; h >= 0; h--) {
                if (hallway[h] != EMPTY_SPACE) {
                    // Blocked by another amphipod, cannot proceed further in this direction
                    break;
                }
                if (isIllegalHallway(h)) {
                    continue;
                }

                State newState = new State(this);

                newState.rooms[r][c] = EMPTY_SPACE;
                newState.updateRoomState(r);  // Update room state of room amphipod just left
                newState.hallway[h] = amphipod;

                int stepsTaken = (c + 1) + (ROOM_X[r] - h);
                newState.energy += stepsTaken * Math.pow(10, amphipod);

                nextStates.add(newState);
            }

            // Moving right
            for (int h = ROOM_X[r]; h < HALLWAY_LEN; h++) {
                if (hallway[h] != EMPTY_SPACE) {
                    // Blocked by another amphipod, cannot proceed further in this direction
                    break;
                }
                if (isIllegalHallway(h)) {
                    continue;
                }

                State newState = new State(this);

                newState.rooms[r][c] = EMPTY_SPACE;
                newState.updateRoomState(r);  // Update room state of room amphipod just left
                newState.hallway[h] = amphipod;

                int stepsTaken = (c + 1) + (h - ROOM_X[r]);
                newState.energy += stepsTaken * Math.pow(10, amphipod);

                nextStates.add(newState);
            }
        }

        // Try moving an amphipod from room r to its own room
        private void moveRoomToRoom(ArrayList<State> nextStates, int r, int c, int amphipod) {
            int xMin = Math.min(ROOM_X[r], ROOM_X[amphipod]);
            int xMax = Math.max(ROOM_X[r], ROOM_X[amphipod]);
            if (roomStates[amphipod] != ROOM_HAS_FOREIGN && hallwayClear(xMin, xMax)) {
                State newState = new State(this);

                newState.rooms[r][c] = EMPTY_SPACE;
                newState.updateRoomState(r);  // Update room state of room amphipod just left
                newState.rooms[amphipod][roomStates[amphipod]] = amphipod;
                newState.roomStates[amphipod]--;  // Update index in room where next amphipod should move to

                int stepsTaken = (c + 1) + (xMax - xMin) + (roomStates[amphipod] + 1);
                newState.energy += stepsTaken * Math.pow(10, amphipod);

                nextStates.add(newState);
            }
        }

        // Try moving each amphipod from the hallway into its room
        private void moveHallwayToRoom(ArrayList<State> nextStates) {
            for (int h = 0; h < HALLWAY_LEN; h++) {
                int amphipod = hallway[h];
                if (amphipod == EMPTY_SPACE || roomStates[amphipod] == ROOM_HAS_FOREIGN) {
                    continue;
                }

                int xMin;
                int xMax;
                if (h < ROOM_X[amphipod]) {
                    xMin = h + 1;
                    xMax = ROOM_X[amphipod];
                } else {
                    xMin = ROOM_X[amphipod];
                    xMax = h - 1;
                }

                if (hallwayClear(xMin, xMax)) {
                    State newState = new State(this);

                    newState.hallway[h] = EMPTY_SPACE;
                    newState.rooms[amphipod][roomStates[amphipod]] = amphipod;
                    newState.roomStates[amphipod]--;  // Update index in room where next amphipod should move to

                    int stepsTaken = (xMax - xMin + 1) + (roomStates[amphipod] + 1);
                    newState.energy += stepsTaken * Math.pow(10, amphipod);

                    if (Arrays.stream(newState.roomStates).allMatch(roomState -> roomState == ROOM_DONE)) {
                        newState.done = true;
                    }

                    nextStates.add(newState);
                }
            }
        }

        // Checks if hallway position is in front of a room
        private static boolean isIllegalHallway(int h) {
            return h % 2 == 0 && h != 0 && h != HALLWAY_LEN - 1;
        }

        // Check hallway from xMin to xMax is clear
        private boolean hallwayClear(int xMin, int xMax) {
            for (int h = xMin; h <= xMax; h++) {
                if (hallway[h] != EMPTY_SPACE) {
                    return false;
                }
            }
            return true;
        }

        // Used to update the room state of room r
        private void updateRoomState(int r) {
            roomStates[r] = ROOM_DONE;
            for (int c = 0; c < ROOM_SIZE; c++) {
                if (rooms[r][c] == EMPTY_SPACE) {
                    // Keep the index of the innermost vacant index
                    roomStates[r] = c;
                } else if (rooms[r][c] != r) {  // Foreign amphipod in room
                    roomStates[r] = -2;
                    break;
                }
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] startRooms = new int[State.NUM_ROOMS][State.ROOM_SIZE];
        sc.nextLine();
        sc.nextLine();
        for (int c = 0; c < State.ROOM_SIZE; c++) {
            String row = sc.nextLine();
            for (int r = 0; r < State.NUM_ROOMS; r++) {
                startRooms[r][c] = row.charAt(2 * r + 3) - 'A';  // 'A' -> 0, 'B' -> 1 etc.
            }
        }

        Stack<State> newStates = new Stack<>();
        HashSet<State> seenStates = new HashSet<>();  // Ensure do not visit same state twice
        State startState = new State(startRooms);
        newStates.push(startState);
        seenStates.add(startState);
        int lowestEnergy = Integer.MAX_VALUE;

        while (!newStates.empty()) {
            State state = newStates.pop();
            for (State nextState : state.possibleNextStates()) {
                if (nextState.isDone()) {
                    lowestEnergy = Math.min(nextState.getEnergy(), lowestEnergy);
                } else if (nextState.getEnergy() < lowestEnergy && !seenStates.contains(nextState)) {
                    newStates.push(nextState);
                    seenStates.add(nextState);
                }
            }
        }

        System.out.println(lowestEnergy);
    }
}
