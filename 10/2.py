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

# boundary of rectangular area with pipe
MIN_R = math.inf
MAX_R = -math.inf
MIN_C = math.inf
MAX_C = -math.inf

for tile in loop:
  r,c = tile

  MIN_R = min(MIN_R, r)
  MAX_R = max(MAX_R, r)
  MIN_C = min(MIN_C, c)
  MAX_C = max(MAX_C, c)

# represent each tile as a 3x3 array of "pixels"
# so we can capture the "gaps" between pipes
# as blank pixels
#
# 1 is "filled", part of the pipe
# 0 is "unfilled", either inside or outside
#
# e.g. "L" looks like this visually:
# .X.
# .XX
# ...
def pixels_for_tile_type(tile_type):
  if tile_type == '.':
    return [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]
    ]
  if tile_type == 'S':
    return [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1]
    ]
  if tile_type == '|':
    return [
      [0, 1, 0],
      [0, 1, 0],
      [0, 1, 0]
    ]
  if tile_type == '-':
    return [
      [0, 0, 0],
      [1, 1, 1],
      [0, 0, 0]
    ]
  if tile_type == 'L':
    return [
      [0, 1, 0],
      [0, 1, 1],
      [0, 0, 0]
    ]
  if tile_type == 'J':
    return [
      [0, 1, 0],
      [1, 1, 0],
      [0, 0, 0]
    ]
  if tile_type == '7':
    return [
      [0, 0, 0],
      [1, 1, 0],
      [0, 1, 0]
    ]
  if tile_type == 'F':
    return [
      [0, 0, 0],
      [0, 1, 1],
      [0, 1, 0]
    ]

all_pixels = []
center_pixels_by_blank_tile = {}

# row of pixels, column of pixels
# will increment by 3 at a time
rp = 0
cp = 0

for r in range(MIN_R, MAX_R + 1):
  pixels = [[], [], []]

  for c in range(MIN_C, MAX_C + 1):
    tile = (r, c)
    tile_type = grid[r][c]

    # clearing out the "junk" and leave only the loop
    if tile not in loop:
      tile_type = '.'

    [rp0, rp1, rp2] = pixels_for_tile_type(tile_type)

    pixels[0] += rp0
    pixels[1] += rp1
    pixels[2] += rp2

    # so we can keep track of which pixels represent which blank tiles
    if tile_type == '.':
      center_pixels_by_blank_tile[tile] = (rp+1, cp+1)

    cp += 3

  all_pixels += pixels
  rp += 3
  cp = 0

def flood_fill(start_pixel):
  r,c = start_pixel

  S = [start_pixel]
  visited = set()

  while len(S) > 0:
    pixel = S.pop()
    r,c = pixel

    if pixel not in visited:
      if all_pixels[r][c] == 0:
        all_pixels[r][c] = -1

      visited.add(pixel)
      directions = cardinals.keys()

      for direction in directions:
        neighbor = (r + direction[0], c + direction[1])
        r1, c1 = neighbor

        # outside the grid
        if r1 < 0 or r1 >= len(all_pixels):
          continue

        # outside the grid
        if c1 < 0 or c1 >= len(all_pixels[0]):
          continue

        # boundary color
        if all_pixels[r1][c1] == 1:
          continue

        S.append(neighbor)

# flood fill the "outside":
# no matter what tile type is in the top left corner,
# the pixel (0,0) is definitely outside
flood_fill((0, 0))

enclosed_tiles = 0

for tile,pixel in center_pixels_by_blank_tile.items():
  r,c = pixel

  # if == 0 , did not get hit by the flood fill
  if all_pixels[r][c] == 0:
    enclosed_tiles += 1

print(enclosed_tiles)

# visualization
output = ''

for row in all_pixels:
  for pixel in row:
    if pixel == -1:
      output += '.'
    if pixel == 1:
      output += 'X'
    if pixel == 0:
      output += 'o'

  output += '\n'

f = open("part2-vis.txt", "w")
f.write(output)
f.close()
