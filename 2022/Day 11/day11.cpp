#include <functional>
#include <iostream>
#include <numeric>
#include <sstream>

class Monkey {
    int items_inspected_ = 0;
    std::vector<int> items_;
    std::function<int(int)> operation_;
    std::function<int(int)> monkey_target_;

public:
    Monkey(std::vector<int>& items, std::function<int(int)>& operation, std::function<int(int)>& monkey_target) {
        items_ = items;
        operation_ = operation;
        monkey_target_ = monkey_target;
    }

    void AddItem(int item) {
        items_.push_back(item);
    }

    void ThrowItems(std::vector<Monkey>& monkeys) {
      items_inspected_ += items_.size();
        for (int item : items_) {
            int new_item = operation_(item);
            monkeys[monkey_target_(new_item)].AddItem(new_item);
        }
        items_.clear();
    }

    [[nodiscard]] int get_items_inspected() const {
        return items_inspected_;
    }

    bool operator < (const Monkey& monkey) const {
        return items_inspected_ > monkey.items_inspected_;
    }
 };

int main() {
    const int kNumRounds = 10000; // Set to 20 for part 1
    const int kWorryDropFactor = 1; // Set to 3 for part 1

    int mod = 1; // Will become the lcm of all the divisors, used to limit item worry levels
    std::string ignored;
    std::string line;
    std::vector<Monkey> monkeys;
    while (getline(std::cin, ignored)) { // "Monkey n:"
        std::vector<int> items;
        std::cin.ignore(18); // "  Starting items: "
        getline(std::cin, line);
        std::stringstream ss = std::stringstream(line);
        int item;
        while (ss >> item) {
            items.push_back(item);
            ss.ignore(); // Ignore commas between items
        }

        std::cin.ignore(23); // "  Operation: new = old "
        char op;
        std::string operand;
        std::cin >> op >> operand;
        std::function<int(int)> operation = [op, operand, &mod](int item) {
            int change = operand == "old" ? item : stoi(operand);
            if (op == '+') {
                return ((item + change) / kWorryDropFactor) % mod;
            } else { // op == '*'
                return (int) (((long long) item * change / kWorryDropFactor) % mod);
            }
        };
        std::cin.ignore(); // Ignore "\n"

        getline(std::cin, line);
        int divisor = stoi(line.substr(line.find_last_of(' ')));
        getline(std::cin, line);
        int true_monkey_id = stoi(line.substr(line.find_last_of(' ')));
        getline(std::cin, line);
        int false_monkey_id = stoi(line.substr(line.find_last_of(' ')));
        std::function<int(int)> monkey_target = [divisor, true_monkey_id, false_monkey_id](int item) {
            return item % divisor == 0 ? true_monkey_id : false_monkey_id;
        };
        mod = std::lcm(mod, divisor);
        std::cin.ignore(); // Ignore "\n"

        monkeys.emplace_back(items, operation, monkey_target);
    }

    for (int i = 0; i < kNumRounds; ++i) {
        for (Monkey& monkey : monkeys) {
            monkey.ThrowItems(monkeys);
        }
    }
    std::sort(monkeys.begin(), monkeys.end());
    long long monkey_business = (long long) monkeys[0].get_items_inspected() * monkeys[1].get_items_inspected();
    std::cout << monkey_business << "\n";
}
