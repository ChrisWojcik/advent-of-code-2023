import sys
from math import gcd

directions = None
nodes = {}
start_nodes = []
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

    if node[-1] == 'A':
      start_nodes.append(node)

def find_lcm(integers):
  lcm = 1

  for i in integers:
    lcm = lcm*i//gcd(lcm, i)

  return lcm

def find_number_of_steps(start_node):
  number_of_steps = 0
  current_node = start_node
  current_direction_index = 0

  while current_node[-1] != 'Z':
    number_of_steps += 1

    left_neighbor, right_neighbor = nodes[current_node]
    direction = directions[current_direction_index]

    if direction == 'L':
      next_node = left_neighbor
    elif direction == 'R':
      next_node = right_neighbor

    if current_direction_index == len(directions) - 1:
      current_direction_index = 0
    else:
      current_direction_index += 1

    current_node = next_node

  return number_of_steps

distances = []

for start_node in start_nodes:
  number_of_steps = find_number_of_steps(start_node)

  distances.append(number_of_steps)

print(find_lcm(distances))
