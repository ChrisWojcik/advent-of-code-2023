import sys
from itertools import combinations

galaxies = []

ROWS = 0
COLUMNS = 0

for line in sys.stdin:
  line = line.strip()

  row = list(line)
  COLUMNS = len(row)

  r = ROWS

  for c in range(COLUMNS):
    if row[c] == '#':
      galaxies.append((r,c))

  ROWS += 1

rows_with_galaxies = set()
columns_with_galaxies = set()

for galaxy in galaxies:
  gr,gc = galaxy

  rows_with_galaxies.add(gr)
  columns_with_galaxies.add(gc)

galaxies_expanded = []
EXPANSION_RATE = 1000000

# offset the position of the galaxies
# based on the expansion rate and
# which rows / columns need to grow
for galaxy in galaxies:
  gr, gc = galaxy

  gr1 = gr
  gc1 = gc

  for r in range(ROWS):
    if r not in rows_with_galaxies and gr > r:
      gr1 += EXPANSION_RATE - 1

  for c in range(COLUMNS):
    if c not in columns_with_galaxies and gc > c:
      gc1 += EXPANSION_RATE - 1

  galaxies_expanded.append((gr1, gc1))

def manhattan_distance(p1, p2):
  p1x, p1y = p1
  p2x, p2y = p2

  return abs(p2x - p1x) + abs(p2y - p1y)

def list_choose_r(the_list, r):
  return combinations(the_list, r)

pairs = list_choose_r(galaxies_expanded, 2)
answer = 0

for pair in pairs:
  g1,g2 = pair
  answer += manhattan_distance(g1,g2)

print(answer)
