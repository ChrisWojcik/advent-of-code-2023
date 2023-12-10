import sys
from collections import Counter
from functools import cmp_to_key

hands = []

face_card_values = {
  'T': 10,
  'J': 11,
  'Q': 12,
  'K': 13,
  'A': 14
}

hand_type_ranks = {
  'high_card': 1,
  'pair': 2,
  'two_pair': 3,
  'three_of_a_kind': 4,
  'full_house': 5,
  'four_of_a_kind': 6,
  'five_of_a_kind': 7
}

def card_with_value(card):
  if card in face_card_values.keys():
    return (card, face_card_values[card])
  else:
    return (card, int(card))

def type_of_hand(cards):
  card_values = [card[1] for card in cards]

  counts = Counter(card_values)

  pairs_found = 0
  three_of_a_kind_found = False

  for card_value, count in counts.items():
    if count == 5:
      return 'five_of_a_kind'
    if count == 4:
      return 'four_of_a_kind'
    if count == 3:
      three_of_a_kind_found = True
    if count == 2:
      pairs_found += 1

  if three_of_a_kind_found:
    return 'full_house' if pairs_found > 0 else 'three_of_a_kind'
  if pairs_found > 0:
    return 'two_pair' if pairs_found == 2 else 'pair'

  return 'high_card'

def compare_hands(a, b):
  hand_a, bid_a = a
  hand_b, bid_b = b
  cards_a, type_a = hand_a
  cards_b, type_b = hand_b

  compare_types = hand_type_ranks[type_a] - hand_type_ranks[type_b]

  if compare_types != 0:
    return compare_types

  for i in range(len(cards_a)):
    compare_cards = cards_a[i][1] - cards_b[i][1]

    if compare_cards != 0:
      return compare_cards

  return 0

for line in sys.stdin:
  line = line.strip()

  cards,bid = line.split(' ')
  cards = list(cards)

  cards = [card_with_value(card) for card in cards]
  bid = int(bid)

  hand = [(cards, type_of_hand(cards)), bid]
  hands.append(hand)

hands.sort(key=cmp_to_key(compare_hands))

winnings = 0

for i, hand in enumerate(hands):
  rank = i + 1
  cards, bid = hand

  winnings += rank * bid

print(winnings)
