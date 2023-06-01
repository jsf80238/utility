import csv
from pathlib import Path
from textwrap import wrap, indent

GROUP = 'Group'
TITLE = 'Title'
USERNAME = 'Username'
PASSWORD = 'Password'
URL = 'URL'
NOTES = 'Notes'

EXCLUDE_LIST = (
    "Miscellaneous",
    "Archive",
    "Employment",
    "School",
    "Retail",
)

def is_excluded(s):
    return any(True for x in EXCLUDE_LIST if x in s)

data = Path("/tmp/stuff.csv")
output = Path("/tmp/better.csv")
with open(data, newline="") as reader, open(output, "w", newline="") as writer:
    csvreader = csv.DictReader(reader)
    for row in csvreader:
        if is_excluded(row[GROUP]):
            continue
        print()
        print("-"*40)
        print(f"{TITLE:<8}: {row[TITLE]}")
        print(f"{USERNAME:<8}: {row[USERNAME]}")
        print(f"{PASSWORD:<8}: {row[PASSWORD]}")
        print(f"{URL:<8}: {row[URL]}")
        #print(row[NOTES])
        notes_list = list()
        for line in row[NOTES].strip().splitlines():
            if not line:
                continue
            lines = "\n".join(wrap(line, 50))
            if type(lines) == str:
                notes_list.append(lines)
            elif type(lines) == list:
                notes_list.extend(lines)
            else:
                raise "Programming error"
        if notes_list:
            notes = notes_list.pop(0) + "\n" + indent("\n".join(notes_list), ' '*10)
        else:
            notes = ""
        #notes = indent(row[NOTES].strip(), ' '*10)
        #notes = "\n".join(wrap(row[NOTES].strip(), width=50, initial_indent='', subsequent_indent=' '*10))
        print(f"{NOTES:<8}: {notes}")
