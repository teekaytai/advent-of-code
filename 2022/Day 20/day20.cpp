#include <iostream>
#include <list>
#include <vector>

using namespace std;

int main() {
    const int kDecryptionKey = 811589153; // Set to 1 for part 1
    const int kNumMixes = 10; // Set to 1 for part 1

    vector<long long*> order;
    list<long long*> lst;
    long long* zero_ptr;
    int input;
    while (cin >> input) {
        auto* num_ptr = new long long((long long) input * kDecryptionKey);
        order.push_back(num_ptr);
        lst.push_back(num_ptr);
        if (input == 0) {
            zero_ptr = num_ptr;
        }
    }
    int L = order.size();

    for (int i = 0; i < kNumMixes; ++i) {
        for (long long* num_ptr : order) {
            if (*num_ptr == 0) {
                continue;
            }
            auto start_it = std::find(lst.begin(), lst.end(), num_ptr);
            auto end_it = start_it;
            ++end_it;
            if (end_it == lst.end()) {
                end_it = lst.begin();
            }
            lst.erase(start_it);
            if (*num_ptr > 0) {
                for (int j = *num_ptr % (L - 1); j > 0; --j) {
                    ++end_it;
                    if (end_it == lst.end()) {
                        end_it = lst.begin();
                    }
                }
            } else {
                for (int j = *num_ptr % (L - 1); j < 0; ++j) {
                    if (end_it == lst.begin()) {
                        end_it = lst.end();
                    }
                    --end_it;
                }
            }
            lst.insert(end_it, num_ptr);
        }
    }

    long long res = 0;
    auto it = find(lst.begin(), lst.end(), zero_ptr);
    for (int i = 1; i <= 3000; ++i) {
        ++it;
        if (it == lst.end()) {
            it = lst.begin();
        }
        if (i % 1000 == 0) {
            res += **it;
        }
    }

    cout << res << "\n";
}
