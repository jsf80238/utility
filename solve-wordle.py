import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Solve wordscapes problems.', epilog='Example patterns: "b?ll"  "____"  "ca_"  "mo?se"')
parser.add_argument('allowed', metavar="ALLOWED_LETTERS", help="Letters which can be used in the solution, case-insensitive.")
parser.add_argument('pattern', metavar="PATTERN", help="Enter constraints here. Use underscores or question marks for the letters to be filled in/guessed.")
parser.add_argument('--required', metavar="REQUIRED_LETTERS", help="Letters which must be used in the solution, case-insensitive. These are automatically added to the 'allowed' list if not already present.")
parser.add_argument('--anti-pattern', metavar="ANTI_PATTERN", help="Where letters do NOT appear. Use underscores or question marks for the positions about which you have no information.")
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
allowed_letters = args.allowed
required_letters = args.required or list()
pattern = args.pattern
solution_length = len(pattern)
anti_pattern = args.anti_pattern or "_" * solution_length
dictionary_file = args.dictionary_file

regex = re.compile("^[a-zA-Z]+$")
if not regex.match(allowed_letters):
    parser.error("Letters only for first argument.")
if not regex.match(required_letters):
    parser.error("Letters only for required letters.")

regex = re.compile(r"^[a-zA-Z_\?]+$")
if not regex.match(pattern):
    parser.error("Letters, underscores and question marks only for second argument.")
if not regex.match(anti_pattern):
    parser.error("Letters, underscores and question marks only for anti-pattern.")
if len(anti_pattern) != solution_length:
    parser.error("Anti-pattern, if provided, must be same length as pattern.")

# Letters in the required list should be merged into the allowed list
allowed_letters = set(allowed_letters) | set(required_letters)
# Get valid words
valid_word_set = set([line.strip().lower() for line in open(dictionary_file).readlines() if len(line.strip()) == solution_length])

match_set = set()
for candidate in valid_word_set:
    is_clear = True
    # Reject if the candidate contains a letter not in allowed letters
    for letter in candidate:
        if letter not in allowed_letters:
            is_clear = False
            break
    # Reject if the candidate does not contain a required letter
    for letter in required_letters:
        if letter not in candidate:
            is_clear = False
            break
    # Verify it does not match the anti-pattern
    for i in range(solution_length):
        if candidate[i] == anti_pattern[i]:
            is_clear = False
            break
    if not is_clear:
        continue
    # Now check if it matches the pattern
    search_pattern_text = "(" + pattern.replace("_", r"\w").replace("?", r"\w") + ")"
    regex = re.compile(search_pattern_text, re.IGNORECASE)
    if match := regex.match(candidate):
        match_set.add(match.group(1).lower())

print("\n".join(sorted(match_set)))
