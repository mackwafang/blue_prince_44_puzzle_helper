import csv, os, logging
from string import ascii_lowercase

GRID_WIDTH = 5
GRID_HEIGHT = 9
GRID_COUNT = 45
HINT_FILENAME = "hints.csv"
clues = [""] * GRID_COUNT

def load_hints():
	global clues
	if not os.path.isfile(HINT_FILENAME):
		logging.error(f"File [{HINT_FILENAME}] is not found in local direction.")
		return None

	clues = []
	logging.info(F"Reding {HINT_FILENAME}")
	with open(HINT_FILENAME, newline="") as file:
		reader = csv.reader(file)
		for row in reader:
			logging.info(f"read {row}")
			clues += row

	logging.info(f"clues are: {clues}")

def save_hints():
	global clues
	logging.info(f"Writing {HINT_FILENAME}")
	with open(HINT_FILENAME, "w", newline="") as file:
		writer = csv.writer(file)
		for clue in [clues[i:i+GRID_WIDTH] for i in range(0, GRID_COUNT, GRID_WIDTH)]:
			logging.info(f"wrote {clue}")
			writer.writerow(clue)

def diff_word(a, b):
	count_a = [0] * 26
	count_b = [0] * 26

	for c in a:
		if c in ascii_lowercase:
			count_a[ord(c)-97] += 1
	for c in b:
		if c in ascii_lowercase:
			count_b[ord(c)-97] += 1
	final_count = [abs(count_a[i] - count_b[i]) for i in range(26)]
	return ''.join(chr(index+97) for index, i in enumerate(final_count) if i > 0)
