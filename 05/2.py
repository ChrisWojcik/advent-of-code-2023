import sys
import math

seed_ranges = []
maps = []

current_map_name = None
current_map_ranges = []

for line in sys.stdin:
  line = line.strip()

  if line.startswith('seeds:'):
    [name, numbers] = line.split(': ')
    numbers = [int(n) for n in numbers.split()]
    seed_ranges = [numbers[i:i + 2] for i in range(0, len(numbers), 2)]
  elif line == '':
    if current_map_name:
      maps.append((current_map_name, current_map_ranges))
      current_map_name = None
      current_map_ranges = []
  elif line.endswith(' map:'):
    [source, destination] = line[0:-5].split('-to-')
    current_map_name = (source,destination)
  else:
    current_map_ranges.append([int(n) for n in line.split()])

maps.append((current_map_name, current_map_ranges))

# takes an input range [start, end) and a range to remove [start, end) - each as tuples
# returns [[..ranges left over after removing], removed_range]
def remove_range(input_range, range_to_remove):
  (input_start, input_end) = input_range
  (to_remove_start, to_remove_end) = range_to_remove

  if input_start >= input_end:
    raise Exception('input_range '+str(input_range)+' invalid')

  if to_remove_start >= to_remove_end:
    raise Exception('range_to_remove '+str(range_to_remove)+' invalid')

  if to_remove_start >= input_end:
    return[[input_range], None]
  if to_remove_start < input_start and to_remove_end <= input_start:
    return [[input_range], None]
  if to_remove_start <= input_start and to_remove_end > input_start and to_remove_end < input_end:
    return [[(to_remove_end, input_end)], (input_start, to_remove_end)]
  if to_remove_start <= input_start and to_remove_end > input_start and to_remove_end >= input_end:
    return [[], (input_start, input_end)]
  if to_remove_start >= input_start and to_remove_end < input_end:
    return [[(input_start, to_remove_start), (to_remove_end, input_end)], (to_remove_start, to_remove_end)]
  if to_remove_start >= input_start and to_remove_end >= input_end:
    return [[(input_start, to_remove_start)], (to_remove_start, input_end)]

closest_location = math.inf

for [seed_range_start, seed_range_length] in seed_ranges:
  source_ranges = [(seed_range_start, seed_range_start + seed_range_length)]

  for (map_name, ranges) in maps:
    (source, destination) = map_name
    mapped_ranges = []
    unmapped_ranges = source_ranges.copy()

    for r in ranges:
      [destination_start, source_start, range_length] = r
      source_range_to_remove = (source_start, source_start + range_length)
      offset = destination_start - source_start

      for source_range in unmapped_ranges.copy():
        [partitioned_ranges, removed_source_range] = remove_range(source_range, source_range_to_remove)

        if removed_source_range != None:
          unmapped_ranges.remove(source_range)
          unmapped_ranges = unmapped_ranges + partitioned_ranges

          (removed_start, removed_end) = removed_source_range

          removed_length = removed_end - removed_start
          mapped_start = removed_start + offset
          mapped_end = mapped_start + removed_length

          mapped_ranges.append((mapped_start, mapped_end))

    source_ranges = unmapped_ranges + mapped_ranges

  closed_location_for_seed_range = min([start for (start, end) in source_ranges])
  closest_location = min(closest_location, closed_location_for_seed_range)

print(closest_location)
