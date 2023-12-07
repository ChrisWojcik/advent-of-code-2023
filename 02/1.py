import sys

max_per_color = {
  'red': 12,
  'green': 13,
  'blue': 14
}

sum = 0
game_id = 1

for line in sys.stdin:
  line = line.strip()

  [game_name, rounds] = line.split(': ')

  rounds = rounds.split('; ')
  rounds = [round.split(', ') for round in rounds]
  rounds = [choice.split(' ') for round in rounds for choice in round]
  rounds = [(int(round[0]), round[1]) for round in rounds]

  game_possible = True

  for [number, color] in rounds:
    if number > max_per_color[color]:
      game_possible = False
      break

  if game_possible:
    sum += game_id

  game_id += 1

print(sum)
