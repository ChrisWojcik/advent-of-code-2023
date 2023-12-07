import sys

numbers = []
schematic = []

WIDTH = 0
HEIGHT = 0
line_number = 0

for line in sys.stdin:
  line = line.strip()

  schematic.append(list(line))
  WIDTH = len(line)

  current_number = ''
  start_of_current_number = None

  for pos, char in enumerate(line):
    if char.isdigit():
      if not current_number:
        start_of_current_number = pos

      current_number += char

      next_char = '' if pos == WIDTH - 1 else line[pos+1] 

      if not next_char.isdigit():
        start_pos = start_of_current_number
        end_pos = pos

        # e.g. (457, (0, (3, 5)))
        number = (int(current_number), (line_number, (start_pos, end_pos)))

        numbers.append(number)

        current_number = ''
        start_of_current_number = None

  line_number += 1
  HEIGHT = line_number

def is_symbol(char):
  return char != '.' and not char.isdigit()

def is_part_number(number, position):
  (line_number, start_end) = position
  (start, end) = start_end

  len_line = len(schematic[line_number])

  # symbol on same line to left
  if start > 0 and is_symbol(schematic[line_number][start - 1]):
    return True
  
  # symbol on same line to right
  if end < WIDTH - 1 and is_symbol(schematic[line_number][end + 1]):
    return True

  # symbol above
  if line_number > 0:
    start_above = start - 1 if start > 0 else 0
    end_above = end + 1 if end < WIDTH - 1 else WIDTH - 1
    
    for char in schematic[line_number - 1][start_above:end_above+1]:
      if is_symbol(char):
        return True

  # symbol below
  if line_number < HEIGHT - 1:
    start_below = start - 1 if start > 0 else 0
    end_below = end + 1 if end < WIDTH - 1 else WIDTH - 1

    for char in schematic[line_number + 1][start_below:end_below+1]:
      if is_symbol(char):
        return True

  return False

sum = 0

for (number, position) in numbers:
  if is_part_number(number, position):
    sum += number

print(sum)