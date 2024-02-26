# https://apps.apple.com/us/app/wordscapes-uncrossed/id1302451299
import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Solve spelling bees.', epilog='Example patterns: "b?ll"  "____"  "ca_"  "mo?se"')
parser.add_argument('letters', metavar="LETTERS", help="Letters which could be used in the solution, case-insensitive.")
parser.add_argument('minimum_length', metavar="LENGTH", type=int)
parser.add_argument('--must-haves', metavar="LETTERS", help="Don't include words unless they contain this/these.")
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
letters = args.letters
minimum_length = args.minimum_length
must_haves = args.must_haves
dictionary_file = args.dictionary_file

def is_word_contains_these(word: str, chars: str) -> bool:
    for must_have in chars:
        if must_have not in word:
            return False
    return True

# dictionary_file = DEFAULT_DICTIONARY_FILE
# letters = "grotali"
candidate_translation_table = str.maketrans(letters, " " * len(letters))

result_set = set()
for candidate in [line.strip().lower() for line in open(dictionary_file).readlines()]:
    if len(candidate) >= minimum_length:
        word_without_letters_we_want = candidate.translate(candidate_translation_table)
        if len(word_without_letters_we_want.strip()) == 0:
            if is_word_contains_these(candidate, must_haves):
                result_set.add(candidate)

print("\n".join(sorted(result_set)))
