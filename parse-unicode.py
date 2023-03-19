import unicodedata as u
import fileinput
import os

ENCODING = "utf-8"
byte_num = 0
char_num = 0
line_num = 0

fields = "char line_num char_num byte_num character_name"
field_list = fields.split()
field_width_list = [len(x) for x in field_list]
print(fields)

for line in fileinput.input(encoding=ENCODING):
    line_num += 1
    for char in line:
        if char == os.linesep:
            print(" ".rjust(field_width_list[0]), end=" ")
            print(str(line_num).rjust(field_width_list[1]), end=" ")
            print(str(char_num).rjust(field_width_list[2]), end=" ")
            print(str(byte_num).rjust(field_width_list[3]), end=" ")
            print("CARRIAGE RETURN")
        else:
            char_name = u.name(char)
            print(char.rjust(field_width_list[0]), end=" ")
            print(str(line_num).rjust(field_width_list[1]), end=" ")
            print(str(char_num).rjust(field_width_list[2]), end=" ")
            print(str(byte_num).rjust(field_width_list[3]), end=" ")
            print(char_name)
        char_num += 1
        byte_num += len(bytes(char, ENCODING))
