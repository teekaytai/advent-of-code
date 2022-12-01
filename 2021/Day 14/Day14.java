import java.util.*;

public class Day14 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String startPolymer = sc.nextLine();
        HashMap<String, Long> pairCounts = new HashMap<>();  // Maps pairs to their number of occurrences
        for (int i = 0, L = startPolymer.length(); i < L - 1; i++) {
            pairCounts.merge(startPolymer.substring(i, i + 2), 1L, Long::sum);
        }

        sc.nextLine();  // Blank line

        HashMap<String, String[]> rules = new HashMap<>();  // Maps start pairs to the two resulting pairs
        while (sc.hasNext()) {
            String[] rule = sc.nextLine().split(" -> ");
            String startPair = rule[0];
            String addedLetter = rule[1];
            String[] newPairs = {startPair.charAt(0) + addedLetter, addedLetter + startPair.charAt(1)};

            rules.put(startPair, newPairs);
        }

        final int STEPS = 40;
        for (int i = 0; i < STEPS; i++) {
            HashMap<String, Long> nextPairCounts = new HashMap<>();
            for (Map.Entry<String, Long> entry : pairCounts.entrySet()) {
                String startPair = entry.getKey();
                long startPairCount = entry.getValue();
                String[] newPairs = rules.get(startPair);

                // The startPair's current count contributes to the pairCounts of the new pairs
                nextPairCounts.merge(newPairs[0], startPairCount, Long::sum);
                nextPairCounts.merge(newPairs[1], startPairCount, Long::sum);
            }

            pairCounts = nextPairCounts;
        }

        HashMap<Character, Long> charCounts = new HashMap<>();
        // Note that counting chars in pairs double counts every char except the first and last
        for (Map.Entry<String, Long> entry : pairCounts.entrySet()) {
            String pair = entry.getKey();
            Long count = entry.getValue();
            charCounts.merge(pair.charAt(0), count, Long::sum);
            charCounts.merge(pair.charAt(1), count, Long::sum);
        }
        charCounts.merge(startPolymer.charAt(0), 1L, Long::sum);
        charCounts.merge(startPolymer.charAt(startPolymer.length() - 1), 1L, Long::sum);

        long maxQuantity = Collections.max(charCounts.values()) / 2;
        long minQuantity = Collections.min(charCounts.values()) / 2;
        System.out.println(maxQuantity - minQuantity);
    }



    // Less efficient solution by direct simulation used for part 1
    public static class PolymerLinkedList {
        private static final HashMap<String, String> insertionRules = new HashMap<>();

        private final Node root;
        private final HashMap<String, Integer> elementCounts = new HashMap<>();

        public PolymerLinkedList(String polymer) {
            String[] elements = polymer.split("");
            root = new Node(elements[0]);
            elementCounts.merge(elements[0], 1 , Integer::sum);
            Node curr = root;
            for (int i = 1; i < elements.length; i++) {
                Node next = new Node(elements[i]);
                elementCounts.merge(elements[i], 1 , Integer::sum);
                curr.setNext(next);
                curr = next;
            }
        }

        public static void addInsertionRule(String pair, String insertedElement) {
            insertionRules.put(pair, insertedElement);
        }

        private void addAfter(String element, Node node) {
            Node newNode = new Node(element, node.getNext());
            elementCounts.merge(element, 1 , Integer::sum);
            node.setNext(newNode);
        }

        // Iterate through list and add new nodes along the way
        public void step() {
            Node curr = root;
            Node next = curr.getNext();
            while (next != null) {
                String newElement = insertionRules.get(curr.getVal() + next.getVal());
                addAfter(newElement, curr);
                curr = next;
                next = next.getNext();
            }
        }

        public HashMap<String, Integer> getCounts() {
            return elementCounts;
        }

        private static class Node {
            private final String val;
            private Node next;

            public Node(String val) {
                this.val = val;
                this.next = null;
            }

            public Node(String val, Node next) {
                this.val = val;
                this.next = next;
            }

            public String getVal() {
                return val;
            }

            public Node getNext() {
                return next;
            }

            public void setNext(Node next) {
                this.next = next;
            }
        }
    }

    public static void part1() {
        Scanner sc = new Scanner(System.in);
        PolymerLinkedList polymer = new PolymerLinkedList(sc.nextLine());
        sc.nextLine();  // Blank line
        while (sc.hasNext()) {
            String[] insertionRule = sc.nextLine().split(" -> ");
            PolymerLinkedList.addInsertionRule(insertionRule[0], insertionRule[1]);
        }

        final int STEPS = 10;
        for (int i = 0; i < STEPS; i++) {
            polymer.step();
        }

        HashMap<String, Integer> counts = polymer.getCounts();
        int maxQuantity = Collections.max(counts.values());
        int minQuantity = Collections.min(counts.values());
        System.out.println(maxQuantity - minQuantity);
    }
}
