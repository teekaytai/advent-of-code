import java.util.ArrayList;
import java.util.Scanner;

public class Day24 {
    public static class Expression {
        private static final int CONSTANT = 0;
        private static final int VARIABLE = 1;
        private static final int OPERATION = 2;
        public static final Expression ZERO = new Expression(0);
        public static final Expression ONE = new Expression(1);

        int constant;
        char variable;
        char op;
        Expression exp1;
        Expression exp2;
        int type;

        public Expression(int constant) {
            this.constant = constant;
            this.type = CONSTANT;
        }

        public Expression(char variable) {
            this.variable = variable;
            this.type = VARIABLE;
        }

        private Expression(char op, Expression exp1, Expression exp2) {
            this.op = op;
            this.exp1 = exp1;
            this.exp2 = exp2;
            this.type = OPERATION;
        }

        @Override
        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            addToString(stringBuilder);
            return stringBuilder.toString();
        }

        public void addToString(StringBuilder stringBuilder) {
            if (type == CONSTANT) {
                stringBuilder.append(constant);
            } else if (type == VARIABLE) {
                stringBuilder.append(variable);
            } else {
                stringBuilder.append("(");
                exp1.addToString(stringBuilder);
                stringBuilder.append(" ");
                stringBuilder.append(op);
                stringBuilder.append(" ");
                exp2.addToString(stringBuilder);
                stringBuilder.append(")");
            }
        }

        public Expression add(Expression exp) {
            if (this.isZero()) {
                return exp;
            }
            if (exp.isZero()) {
                return this;
            }
            if (this.type == CONSTANT && exp.type == CONSTANT) {
                return new Expression(this.constant + exp.constant);
            }

            return new Expression('+', this, exp);
        }

        public Expression mul(Expression exp) {
            if (this.isZero() || exp.isZero()) {
                return ZERO;
            }
            if (this.isOne()) {
                return exp;
            }
            if (exp.isOne()) {
                return this;
            }
            if (this.type == CONSTANT && exp.type == CONSTANT) {
                return new Expression(this.constant * exp.constant);
            }

            return new Expression('*', this, exp);
        }

        public Expression div(Expression exp) {
            if (this.isZero()) {
                return ZERO;
            }
            if (exp.isOne()) {
                return this;
            }
            if (this.type == CONSTANT && exp.type == CONSTANT) {
                return new Expression(this.constant / exp.constant);
            }

            return new Expression('/', this, exp);
        }

        public Expression mod(Expression exp) {
            if (this.isZero()) {
                return ZERO;
            }
            if (this.type == CONSTANT && exp.type == CONSTANT) {
                return new Expression(this.constant % exp.constant);
            }

            return new Expression('%', this, exp);
        }

        public Expression eql(Expression exp) {
            if (this.type == CONSTANT && exp.type == CONSTANT) {
                return this.constant == exp.constant ? ONE : ZERO;
            }

            return new Expression('=', this, exp);
        }

        private boolean isZero() {
            return type == CONSTANT && constant == 0;
        }

        private boolean isOne() {
            return type == CONSTANT && constant == 1;
        }
    }

    public static class Registry {
        Expression[] registers;

        public Registry() {
            registers = new Expression[4];
            for (int i = 0; i < 4; i++) {
                registers[i] = new Expression(0);
            }
        }

        public Expression getRegister(String r) {
            return registers[r.charAt(0) - 'w'];  // registers[0] is register 'w'
        }

        public void setRegister(String r, Expression exp) {
            registers[r.charAt(0) - 'w'] = exp;  // registers[0] is register 'w'
        }
    }

    // The instructions noticeably repeat a similar behaviour several times: read a value into register w,
    // reset the values in registers x and y, and perform some calculation to update the value in register z.
    // This function runs the instructions and prints out the expression in the z register after each "round"
    public static Expression run(String[][] instructions, String input) {
        Registry registry = new Registry();
        int inputIndex = 0;

        for (String[] instruction : instructions) {
            if (instruction[0].equals("inp")) {
                if (inputIndex > 0) {
                    // Print out the intermediate expression in register z after each "round"
                    System.out.printf("%c = %s\n", 'A' + inputIndex - 1, registry.getRegister("z"));
                    if (registry.getRegister("z").type != Expression.CONSTANT) {
                        // Replace the expression in z with a variable name to simplify subsequent expressions
                        registry.setRegister("z", new Expression((char) ('A' + inputIndex - 1)));
                    }
                }

                char in = input.charAt(inputIndex);
                inputIndex++;
                Expression inputExp;
                if (Character.isDigit(in)) {
                    inputExp = new Expression( in - '0');
                } else {
                    // Input is a variable name
                    inputExp = new Expression(in);
                }
                registry.setRegister(instruction[1], inputExp);
            } else {
                Expression exp1 = registry.getRegister(instruction[1]);
                Expression exp2;
                if (instruction[2].matches("[w-z]")) {
                    exp2 = registry.getRegister(instruction[2]);
                } else {
                    exp2 = new Expression(Integer.parseInt(instruction[2]));
                }
                Expression result = switch (instruction[0]) {
                    case "add" -> exp1.add(exp2);
                    case "mul" -> exp1.mul(exp2);
                    case "div" -> exp1.div(exp2);
                    case "mod" -> exp1.mod(exp2);
                    case "eql" -> exp1.eql(exp2);
                    default -> throw new IllegalArgumentException("Unexpected instruction type");
                };
                registry.setRegister(instruction[1], result);
            }
        }

        return registry.getRegister("z");
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<String[]> instructionsList = new ArrayList<>();
        while (sc.hasNext()) {
            String[] instruction = sc.nextLine().split(" ");
            instructionsList.add(instruction);
        }
        String[][] instructions = instructionsList.toArray(new String[0][]);

        // modelNum can contain digits or single-letter variables or both
        String modelNum = "abcdefghijklmn";
        // String modelNum = "1234567891234n";
        Expression result = run(instructions, modelNum);
        System.out.printf("N = %s\n", result);
    }
}
