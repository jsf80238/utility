import argparse
import enum
import random
import string

# Imports above are standard Python
# Imports below are 3rd-party
from colored import Fore, Back, Style, stylize

DEFAULT_DICTIONARY_FILE = "/usr/share/dict/american-english"  # On Ubuntu at least

'''
parser = argparse.ArgumentParser(description='Play Wordle.')
parser.add_argument('--dictionary-file', metavar='/path/to/dictionary', default=DEFAULT_DICTIONARY_FILE, help=f'Depends on operating system, default is {DEFAULT_DICTIONARY_FILE}.')
parser.add_argument('length', metavar="LENGTH", type=int, help="Length of the words to generate.")
args = parser.parse_args()
dictionary_file = args.dictionary_file
length = args.length
'''
dictionary_file = DEFAULT_DICTIONARY_FILE
length = 5

class ColorCode(enum.StrEnum):
    not_guessed: str = f'{Fore.black}{Back.white}'
    guessed_exactly_correctly: str = f'{Fore.blue}{Back.green}'
    guessed_correctly: str = f'{Fore.black}{Back.green}'
    guessed_incorrectly: str = f'{Fore.black}{Back.red}'


letter_dict = dict()
for char in string.ascii_uppercase:
    letter_dict[char] = ColorCode.not_guessed

candidate_list = [x.strip().lower() for x in open(dictionary_file).readlines() if "'" not in x and len(x.strip()) == length]
answer = random.choice(candidate_list)
answer = "AFTER"
guess_list = list()

while True:
    print()
    for letters, styles in guess_list:
        for letter, style in zip(letters, styles):
            print(" " + stylize(letter, style), end="")
    print(f"{Style.reset}")
    for key, value in letter_dict.items():
        style = letter_dict[key]
        print(" " + stylize(key, style), end="")
    print(f"{Style.reset}")
    print()
    # guess = input("->").upper()
    guess = ''.join(random.choices(string.ascii_uppercase, k=length))
    if len(guess) != length:
        print("Incorrect length!")
        continue

    exactly_correct_letter_count = 0
    guess_result_list = list()
    for guessed_letter, answer_letter in zip(guess, answer):
        if guessed_letter in answer:
            letter_dict[guessed_letter] = ColorCode.guessed_correctly
            if guessed_letter == answer_letter:
                guess_result_list.append(ColorCode.guessed_exactly_correctly)
                exactly_correct_letter_count += 1
            else:
                guess_result_list.append(ColorCode.guessed_correctly)
        else:
            letter_dict[guessed_letter] = ColorCode.guessed_incorrectly
            guess_result_list.append(ColorCode.guessed_incorrectly)
    if exactly_correct_letter_count == length:
        print("Solved!")
        exit()
    guess_list.append((guess, guess_result_list[:]))
