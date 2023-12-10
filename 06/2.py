import sys

time_limit = None
distance_to_beat = None

for line in sys.stdin:
  line = line.strip()

  if line.startswith('Time:'):
    parts = line.split()
    time_limit = int(''.join([_ for _ in parts[1:]]))

  if line.startswith('Distance:'):
    parts = line.split()
    distance_to_beat = int(''.join([_ for _ in parts[1:]]))

ways_to_win = 0

for t in range(time_limit - 1, 0, -1):
  hold_time = t
  moving_time = time_limit - t

  if hold_time * moving_time > distance_to_beat:
    ways_to_win += 1

print(ways_to_win)
