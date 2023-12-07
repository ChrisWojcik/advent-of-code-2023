import sys

sum = 0

for line in sys.stdin:
  line = line.strip()

  only_digits = list(filter(lambda char: char.isdigit(), list(line)))
  calibration_value = only_digits[0] + only_digits[-1]

  sum += int(calibration_value)

print(sum)
