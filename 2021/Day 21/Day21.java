import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Scanner;

public class Day21 {
    public static class Player {
        private int pos;
        private int score = 0;

        public Player(int pos) {
            this.pos = pos;
        }

        public void move(int spaces) {
            pos = (pos + spaces) % 10;
            score += pos == 0 ? 10 : pos;
        }

        public boolean hasWon() {
            return score >= 1000;
        }

        public int getScore() {
            return score;
        }
    }

    public static void part1() {
        Scanner sc = new Scanner(System.in);
        LinkedList<Player> playerQueue = new LinkedList<>();
        while (sc.hasNext()) {
            int pos = Integer.parseInt(sc.nextLine().split(": ")[1]);
            playerQueue.add(new Player(pos));
        }

        int[] rolls = {1, 2, 3};
        int turns = 0;

        while (true) {
            turns += 3;
            Player player = playerQueue.remove();
            int spaces = 0;
            for (int i = 0; i < rolls.length; i++) {
                spaces += rolls[i];
                rolls[i] = (rolls[i] + 3) % 100;
                rolls[i] = rolls[i] == 0 ? 100 : rolls[i];
            }
            player.move(spaces);

            if (player.hasWon()) {
                break;
            }
            playerQueue.add(player);
        }

        System.out.println(playerQueue.remove().getScore() * turns);
    }

    public static class State {
        private final int pos1;
        private final int pos2;
        private final int score1;
        private final int score2;
        private final boolean isPlayer1Turn;
        private final long universes;  // How many copies of this game state represented

        public State(int pos1, int pos2) {
            this.pos1 = pos1;
            this.pos2 = pos2;
            this.score1 = 0;
            this.score2 = 0;
            this.isPlayer1Turn = true;
            this.universes = 1;
        }

        private State(int pos1, int pos2, int score1, int score2, boolean isPlayer1Turn, long universes) {
            this.pos1 = pos1;
            this.pos2 = pos2;
            this.score1 = score1;
            this.score2 = score2;
            this.isPlayer1Turn = isPlayer1Turn;
            this.universes = universes;
        }

        public State move(int spaces, int copies) {
            long newUniverses = universes * copies;
            if (isPlayer1Turn) {
                int newPos1 = (pos1 + spaces) % 10;
                int newScore1 = score1 + (newPos1 == 0 ? 10 : newPos1);
                return new State(newPos1, pos2, newScore1, score2, false, newUniverses);
            } else {
                int newPos2 = (pos2 + spaces) % 10;
                int newScore2 = score2 + (newPos2 == 0 ? 10 : newPos2);
                return new State(pos1, newPos2, score1, newScore2, true, newUniverses);
            }
        }

        public int winner() {
            if (score1 >= 21) {
                return 1;
            }
            if (score2 >= 21) {
                return 2;
            }
            return 0;
        }

        public long getUniverses() {
            return universes;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<State> states = new ArrayList<>();
        int startPos1 = Integer.parseInt(sc.nextLine().split(": ")[1]);
        int startPos2 = Integer.parseInt(sc.nextLine().split(": ")[1]);
        states.add(new State(startPos1, startPos2));

        // ROLL_COUNTS[i] is the number of universes where the three dice rolls sum to i
        final int[] ROLL_COUNTS = {0, 0, 0, 1, 3, 6, 7, 6, 3, 1};
        long player1Wins = 0;
        long player2Wins = 0;

        while (!states.isEmpty()) {
            ArrayList<State> newStates = new ArrayList<>();
            for (State state : states) {
                for (int i = 3; i <= 9; i++) {
                    State nextState = state.move(i, ROLL_COUNTS[i]);
                    int winner = nextState.winner();
                    if (winner != 0) {
                        if (winner == 1) {
                            player1Wins += nextState.getUniverses();
                        } else {
                            player2Wins += nextState.getUniverses();
                        }
                    } else {
                        newStates.add(nextState);
                    }
                }
            }

            states = newStates;
        }

        System.out.println(Math.max(player1Wins, player2Wins));
    }
}
