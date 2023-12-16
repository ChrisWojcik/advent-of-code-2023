import sys
import math
from collections import defaultdict

grid = []
start = None
COLUMNS = 0
ROWS = 0

def get_index_of(needle, haystack):
  try :
    index = haystack.index(needle)
  except ValueError :
    index = -1

  return index

for line in sys.stdin:
  line = line.strip()

  row = list(line)
  COLUMNS = len(row)

  s = get_index_of('S', row)

  if s >= 0:
    start = (ROWS, s)

  grid.append(row)
  ROWS += 1

cardinals = {
  (-1, 0): 'north',
  (0, 1): 'east',
  (1, 0): 'south',
  (0, -1): 'west'
}

directions_to_next_tile = {
  '.': [],
  '|': ['north', 'south'],
  '-': ['east', 'west'],
  'L': ['north', 'east'],
  'J': ['north', 'west'],
  '7': ['south', 'west'],
  'F': ['south', 'east'],
}

valid_tiles_in_direction = {
  'north': ['|', '7', 'F'],
  'east': ['-', 'J', '7'],
  'south': ['|', 'L', 'J'],
  'west': ['-', 'L', 'F']
}

def continues_path(neighbor, tile, direction):
  if neighbor == '.':
    return False

  cardinal = cardinals[direction]

  if (tile == 'S' or cardinal in directions_to_next_tile[tile]) and \
      neighbor in valid_tiles_in_direction[cardinal]:
    return True
  else:
    return False

# build a graph of the tiles where tiles which are connected
# by pipes in a valid way are connected by edges in the graph
graph = defaultdict(set)

for r in range(0, ROWS):
  for c in range(0, COLUMNS):
    tile = (r, c)
    tile_type = grid[r][c]

    directions = cardinals.keys()

    for direction in directions:
      neighbor = (r + direction[0], c + direction[1])
      r1, c1 = neighbor

      # outside the grid
      if r1 < 0 or r1 >= ROWS:
        continue

      # outside the grid
      if c1 < 0 or c1 >= COLUMNS:
        continue

      neighbor_type = grid[r1][c1]

      # undirected because you can go either way around the loop
      if continues_path(neighbor_type, tile_type, direction):
        graph[tile].add(neighbor)
        graph[neighbor].add(tile)

# DFS
def find_cycle(start):
  S = [[start]]
  visited = set()

  while len(S) > 0:
    path = S.pop()
    tile = path[-1]
    previous_tile = path[-2] if len(path) > 1 else None

    if tile not in visited:
      visited.add(tile)
      neighbors = graph[tile]

      for neighbor in neighbors:
        if neighbor == previous_tile:
          continue

        if neighbor == start:
          return path

        new_path = list(path)
        new_path.append(neighbor)
        S.append(new_path)

  return None

loop = find_cycle(start)
print(len(loop) // 2)
