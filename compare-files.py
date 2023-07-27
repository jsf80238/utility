import sys

file_1 = open(sys.argv[1]).readlines()
file_2 = open(sys.argv[2]).readlines()

line_count_1 = len(file_1)
line_count_2 = len(file_2)

print(f"{line_count_1} in file {sys.argv[1]}.")
print(f"{line_count_2} in file {sys.argv[2]}.")
print()

set_1 = set([x.strip() for x in file_1])
set_2 = set([x.strip() for x in file_2])

in_both = sorted(set_1.intersection(set_2))
in_1_not_2 = sorted(set_1.difference(set_2))
in_2_not_1 = sorted(set_2.difference(set_1))

print(f"In both: ({len(in_both)})")
print("\n".join([f"  {x}" for x in in_both]))
print()

print(f"In {sys.argv[1]} but not {sys.argv[2]}: ({len(in_1_not_2)})")
print("\n".join([f"  {x}" for x in in_1_not_2]))
print()

print(f"In {sys.argv[2]} but not {sys.argv[1]}: ({len(in_2_not_1)})")
print("\n".join([f"  {x}" for x in in_2_not_1]))
