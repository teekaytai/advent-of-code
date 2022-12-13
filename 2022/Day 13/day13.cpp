#include <iostream>
#include <sstream>
#include <vector>

class IPacketData {
  public:
    virtual ~IPacketData() = default;
};

class IntData : public IPacketData {
  public:
    explicit IntData(std::basic_istream<char>& in) {
        in >> this->value_;
    }

    std::strong_ordering operator<=>(const IntData& that) const {
        return this->value_ <=> that.value_;
    }

  private:
    int value_;
};

class ListData : public IPacketData {
  public:
    explicit ListData(std::basic_istream<char>& in) {
        in.ignore(); // '['
        if (in.peek() == ']') {
            in.ignore();
            return;
        }

        bool end_reached = false;
        while (!end_reached) {
            char next_char = in.peek();
            if (next_char == '[') {
                data_.push_back(new ListData(in));
            } else {
                data_.push_back(new IntData(in));
            }
            end_reached = in.peek() == ']';
            in.ignore(); // ',' or ']'
        }
    }

    explicit ListData(const IntData& int_data) {
        data_.push_back(new IntData(int_data));
    }

    [[nodiscard]] int size() const {
        return data_.size();
    }

    const IPacketData* operator[](int i) const {
        return data_[i];
    }

    std::strong_ordering operator<=>(const IPacketData* that) const {
        if (typeid(*that) == typeid(IntData)) {
            return *this <=> dynamic_cast<const IntData&>(*that);
        }
        return *this <=> dynamic_cast<const ListData&>(*that);
    }

    std::strong_ordering operator<=>(const IntData& that) const {
        return *this <=> ListData(that);
    }

    std::strong_ordering operator<=>(const ListData& that) const {
        int L = std::min((int) data_.size(), that.size());
        for (int i = 0; i < L; ++i) {
            const IPacketData* data1 = data_[i];
            const IPacketData* data2 = that[i];
            std::strong_ordering cmp = std::strong_ordering::equal;
            if (typeid(*data1) == typeid(ListData)) {
                auto& list1 = dynamic_cast<const ListData&>(*data1);
                cmp = list1 <=> data2;
            } else {
                auto& int1 = dynamic_cast<const IntData&>(*data1);
                if (typeid(*data2) == typeid(IntData)) {
                    auto& int2 = dynamic_cast<const IntData&>(*data2);
                    cmp = int1 <=> int2;
                } else {
                    auto& list2 = dynamic_cast<const ListData&>(*data2);
                    cmp = int1 <=> list2;
                }
            }
            if (cmp != std::strong_ordering::equal) {
                return cmp;
            }
        }
        return (int) data_.size() <=> that.size();
    }

  private:
    std::vector<IPacketData*> data_;
};

int main() {
    std::vector<ListData> packets;
    int in_order_total = 0; // Part 1

    std::string line;
    for (int i = 1; !std::cin.eof(); ++i) {
        ListData packet1(std::cin);
        std::cin.ignore();
        ListData packet2(std::cin);
        std::cin.ignore(2);
        if (packet1 <= packet2) {
            in_order_total += i;
        }
        packets.push_back(packet1);
        packets.push_back(packet2);
    }
    std::cout << in_order_total << "\n";

    // Part 2
    std::stringstream ss1("[[2]]");
    ListData divider_packet_1 = ListData(ss1);
    std::stringstream ss2("[[6]]");
    ListData divider_packet_2 = ListData(ss2);
    int count1 = std::count_if(packets.begin(), packets.end(), [divider_packet_1](auto packet){
        return packet < divider_packet_1;
    });
    int count2 = std::count_if(packets.begin(), packets.end(), [divider_packet_2](auto packet){
        return packet < divider_packet_2;
    });
    std::cout << (count1 + 1) * (count2 + 2) << "\n";
}
