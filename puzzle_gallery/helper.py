import nltk
import logging

from typing import Generator
from nltk.corpus import words, wordnet
from itertools import product
from PyQt6.QtWidgets import QProgressBar
from tqdm import tqdm

nltk.download("wordnet")

_word_pool = set(words.words())

def create_possible_words(progress_widget: QProgressBar, options: list) -> dict:
	"""
		generate possible words given the options
		
		Arguments:
			options (list): List of columns of possible combinat
	"""
	possible_words = set(''.join(w) for w in product(*options))
	logging.info(f"Found {len(possible_words)} words")

	word_pool = list(_word_pool & possible_words)

	synonym = {}

	progress_widget.setMaximum(len(word_pool))
	# generate synonyms of all candidates
	for i, word in enumerate(word_pool):
		sym = frozenset(ss for s in wordnet.synonyms(word) for ss in s)
		if len(sym) > 3:
			synonym[word] = sym
		progress_widget.setValue(i+1)

	d = {word: synonym[word] for word in synonym}
	d = {k: d[k] for k in sorted(d)}
	return d

# RESTRICT
# TIOASOEY
# DOMETHDH
# GURIENSE
# HHAOGLTS
# LRUULTON
# MYFPNALB
# NANGOEUK
