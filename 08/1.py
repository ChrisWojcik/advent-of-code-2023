import sys

directions = None
nodes = {}
line_number = -1

for line in sys.stdin:
  line_number += 1

  line = line.strip()

  if line_number == 0:
    directions = list(line)
  elif line_number == 1:
    continue
  else:
    node,neighbors = line.split(' = ')
    neighbors = neighbors[1:-1].split(', ')
    nodes[node] = neighbors

number_of_steps = 0
current_node = 'AAA'
current_direction_index = 0

while current_node != 'ZZZ':
  number_of_steps += 1

  left_neighbor, right_neighbor = nodes[current_node]
  direction = directions[current_direction_index]

  if direction == 'L':
    current_node = left_neighbor
  elif direction == 'R':
    current_node = right_neighbor

  if current_direction_index == len(directions) - 1:
    current_direction_index = 0
  else:
    current_direction_index += 1

print(number_of_steps)
