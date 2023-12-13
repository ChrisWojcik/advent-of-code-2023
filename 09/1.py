import sys

histories = []

for line in sys.stdin:
  line = line.strip()

  history = [int(n) for n in line.split()]
  histories.append(history)

answer = 0

for history in histories:
  sequences = [history]

  while True:
    last_sequence = sequences[-1]
    new_sequence = []
    all_zeroes = True

    for i in range(1, len(last_sequence)):
      difference = last_sequence[i] - last_sequence[i - 1]
      new_sequence.append(difference)

      if difference != 0:
        all_zeroes = False

    sequences.append(new_sequence)

    if all_zeroes:
      break

  prediction = 0

  for sequence in reversed(sequences):
    prediction = sequence[-1] + prediction

  answer += prediction

print(answer)
