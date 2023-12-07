from collections import Counter
import sys

NUM_LABELS = 13
ORDER_NO_JOKER = '23456789TJQKA'
ORDER_WITH_JOKER = 'J23456789TQKA'

def score(hand: str, use_joker: bool) -> int:
    label_order = ORDER_WITH_JOKER if use_joker else ORDER_NO_JOKER
    tiebreaker_score = 0
    for card in hand:
        tiebreaker_score = tiebreaker_score * NUM_LABELS + label_order.index(card)

    if use_joker and any(card != 'J' for card in hand):
        # The optimal joker strategy is to greedily replace every joker with the most common other card in the hand
        most_common_label = Counter(card for card in hand if card != 'J').most_common(1)[0][0]
        hand = hand.replace('J', most_common_label)

    label_counts = [count for _, count in Counter(hand).most_common()]
    highest_count = label_counts[0]
    if highest_count == 5:
        return 6000000 + tiebreaker_score
    if highest_count == 4:
        return 5000000 + tiebreaker_score
    if highest_count == 3 and label_counts[1] == 2:
        return 4000000 + tiebreaker_score
    if highest_count == 3:
        return 3000000 + tiebreaker_score
    if label_counts[1] == 2:
        return 2000000 + tiebreaker_score
    if highest_count == 2:
        return 1000000 + tiebreaker_score
    return tiebreaker_score


# False for part 1, True for part 2
use_joker = True

hand_bid_pairs = sorted((line.split() for line in sys.stdin), key=lambda p: score(p[0], use_joker))
print(sum(i * int(bid) for i, (_, bid) in enumerate(hand_bid_pairs, start=1)))
