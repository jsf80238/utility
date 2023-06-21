# https://apps.apple.com/us/app/wordscapes-uncrossed/id1302451299
import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Solve wordscapes problems.', epilog='Example patterns: "b?ll"  "____"  "ca_"  "mo?se"')
parser.add_argument('letters', metavar="LETTERS", help="Letters which could be used in the solution, case-insensitive.")
parser.add_argument('pattern', metavar="PATTERN", help="Enter constraints here. Use underscores or question marks for the letters to be filled in/guessed.")
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
letters = args.letters
pattern = args.pattern
dictionary_file = args.dictionary_file
solution_length = len(pattern)
regex = re.compile("^[a-zA-Z]+$")
match = regex.match(letters)
if not match:
    parser.error("Letters only for first argument.")
regex = re.compile("^[a-zA-Z_\?]+$")
match = regex.match(pattern)
if not match:
    parser.error("Letters, underscores and question marks only for second argument.")

# Get valid words
valid_word_set = set([line.strip().lower() for line in open(dictionary_file).readlines()])

match_set = set()
for permutation in itertools.permutations(letters, len(pattern)):
    potential_match = "".join(list(permutation))
    # Check whether this permutation is a valid word
    if not potential_match.lower() in valid_word_set:
        continue
    # Now check if it matches the pattern given by the user
    search_pattern_text = "(" + pattern.replace("_", "\w").replace("?", "\w") + ")"
    regex = re.compile(search_pattern_text, re.IGNORECASE)
    match = regex.match(potential_match)
    if match:
        match_set.add(match.group(1).lower())

print("\n".join(sorted(match_set)))
