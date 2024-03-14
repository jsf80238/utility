import argparse
import csv
import enum
# import glob
import os
import re


class Field(enum.StrEnum):
    company = "Company"
    first_name = "First Name"
    last_name = "Last Name"
    position = "Position"


parser = argparse.ArgumentParser()
parser.add_argument('pattern')
parser.add_argument('input', nargs='+', type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()
pattern = re.compile(".*" + args.pattern + ".*", re.IGNORECASE)
file_io_list = args.input

# pattern = re.compile(".*mitsu.*", re.IGNORECASE)
# file_io_list = "/home/jason/Employment/*conn*csv"

found_count = 0

for file_io in file_io_list:
    is_filename_printed = False
    reader = csv.DictReader(file_io)
    for row in reader:
        if not row[Field.company]:
            continue
        if match := pattern.search(row[Field.company]):
            if not is_filename_printed:
                print()
                print(os.path.basename(file_io.name))
                is_filename_printed = True
            print(f"  {row[Field.first_name]} {row[Field.last_name]} ({row[Field.position]} at {row[Field.company]})")
