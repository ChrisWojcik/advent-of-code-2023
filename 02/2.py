import sys
import math

sum = 0

for line in sys.stdin:
  line = line.strip()

  [game_name, rounds] = line.split(': ')

  rounds = rounds.split('; ')
  rounds = [round.split(', ') for round in rounds]
  rounds = [choice.split(' ') for round in rounds for choice in round]
  rounds = [(int(round[0]), round[1]) for round in rounds]

  fewest_per_color = {
    'red': 0,
    'green': 0,
    'blue': 0
  }

  for [number, color] in rounds:
    fewest_per_color[color] = max(fewest_per_color[color], number)

  power_of_set = fewest_per_color['red'] * fewest_per_color['green'] * fewest_per_color['blue']
  sum += power_of_set

print(sum)
