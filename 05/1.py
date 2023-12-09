import sys

seeds = {}
maps = []

current_map_name = None
current_map_ranges = []

for line in sys.stdin:
  line = line.strip()

  if line.startswith('seeds:'):
    [name, numbers] = line.split(': ')
    seeds = { int(seed):{} for seed in numbers.split() }
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

for seed in seeds.keys():
  source_value = seed

  for (map_name, ranges) in maps:
    (source, destination) = map_name
    destination_value = None

    for r in ranges:
      [destination_start, source_start, range_length] = r

      destination_end = destination_start + range_length - 1
      source_end = source_start + range_length - 1

      if source_value >= source_start and source_value <= source_end:
        offset = source_value - source_start
        destination_value = destination_start + offset
        break

    if destination_value == None:
      destination_value = source_value

    seeds[seed][destination] = destination_value
    source_value = destination_value

locations = [v['location'] for k,v in seeds.items()]

print(min(locations))
