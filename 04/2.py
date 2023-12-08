import sys
from collections import defaultdict

cards = []

for line in sys.stdin:
  line = line.strip()

  [card_name, numbers] = line.split(': ')
  [winning_numbers, my_numbers] = numbers.split(' | ')

  winning_numbers = winning_numbers.split()
  my_numbers = my_numbers.split()

  cards.append([winning_numbers, my_numbers])

count_of_each_card = { card_number: 1 for card_number in range(len(cards)) }

for card_number, card in enumerate(cards):
  [winning_numbers, my_numbers] = card
  cards_won = []

  for number in my_numbers:
    if number in winning_numbers:
      cards_won.append(card_number + len(cards_won) + 1)

  for number_of_won_card in cards_won:
    count_of_each_card[number_of_won_card] += count_of_each_card[card_number]

total_cards = sum(count_of_each_card.values())
print(total_cards)
