import sys

cards = []

for line in sys.stdin:
  line = line.strip()

  [card_name, numbers] = line.split(': ')
  [winning_numbers, my_numbers] = numbers.split(' | ')

  winning_numbers = winning_numbers.split()
  my_numbers = my_numbers.split()

  cards.append([winning_numbers, my_numbers])

score = 0

for [winning_numbers, my_numbers] in cards:
  score_for_card = 0

  for number in my_numbers:
    if number in winning_numbers:
      score_for_card = score_for_card * 2 if score_for_card > 0 else 1

  score += score_for_card

print(score)
