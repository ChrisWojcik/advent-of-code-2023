import sys

times = []
distances_to_beat = []

for line in sys.stdin:
  line = line.strip()

  if line.startswith('Time:'):
    parts = line.split()
    times = [int(t) for t in parts[1:]]

  if line.startswith('Distance:'):
    parts = line.split()
    distances_to_beat = [int(d) for d in parts[1:]]

races = list(zip(times, distances_to_beat))

answer = 1

for race in races:
  (time_limit, distance_to_beat) = race

  ways_to_win = 0

  for t in range(time_limit - 1, 0, -1):
    hold_time = t
    moving_time = time_limit - t

    if hold_time * moving_time > distance_to_beat:
      ways_to_win += 1

  answer = answer * ways_to_win

print(answer)
