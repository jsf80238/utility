# https://apps.apple.com/us/app/wordscapes-uncrossed/id1302451299
import argparse
import itertools
import re
DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least
DEFAULT_MINIMUM_ALLOWED_LENGTH = 4

parser = argparse.ArgumentParser(description='Solve NY Times spelling bee.')
parser.add_argument('center_letter', metavar="CENTER-LETTER", help="The letter which must be in the answers.")
parser.add_argument('other_letters', metavar="OTHER-LETTERS", help="The other six letters.")
parser.add_argument('--minimum-length', type=int, metavar='NUMBER', default=DEFAULT_MINIMUM_ALLOWED_LENGTH, help=f'Minimum length of an answer, default is {DEFAULT_MINIMUM_ALLOWED_LENGTH}.')
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
args = parser.parse_args()
center_letter = args.center_letter.lower()
other_letters = args.other_letters.lower()
dictionary_file = args.dictionary_file
minimum_length = args.minimum_length


letters_set = set(other_letters + center_letter)

match_set = set()
for candidate in [x.strip().lower() for x in open(dictionary_file).readlines()]:
    if len(candidate) >= DEFAULT_MINIMUM_ALLOWED_LENGTH:
        #candidate = "track"
        if center_letter in candidate:
            if set(candidate).issubset(letters_set):
                match_set.add(candidate)

print("\n".join(sorted(match_set)))


"""
Javascript equivalent according to https://www.codeconvert.ai/python-to-javascript-converter:

const fs = require('fs');

const dictionaryFile = "/path/to/file";
const minimumLength = 4;

const lettersSet = new Set([...otherLetters, centerLetter]);

const matchSet = new Set();
for (const candidate of fs.readFileSync(dictionaryFile, 'utf-8').split('\n').map(x => x.trim().toLowerCase())) {
    if (candidate.length >= minimumLength) {
        if (candidate.includes(centerLetter)) {
            if (new Set(candidate).every(char => lettersSet.has(char))) {
                matchSet.add(candidate);
            }
        }
    }
}

console.log([...matchSet].sort().join('\n'));

"""