#include <deque>
#include <iostream>
#include <vector>

using namespace std;

void rotate(deque<long long*>& dq) {
    dq.push_back(dq.front());
    dq.pop_front();
}

void rotateBack(deque<long long*>& dq) {
    dq.push_front(dq.back());
    dq.pop_back();
}


int main() {
    const int kDecryptionKey = 811589153; // Set to 1 for part 1
    const int kNumMixes = 10; // Set to 1 for part 1

    vector<long long*> order;
    deque<long long*> dq;
    long long* zero_ptr;
    int input;
    while (cin >> input) {
        auto* num_ptr = new long long((long long) input * kDecryptionKey);
        order.push_back(num_ptr);
        dq.push_back(num_ptr);
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
            while (dq.front() != num_ptr) {
                rotate(dq);
            }
            dq.pop_front();
            if (*num_ptr > 0) {
                for (int j = *num_ptr % (L - 1); j > 0; --j) {
                    rotate(dq);
                }
            } else {
                for (int j = *num_ptr % (L - 1); j < 0; ++j) {
                    rotateBack(dq);
                }
            }
            dq.push_front(num_ptr);
        }
    }

    long long res = 0;
    while (dq.front() != zero_ptr) {
        rotate(dq);
    }
    for (int i = 1; i <= 3000; ++i) {
        rotate(dq);
        if (i % 1000 == 0) {
            res += *dq.front();
        }
    }

    cout << res << "\n";
}
