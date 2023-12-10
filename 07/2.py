import sys
from collections import Counter
from functools import cmp_to_key

hands = []

face_card_values = {
  'J': 1,
  'T': 10,
  'Q': 11,
  'K': 12,
  'A': 13
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

  regular_cards = []
  jokers = []

  for value in card_values:
    if value == 1:
      jokers.append(value)
    else:
      regular_cards.append(value)

  counts = Counter(regular_cards)

  hand_type = 'high_card'
  pairs_found = 0
  three_of_a_kind_found = False

  for card_value, count in counts.items():
    if count == 5:
      hand_type = 'five_of_a_kind'
    if count == 4:
      hand_type = 'four_of_a_kind'
    if count == 3:
      three_of_a_kind_found = True
    if count == 2:
      pairs_found += 1

  if three_of_a_kind_found:
    hand_type = 'full_house' if pairs_found > 0 else 'three_of_a_kind'
  else:
    if pairs_found > 0:
      hand_type = 'two_pair' if pairs_found == 2 else 'pair'

  number_of_jokers = len(jokers)

  if number_of_jokers == 0:
    return hand_type

  if number_of_jokers == 5:
    return 'five_of_a_kind'
  if number_of_jokers == 4:
    return 'five_of_a_kind'
  if number_of_jokers == 3:
    return 'five_of_a_kind' if hand_type == 'pair' else 'four_of_a_kind'
  if number_of_jokers == 2:
    if hand_type == 'three_of_a_kind':
      return 'five_of_a_kind'
    if hand_type == 'pair':
      return 'four_of_a_kind'
    if hand_type == 'high_card':
      return 'three_of_a_kind'
  if number_of_jokers == 1:
    if hand_type == 'four_of_a_kind':
      return 'five_of_a_kind'
    if hand_type == 'three_of_a_kind':
      return 'four_of_a_kind'
    if hand_type == 'two_pair':
      return 'full_house'
    if hand_type == 'pair':
      return 'three_of_a_kind'
    if hand_type == 'high_card':
      return 'pair'

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

  number_of_jokers = 0

  for card, value in cards:
    if value == 1:
      number_of_jokers += 1

hands.sort(key=cmp_to_key(compare_hands))

winnings = 0

for i, hand in enumerate(hands):
  rank = i + 1
  cards, bid = hand

  winnings += rank * bid

print(winnings)
