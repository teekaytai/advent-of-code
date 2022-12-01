import java.util.*;
import java.util.stream.Collectors;

import static java.util.Map.entry;

public class Day16 {
    private static final Map<String, String> hexToBits =
            Map.ofEntries(
                entry("0", "0000"),
                entry("1", "0001"),
                entry("2", "0010"),
                entry("3", "0011"),
                entry("4", "0100"),
                entry("5", "0101"),
                entry("6", "0110"),
                entry("7", "0111"),
                entry("8", "1000"),
                entry("9", "1001"),
                entry("A", "1010"),
                entry("B", "1011"),
                entry("C", "1100"),
                entry("D", "1101"),
                entry("E", "1110"),
                entry("F", "1111")
            );

    public static class BitStream {
        private final String bitString;
        private final int len;
        private int bitIndex = 0;

        public BitStream(String bitString) {
            this.bitString = bitString;
            this.len = bitString.length();
        }

        public boolean hasNext() {
            return len - bitIndex > 3;  // Some hex digit has not been read at all
        }

        public int getBitIndex() {
            return bitIndex;
        }

        // Return the next n bits as a string
        private String nextBits(int n) {
            String bits = bitString.substring(bitIndex, bitIndex + n);
            bitIndex += n;
            return bits;
        }

        // Return the next n bits as an int
        private int nextInt(int n) {
            String bits = nextBits(n);
            return Integer.parseInt(bits, 2);
        }

        public int nextVersionNum() {
            return nextInt(3);
        }

        public int nextPacketId() {
            return nextInt(3);
        }

        public int nextLengthType() {
            return nextInt(1);
        }

        public int nextLength(int lengthType) {
            return lengthType == 0 ? nextInt(15) : nextInt(11);
        }

        public long nextLiteral() {
            StringBuilder bits = new StringBuilder();
            while (nextBits(1).equals("1")) {
                bits.append(nextBits(4));
            }
            bits.append(nextBits(4));
            return Long.parseLong(bits.toString(), 2);
        }
    }

    // Part 1
    public static int totalVersion(BitStream bitStream) {
        int totalVersion = 0;
        while (bitStream.hasNext()) {
            int version = bitStream.nextVersionNum();
            totalVersion += version;
            int packetId = bitStream.nextPacketId();
            if (packetId == 4) {
                bitStream.nextLiteral();
            } else {
                bitStream.nextLength(bitStream.nextLengthType());
            }
        }

        return totalVersion;
    }

    // Part 2
    public static long evalBitStream(BitStream bitStream) {
        bitStream.nextVersionNum();
        int packetId = bitStream.nextPacketId();
        if (packetId == 4) {
            return bitStream.nextLiteral();
        }

        ArrayList<Long> operands = new ArrayList<>();
        int lengthType = bitStream.nextLengthType();
        if (lengthType == 0) {
            int numBits = bitStream.nextLength(lengthType);
            int lastBitIndex = bitStream.getBitIndex() + numBits;
            while (bitStream.getBitIndex() < lastBitIndex) {
                operands.add(evalBitStream(bitStream));
            }
        } else {
            int numPackets = bitStream.nextLength(lengthType);
            for (int i = 0; i < numPackets; i++) {
                operands.add(evalBitStream(bitStream));
            }
        }

        switch (packetId) {
            case 0:
                long sum = 0;
                for (long summand : operands) {
                    sum += summand;
                }
                return sum;
            case 1:
                long product = 1;
                for (long multiplicand : operands) {
                    product *= multiplicand;
                }
                return product;
            case 2:
                return Collections.min(operands);
            case 3:
                return Collections.max(operands);
            case 5:
                return operands.get(0) > operands.get(1) ? 1L : 0L;
            case 6:
                return operands.get(0) < operands.get(1) ? 1L : 0L;
            default: // 7
                return operands.get(0).equals(operands.get(1)) ? 1L : 0L;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] hexArray = sc.nextLine().split("");
        String bitString = Arrays.stream(hexArray).map(hexToBits::get).collect(Collectors.joining());
        BitStream bitStream = new BitStream(bitString);

        // System.out.println(totalVersion(bitStream));
        System.out.println(evalBitStream(bitStream));
    }
}
