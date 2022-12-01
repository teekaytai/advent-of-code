import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Day12 {
    public static boolean isSmallCave(String vertex) {
        return Character.isLowerCase(vertex.charAt(0)) && !vertex.equals("start") && !vertex.equals("end");
    }

    // DFS
    public static int countPaths(HashMap<String, ArrayList<String>> adjList,
                                 HashMap<String, Boolean> smallCavesVisited,
                                 boolean twiceVisited,  // Part 2
                                 String currVertex) {
        if (currVertex.equals("end")) {
            return 1;
        }

        int total = 0;

        for (String adjVertex : adjList.get(currVertex)) {
            if (adjVertex.equals("start")) {
                continue;
            }

            if (isSmallCave(adjVertex)) {
                if (smallCavesVisited.get(adjVertex)) {
                    // Part 2
                    // Small cave already visited, need to expend single twiceVisited to proceed
                    if (!twiceVisited) {
                        total += countPaths(adjList, smallCavesVisited, true, adjVertex);
                    }
                } else {
                    smallCavesVisited.put(adjVertex, true);
                    total += countPaths(adjList, smallCavesVisited, twiceVisited, adjVertex);
                    smallCavesVisited.put(adjVertex, false);
                }
            } else {
                total += countPaths(adjList, smallCavesVisited, twiceVisited, adjVertex);
            }
        }

        return total;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        HashMap<String, ArrayList<String>> adjList = new HashMap<>();
        HashMap<String, Boolean> smallCavesVisited = new HashMap<>();

        while (sc.hasNext()) {
            String[] edge = sc.nextLine().split("-");
            String vertex1 = edge[0];
            String vertex2 = edge[1];

            if (!adjList.containsKey(vertex1)) {
                adjList.put(vertex1, new ArrayList<>());
            }
            if (!adjList.containsKey(vertex2)) {
                adjList.put(vertex2, new ArrayList<>());
            }
            adjList.get(vertex1).add(vertex2);
            adjList.get(vertex2).add(vertex1);

            if (isSmallCave(vertex1)) {
                smallCavesVisited.put(vertex1, false);
            }
            if (isSmallCave(vertex2)) {
                smallCavesVisited.put(vertex2, false);
            }
        }

        System.out.println(countPaths(adjList, smallCavesVisited, false, "start"));
    }
}
