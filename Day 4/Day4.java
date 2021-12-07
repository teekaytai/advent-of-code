import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Day4 {
    public static class BingoBoard {
        int[][] board;
        int score = 0;
        byte[] rowMarked = {0, 0, 0, 0, 0}; // How many entries in row marked
        byte[] colMarked = {0, 0, 0, 0, 0}; // How many entries in col marked
        
        public BingoBoard(int[][] board) {
            this.board = board;
            for (int r = 0; r < 5; r++) {
                for (int c = 0; c < 5; c++) {
                    this.score += board[r][c];
                }
            }
        }

        // Mark a number and return score if bingo achieved, otherwise return -1
        public int markNumber(int num) {
            for (int r = 0; r < 5; r++) {
                for (int c = 0; c < 5; c++) {
                    if (board[r][c] == num) {
                        this.score -= num;
                        rowMarked[r]++;
                        colMarked[c]++;
                        if (rowMarked[r] == 5 || colMarked[c] == 5) {
                            return this.score * num;
                        } else {
                            return -1;
                        }
                    }
                }
            }
            return -1;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        int[] drawOrder = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt).toArray();
        
        ArrayList<BingoBoard> bingoBoardsList = new ArrayList<BingoBoard>();
        
        while (sc.hasNext()) {
            int[][] board = new int[5][];
            for (int r = 0; r < 5; r++) {
                board[r] = new int[5];
                for (int c = 0; c < 5; c++) {
                    board[r][c] = sc.nextInt();
                }
            }
            bingoBoardsList.add(new BingoBoard(board));
        }
        
        BingoBoard[] bingoBoards = bingoBoardsList.toArray(new BingoBoard[0]);

        // Part 1
        // outerLoop:
        // for (int num : drawOrder) {
        //     for (BingoBoard bingoBoard : bingoBoards) {
        //         int score = bingoBoard.markNumber(num);
        //         if (score != -1) {
        //             System.out.println(score);
        //             break outerLoop;
        //         }
        //     }
        // }

        // Part 2
        int boardsLeft = bingoBoards.length;
        outerLoop:
        for (int num : drawOrder) {
            for (int i = 0; i < boardsLeft; i++) {
                BingoBoard bingoBoard = bingoBoards[i];
                int score = bingoBoard.markNumber(num);
                if (score != -1) {
                    if (boardsLeft == 1) {
                        System.out.println(score);
                        break outerLoop;
                    } else {
                        // Swap board to end of array and never look at it again
                        bingoBoards[i] = bingoBoards[boardsLeft - 1];
                        bingoBoards[boardsLeft - 1] = bingoBoard;
                        boardsLeft--;
                        i--;
                    }
                }
            }
        }

        sc.close();
    }
}