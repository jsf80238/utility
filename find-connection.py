import argparse
import csv
import os
import re

COMPANY = "Company"

parser = argparse.ArgumentParser()
parser.add_argument('pattern')
parser.add_argument('input', nargs='+', type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()
pattern = re.compile(".*" + args.pattern + ".*", re.IGNORECASE)
file_io_list = args.input

found_count = 0

for file_io in file_io_list:
    is_filename_printed = False
    reader = csv.DictReader(file_io)
    for row in reader:
        match = pattern.search(row[COMPANY])
        if match:
            if not is_filename_printed:
                print()
                print(os.path.basename(file_io.name))
                is_filename_printed = True
            print("  " + ",".join(row.values()))
