import sys

sum = 0

for line in sys.stdin:
  line = line.strip()

  only_digits = []

  for pos, char in enumerate(line):
    if char.isdigit():
      only_digits.append(char)
    if line[pos:pos+3] == 'one':
      only_digits.append('1')
    if line[pos:pos+3] == 'two':
      only_digits.append('2')
    if line[pos:pos+5] == 'three':
      only_digits.append('3')
    if line[pos:pos+4] == 'four':
      only_digits.append('4')
    if line[pos:pos+4] == 'five':
      only_digits.append('5')
    if line[pos:pos+3] == 'six':
      only_digits.append('6')
    if line[pos:pos+5] == 'seven':
      only_digits.append('7')
    if line[pos:pos+5] == 'eight':
      only_digits.append('8')
    if line[pos:pos+4] == 'nine':
      only_digits.append('9')

  calibration_value = only_digits[0] + only_digits[-1]

  sum += int(calibration_value)

print(sum)