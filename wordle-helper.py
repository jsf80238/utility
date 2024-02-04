import argparse
from collections import Counter, defaultdict
from os import linesep
from pathlib import Path

VOWELS = "aieouy"

DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Generate lists of words with vowels.')
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
parser.add_argument('length', metavar="LENGTH", type=int, help="Length of the words to generate.")
parser.add_argument('vowel_count', metavar="VOWELS", type=int, help="How many vowels the words should have.")
args = parser.parse_args()
dictionary_file = args.dictionary_file
length = args.length
vowel_count = args.vowel_count

content = open(dictionary_file).readlines()
allowed_word_set = [x.strip().lower() for x in content if len(x) == length+1 and "'" not in x]
candidate_dict = defaultdict(list)
for word in allowed_word_set:
    my_counter = Counter(word)
    if len(my_counter) == length:
        # Count the vowels
        if sum([1 for x in word if x in VOWELS]) == vowel_count:
            candidate_dict[vowel_count].append(word)
for key, value in sorted(candidate_dict.items()):
    print(linesep.join(value))
