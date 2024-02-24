import argparse
from os import linesep
from pathlib import Path
import re

DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

parser = argparse.ArgumentParser(description='Generate lists of words matching a pattern.')
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
parser.add_argument('pattern', metavar="PATTERN", help="Use underscore or ? for the unknown letters.")
args = parser.parse_args()
dictionary_file = args.dictionary_file
pattern = args.pattern

# pattern = "im?ediat___"
# dictionary_file = DEFAULT_DICTIONARY_FILE

match_list = list()
regex = re.compile("^" + pattern.lower().replace("_", r"\w").replace("?", r"\w") + "$")
for candidate in [x.strip().lower() for x in open(dictionary_file).readlines()]:
    if match := regex.match(candidate):
        match_list.append(match.string)

print(linesep.join(sorted(match_list)))
