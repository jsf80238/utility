import fileinput
import re
import sys
import unicodedata

DEGREE = unicodedata.lookup("DEGREE SIGN")
MINUTE = unicodedata.lookup("APOSTROPHE")
SECOND = unicodedata.lookup("QUOTATION MARK")
NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"
NORTH_OR_SOUTH = "north_or_south"
EAST_OR_WEST = "east_or_west"

DMS_PATTERN = re.compile(
    fr"""
    \s*
    (?P<lat_degree>[\d\.-]+)
    {DEGREE}
    \s*
    (?P<lat_minute>[\d\.-]+)
    {MINUTE}
    \s*
    (
    (?P<lat_second>[\d\.-]+)
    {SECOND}
    \s*
    )?  # seconds are optional
    (?P<{NORTH_OR_SOUTH}>[NS,])  # latitude and longitude separated by North, South or comma 
                                 # if comma will assume North
    [\s,]*
    (?P<lon_degree>[\d\.-]+)
    {DEGREE}
    \s*
    (?P<lon_minute>[\d\.-]+)
    {MINUTE}
    \s*
    (
    (?P<lon_second>[\d\.-]+)
    {SECOND}
    \s*
    )?  # seconds are optional
    (?P<{EAST_OR_WEST}>[EW])?  # East or West
                               # if neither will assume East
    \s*
    """, re.VERBOSE | re.IGNORECASE
)

DECIMAL_PATTERN = re.compile(
    fr"""
    \s*
    (?P<lat_decimal>[\d\.-]+)
    {DEGREE}?
    \s*
    (?P<{NORTH_OR_SOUTH}>[NS,])  # latitude and longitude separated by North, South or comma 
                               # if comma will assume North
    \s*
    (?P<lon_decimal>[\d\.-]+)
    {DEGREE}?
    \s*
    (?P<{EAST_OR_WEST}>[EW])?  # East or West
                               # if neither will assume East
    \s*
    """, re.VERBOSE | re.IGNORECASE
)


def convert_to_dms(decimal_degree, precision=2) -> tuple([int, int, float]):
    """
    :param decimal_degree:  For example, 39.1234
    :param precision: seconds are rounded to this
    :return: a tuple of degree, minute, second, for example 39, 7, 24.4
    """
    degree = int(decimal_degree)
    minute_int_and_frac = 60 * (decimal_degree % 1)
    minute = int(minute_int_and_frac)
    second = round(60 * (minute_int_and_frac % 1), precision)
    return degree, minute, second


def convert_to_decimal(degree, minute, second, precision=6) -> float:
    """
    :param degree: for example 39
    :param minute: for example 7
    :param second: for example 24.4
    :param precision: result is rounded to this
    :return: for example 39.123400
    """
    return round(degree + minute / 60 + second / 60 / 60, precision)


def convert(s):
    output = f"{s} --> "
    match = DMS_PATTERN.search(s)
    if match:
        if not match.group(NORTH_OR_SOUTH) or match.group(NORTH_OR_SOUTH) == ",":
            north_or_south = NORTH
        else:
            north_or_south = match.group(NORTH_OR_SOUTH).upper()
        if not match.group(EAST_OR_WEST):
            east_or_west = EAST
        else:
            east_or_west = match.group(EAST_OR_WEST).upper()
        lat_degree = int(match.group("lat_degree"))
        lat_minute = int(match.group("lat_minute"))
        lat_second = float(match.group("lat_second")) or 0.0
        lon_degree = int(match.group("lon_degree"))
        lon_minute = int(match.group("lon_minute"))
        lon_second = float(match.group("lon_second")) or 0.0
        output += f"{convert_to_decimal(lat_degree, lat_minute, lat_second)}{DEGREE}{north_or_south}"
        output += f"{convert_to_decimal(lon_degree, lon_minute, lon_second)}{DEGREE}{east_or_west}"
    else:
        match = DECIMAL_PATTERN.search(s)
        if match:
            if not match.group(NORTH_OR_SOUTH) or match.group(NORTH_OR_SOUTH) == ",":
                north_or_south = NORTH
            else:
                north_or_south = match.group(NORTH_OR_SOUTH).upper()
            if not match.group(EAST_OR_WEST):
                east_or_west = EAST
            else:
                east_or_west = match.group(EAST_OR_WEST).upper()
            lat_decimal = float(match.group("lat_decimal"))
            lon_decimal = float(match.group("lon_decimal"))
            lat_degree, lat_minute, lat_second = convert_to_dms(lat_decimal)
            lon_degree, lon_minute, lon_second = convert_to_dms(lon_decimal)
            output += f"{lat_degree}{DEGREE}{lat_minute}{MINUTE}{lat_second}{SECOND}{north_or_south}"
            output += f"{lon_degree}{DEGREE}{lon_minute}{MINUTE}{lon_second}{SECOND}{east_or_west}"
        else:
            output = "Could not match pattern."
    return output


for line in fileinput.input():
    print(convert(line.strip()))
