import java.util.ArrayList;
import java.util.Scanner;

public class Day18 {
    // An element is either a number or another pair. The root pair will also be contained in an element
    public static class Element {
        private int num;  // Note: num may hold a value even if this is a pair. The value should be ignored
        private Pair pair = null;
        private Element parentElement = null;
        private boolean isLeftChild;

        public Element(int num) {
            this.num = num;
        }

        public Element(Pair p) {
            pair = p;
            p.left.parentElement = this;
            p.right.parentElement = this;
        }

        // Return a deep copy of this element
        public Element copy() {
            return isPair() ? new Element(pair.copy()) : new Element(num);
        }

        // Parses a complete element (pair or number) from scanner
        public static Element parse(Scanner sc) {
            String s = sc.next();
            if (s.equals("[")) {
                Element left = Element.parse(sc);
                sc.next();  // ","
                Element right = Element.parse(sc);
                sc.next();  // "]"
                return new Element(new Pair(left, right));
            } else {
                return new Element(Integer.parseInt(s));
            }
        }

        @Override
        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            addToString(stringBuilder);
            return stringBuilder.toString();
        }

        public void addToString(StringBuilder stringBuilder) {
            if (isPair()) {
                pair.addToString(stringBuilder);
            } else {
                stringBuilder.append(num);
            }
        }

        public int magnitude() {
            return isPair() ? pair.magnitude() : num;
        }

        private boolean isNotRoot() {
            return parentElement != null;
        }

        private boolean isPair() {
            return pair != null;
        }

        public Element addElement(Element e) {
            Element newElement = new Element(new Pair(this, e));
            newElement.reduce();
            return newElement;
        }

        private void reduce() {
            reduceExplosions(0);
            boolean splitsRemaining = true;
            while (splitsRemaining) {
                splitsRemaining = reduceSplit(0);
            }
        }

        // Explode every pair at depth 4
        public void reduceExplosions(int depth) {
            if (isPair()) {
                if (depth >= 4) {
                    explode();
                } else {
                    pair.reduceExplosions(depth + 1);
                }
            }
        }

        private void explode() {
            // Increase the number immediately to the left of this exploding pair if there is one
            Element ancestor = this;
            // Find the closest ancestor who is a right child
            while (ancestor.isNotRoot() && ancestor.isLeftChild) {
                ancestor = ancestor.parentElement;
            }
            if (ancestor.isNotRoot()) {
                // Increase the rightmost number in the ancestor's left sibling
                ancestor.parentElement.pair.left.incRightmost(this.pair.left.num);
            }

            // Increase the number immediately to the right of this exploding pair if there is one
            ancestor = this;
            // Find the closest ancestor who is a left child
            while (ancestor.isNotRoot() && !ancestor.isLeftChild) {
                ancestor = ancestor.parentElement;
            }
            if (ancestor.isNotRoot()) {
                // Increase the leftmost number in the ancestor's right sibling
                ancestor.parentElement.pair.right.incLeftmost(this.pair.right.num);
            }

            // Convert this element into a number
            num = 0;
            pair = null;
        }

        // Splits the leftmost number >= 10 if any and returns true if a split was done
        // Also explodes the newly-split pair if necessary
        public boolean reduceSplit(int depth) {
            if (isPair()) {
                return pair.reduceSplit(depth + 1);
            } else {
                if (num >= 10) {
                    split();
                    if (depth >= 4) {
                        explode();
                    }
                    return true;
                }
                return false;
            }
        }

        private void split() {
            Element left = new Element(num / 2);
            Element right = new Element((int) Math.ceil(num / 2.0));
            pair = new Pair(left, right);
            left.parentElement = this;
            right.parentElement = this;
        }

        public void incRightmost(int n) {
            if (isPair()) {
                pair.incRightmost(n);
            } else {
                num += n;
            }
        }

        public void incLeftmost(int n) {
            if (isPair()) {
                pair.incLeftmost(n);
            } else {
                num += n;
            }
        }
    }

    public static class Pair {
        private final Element left;
        private final Element right;

        public Pair(Element left, Element right) {
            this.left = left;
            left.isLeftChild = true;
            this.right = right;
            right.isLeftChild = false;
        }

        // Return a deep copy of this pair
        public Pair copy() {
            return new Pair(left.copy(), right.copy());
        }

        @Override
        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            addToString(stringBuilder);
            return stringBuilder.toString();
        }

        public void addToString(StringBuilder stringBuilder) {
            stringBuilder.append('[');
            left.addToString(stringBuilder);
            stringBuilder.append(',');
            right.addToString(stringBuilder);
            stringBuilder.append(']');
        }

        public int magnitude() {
            return 3 * left.magnitude() + 2 * right.magnitude();
        }

        // Explode every pair at depth 4
        public void reduceExplosions(int depth) {
            left.reduceExplosions(depth);
            right.reduceExplosions(depth);
        }

        // Splits the leftmost number >= 10 if any and returns true if a split was done
        // The newly-split pair also immediately explodes if necessary
        public boolean reduceSplit(int depth) {
            return left.reduceSplit(depth) || right.reduceSplit(depth);
        }

        public void incRightmost(int n) {
            right.incRightmost(n);
        }

        public void incLeftmost(int n) {
            left.incLeftmost(n);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        sc.useDelimiter("");  // Read character by character

        // Part 1
        /*
        Element snailFish = Element.parse(sc);
        while (sc.hasNext()) {
            sc.next();  // "\r"
            sc.next();  // "\n"
            snailFish = snailFish.addElement(Element.parse(sc));
        }

        System.out.println(snailFish.magnitude());
        */

        // Part 2
        ArrayList<Element> snailFishesList = new ArrayList<>();
        snailFishesList.add(Element.parse(sc));
        while (sc.hasNext()) {
            sc.next();  // "\r"
            sc.next();  // "\n"
            snailFishesList.add(Element.parse(sc));
        }
        Element[] snailFishes = snailFishesList.toArray(new Element[0]);

        int maxMagnitude = 0;
        for (int i = 0; i < snailFishes.length; i++) {
            for (int j = 0; j < snailFishes.length; j++) {
                if (i != j) {
                    Element snailFishSum = snailFishes[i].copy().addElement(snailFishes[j].copy());
                    maxMagnitude = Math.max(snailFishSum.magnitude(), maxMagnitude);
                }
            }
        }

        System.out.println(maxMagnitude);
    }
}
