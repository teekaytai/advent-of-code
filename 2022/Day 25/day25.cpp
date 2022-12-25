#include <iostream>

using namespace std;

int main() {
    const int kBase = 5;

    long long total = 0;
    string line;
    while (getline(cin, line)) {
        long long m = 1;
        for (int i = line.length() - 1;  i >= 0; --i) {
            char c = line[i];
            total += m * (c == '=' ? -2 : c == '-' ? -1 : c - '0');
            m *= kBase;
        }
    }

    string output;
    while (total != 0) {
        int digit = total % kBase;
        if (digit > 2) {
            digit -= kBase;
        }
        total -= digit;
        total /= 5;
        output += digit == -2 ? '=' : digit == -1 ? '-' : '0' + digit;
    }
    reverse(output.begin(), output.end());

    cout << output << "\n";
}
