import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Solve wordscapes problems.', epilog='Example patterns: "b?ll"  "____"  "ca_"  "mo?se"')
parser.add_argument('allowed', metavar="ALLOWED_LETTERS", help="Letters which can be used in the solution, case-insensitive.")
parser.add_argument('required', metavar="REQUIRED_LETTERS", help="Letters which must be used in the solution, case-insensitive. These are automatically added to the 'allowed' list if not already present.")
parser.add_argument('pattern', metavar="PATTERN", help="Enter constraints here. Use underscores or question marks for the letters to be filled in/guessed.")
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
allowed_letters = args.allowed
required_letters = args.required
pattern = args.pattern
dictionary_file = args.dictionary_file
solution_length = len(pattern)
regex = re.compile("^[a-zA-Z]+$")
match = regex.match(allowed_letters)
if not match:
    parser.error("Letters only for first argument.")
regex = re.compile(r"^[a-zA-Z_\?]+$")
match = regex.match(pattern)
if not match:
    parser.error("Letters, underscores and question marks only for second argument.")

# Letters in the must list should be merged into the allowed list
allowed_letters = set(allowed_letters) | set(required_letters)
# Get valid words
valid_word_set = set([line.strip().lower() for line in open(dictionary_file).readlines()])

match_set = set()
for potential_match in valid_word_set:
    if len(potential_match) != 5:
        continue
    is_clear = True
    for letter in required_letters:
        if letter not in potential_match:
            is_clear = False
            break
    for letter in potential_match:
        if letter not in allowed_letters:
            is_clear = False
            break
    if not is_clear:
        continue
    # Now check if it matches the pattern given by the user
    search_pattern_text = "(" + pattern.replace("_", r"\w").replace("?", r"\w") + ")"
    regex = re.compile(search_pattern_text, re.IGNORECASE)
    match = regex.match(potential_match)
    if match:
        match_set.add(match.group(1).lower())

print("\n".join(sorted(match_set)))
