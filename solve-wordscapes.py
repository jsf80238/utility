# https://apps.apple.com/us/app/wordscapes-uncrossed/id1302451299
import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Solve wordscapes problems.', epilog='Example patterns: "b?ll"  "____"  "ca_"  "mo?se"')
parser.add_argument('letters', metavar="LETTERS", help="Letters which could be used in the solution, up to six, case-insensitive.")
parser.add_argument('pattern', metavar="PATTERN", help="Enter constraints here. Use up to six characters. Use underscores or question marks for the letters to be filled in/guessed.")
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
letters = args.letters
pattern = args.pattern
dictionary_file = args.dictionary_file
regex = re.compile("^[a-zA-Z]{1,6}$")
match = regex.match(letters)
if not match:
    parser.error("Up to six letters allowed for first argument.")
regex = re.compile("^[a-zA-Z_\?]{1,6}$")
match = regex.match(pattern)
if not match:
    parser.error("Up to six characters allowed for second argument.")

# Get valid words
valid_word_set = set([line.strip().lower() for line in open(dictionary_file).readlines()])

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
        print(match.group(1).lower())
