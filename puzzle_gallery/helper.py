import nltk
import logging

from typing import Generator
from nltk.corpus import words, wordnet
from itertools import product
from tqdm import tqdm

nltk.download("wordnet")

_word_pool = set(words.words())

def create_possible_words(options: list, length: int) -> dict:
	"""
		generate possible words given the options
		
		Arguments:
			options (list): List of columns of possible combinations
			length (int): Length of final word
	"""
	possible_words = set(''.join(w) for w in product(*options))
	logging.info(f"Found {len(possible_words)} words")

	word_pool = list(_word_pool & possible_words)

	synonym = {}
	# generate synonyms of all candidates
	for word in word_pool:
		sym = frozenset(ss for s in wordnet.synonyms(word) for ss in s)
		synonym[word] = sym

	# look for words with some matching synonyms
	candidates = set()
	for word1, sym1 in tqdm(synonym.items()):
		for word2, sym2 in synonym.items():
			if word1 == word2:
				continue
			if len(sym1 & sym2) > 0:
				candidates.add(word1)
				candidates.add(word2)

	d = {word: synonym[word] for word in candidates}
	d = {k: d[k] for k in sorted(d)}
	return d
		
