# Author
[Jason Friedman](https://www.linkedin.com/in/jasonfriedmantechnology/) is the author of this code.

# parse-unicode.py
## Overview
I have many times been asked to diagnose cases where data flowing from a source fails to be accepted by a target with an error like:

    codec can't decode bytes in position 2-4

It is sometimes helpful to verify the input data is what we expect.

## Usage
`parse-unicode.py` takes its input from STDIN, or from a file if one is provided as an argument.

All of the examples produce this output (note the multi-byte character `PLUS-MINUS SIGN` at bytes 19 & 20):

    char line_num char_num byte_num character_name
       T        1        0        0 LATIN CAPITAL LETTER T
       h        1        1        1 LATIN SMALL LETTER H
       e        1        2        2 LATIN SMALL LETTER E
                1        3        3 SPACE
       e        1        4        4 LATIN SMALL LETTER E
       r        1        5        5 LATIN SMALL LETTER R
       r        1        6        6 LATIN SMALL LETTER R
       o        1        7        7 LATIN SMALL LETTER O
       r        1        8        8 LATIN SMALL LETTER R
                1        9        9 SPACE
       r        1       10       10 LATIN SMALL LETTER R
       a        1       11       11 LATIN SMALL LETTER A
       t        1       12       12 LATIN SMALL LETTER T
       e        1       13       13 LATIN SMALL LETTER E
                1       14       14 SPACE
       w        1       15       15 LATIN SMALL LETTER W
       a        1       16       16 LATIN SMALL LETTER A
       s        1       17       17 LATIN SMALL LETTER S
                1       18       18 SPACE
       ±        1       19       19 PLUS-MINUS SIGN
       5        1       20       21 DIGIT FIVE
       %        1       21       22 PERCENT SIGN
       ,        1       22       23 COMMA
                1       23       24 CARRIAGE RETURN
       w        2       24       25 LATIN SMALL LETTER W
       h        2       25       26 LATIN SMALL LETTER H
       i        2       26       27 LATIN SMALL LETTER I
       c        2       27       28 LATIN SMALL LETTER C
       h        2       28       29 LATIN SMALL LETTER H
                2       29       30 SPACE
       w        2       30       31 LATIN SMALL LETTER W
       a        2       31       32 LATIN SMALL LETTER A
       s        2       32       33 LATIN SMALL LETTER S
                2       33       34 SPACE
       g        2       34       35 LATIN SMALL LETTER G
       o        2       35       36 LATIN SMALL LETTER O
       o        2       36       37 LATIN SMALL LETTER O
       d        2       37       38 LATIN SMALL LETTER D
                2       38       39 SPACE
       e        2       39       40 LATIN SMALL LETTER E
       n        2       40       41 LATIN SMALL LETTER N
       o        2       41       42 LATIN SMALL LETTER O
       u        2       42       43 LATIN SMALL LETTER U
       g        2       43       44 LATIN SMALL LETTER G
       h        2       44       45 LATIN SMALL LETTER H
                2       45       46 SPACE
       f        2       46       47 LATIN SMALL LETTER F
       o        2       47       48 LATIN SMALL LETTER O
       r        2       48       49 LATIN SMALL LETTER R
                2       49       50 SPACE
       t        2       50       51 LATIN SMALL LETTER T
       h        2       51       52 LATIN SMALL LETTER H
       e        2       52       53 LATIN SMALL LETTER E
       m        2       53       54 LATIN SMALL LETTER M
       !        2       54       55 EXCLAMATION MARK
                2       55       56 CARRIAGE RETURN

### STDIN v.1

    $ python3 parse-unicode.py <<EOF
    > The error rate was ±5%,
    > which was good enough for them!
    > EOF

### STDIN v.2

    $ cat /tmp/example.txt
    The error rate was ±5%,
    which was good enough for them!

    $ cat /tmp/example.txt | python3 parse-unicode.py

### File
    $ cat /tmp/example.txt
    The error rate was ±5%,
    which was good enough for them!
     
    $ python3 parse-unicode.py /tmp/example.txt 

# Solve wordscapes puzzles
This is based on an app available on phones.
It uses the American English dictionary available by default on my Kubuntu system, and you can specify whatever dictionary you like.

    usage: solve-wordscapes.py [-h] [--dictionary-file /path/to/dictionary] LETTERS PATTERN
    
    Solve wordscapes problems.
    
    positional arguments:
      LETTERS               Letters which could be used in the solution, case-insensitive.
      PATTERN               Enter constraints here. Use underscores or question marks for the letters to be filled in/guessed.
    
    options:
      -h, --help            show this help message and exit
      --dictionary-file /path/to/dictionary
                            Depends on operating system, default is /usr/share/dict/american-english.
    
    Example patterns: "b?ll" "____" "ca_" "mo?se"

For example:

    $ python3 solve-wordscapes.py AGLmor ?????
    largo
    margo
    molar
    moral

And:

    $ python3 solve-wordscapes.py aGlMoR _a?g_
    largo
    margo
