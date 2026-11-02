import json
import sys
from collections import defaultdict
from math import sin, cos, sqrt, atan2, pi
import re

input_file = "/home/jason/Downloads/Colorado_Trail_Plan.json"
with open(input_file, 'r') as f:
    data = json.load(f)

RADIUS_OF_EARTH = 6371 * 3281  # feet
TURN_PATTERN = re.compile(r'(\d+)-(\d+\w+)-(\S+)')

COORDINATES = "coordinates"
DESCRIPTION = "description"
FEATURES = "features"
GEOMETRY = "geometry"
LINE_STRING = "LineString"
POINT = "Point"
PROPERTIES = "properties"
TITLE = "title"
TYPE = "type"

'''
TENT_PROPERTIES = {
    'marker-symbol': 'camping',
    'title': '00. Waterton Canyon trailhead parking',
    "title": "06-029XX-Straight",
    "description": "Bear Right at intersection",
}
'''

# Get tracks
track_dict = dict()

def haversine_distance(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
) -> float:
    """
    φ1, φ2	Latitude of point 1 and 2 in radians	lat1 × π/180, lat2 × π/180
    Δφ	Difference in latitude	φ2 - φ1
    Δλ	Difference in longitude	λ2 - λ1

    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2(√a, √(1−a))
    d = R ⋅ c
    """
    lat_delta = lat2 - lat1
    lon_delta = lon2 - lon1
    a = (sin((lat_delta / 2) * pi / 180)) ** 2 + cos(lat1 * pi / 180) * cos(lat2 * pi / 180) * (sin((lon_delta / 2) * pi / 180)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return c * RADIUS_OF_EARTH


# example_point = (37.67362309014766, -107.67362309014766)
# example_lat, example_lon = example_point[0], example_point[1]
# other_point = (37.6, -107.6)
# other_lat, other_lon = other_point[0], other_point[1]
# print(haversine_distance(example_lat, example_lon, other_lat, other_lon))
# exit()

# example_point = (39.4035, -105.2200)
# example_lat, example_lon = example_point[0], example_point[1]

day_dict = defaultdict(list)

for item in data[FEATURES]:
    if GEOMETRY in item:
        if item[GEOMETRY].get(TYPE) == LINE_STRING:
            segment_name = item[PROPERTIES][TITLE]
            try:
                _, day_number = segment_name.split()
            except:
                pass
            for longitude, latitude in item[GEOMETRY].get(COORDINATES):  # Stored out-of-order is output JSON from Caltopo
                day_dict[day_number].append((round(latitude, 4), round(longitude, 4)))

day_point_counter_dict = {x:2 for x in day_dict.keys()}

def get_day_number(target_latitude: float, target_longitude: float) -> str:
    """
    Iterate over all the points in all the Caltopo lines and find the closest point by distance
    :param target_latitude:
    :param target_longitude:
    :return: the name of that line, with the "Day" removed
    """
    closest_day_number = None
    minimum_distance = sys.maxsize
    for day_number, coordinate_list in day_dict.items():
        for latitude, longitude in coordinate_list:
            distance = haversine_distance(target_latitude, target_longitude, latitude, longitude)
            if distance < minimum_distance:
                minimum_distance = distance
                closest_day_number = day_number
    if closest_day_number:
        return closest_day_number
    raise ValueError("No closest day found")


feature_list = list()
for item in data[FEATURES]:
    if GEOMETRY in item:
        if "camp" in item[PROPERTIES][TITLE].lower():
            item[PROPERTIES]["marker-symbol"] = "camping"
        if item[GEOMETRY].get(TYPE) == POINT:
            if match := TURN_PATTERN.search(item[PROPERTIES][TITLE]):
                # 02. xx-left
                longitude, latitude, _, _ = item[GEOMETRY][COORDINATES]
                day_number = get_day_number(latitude, longitude)
                day_point_number_as_string = str(day_point_counter_dict[day_number]).rjust(2, "0")
                day_point_counter_dict[day_number] += 2
                current_title_parts = item[PROPERTIES][TITLE].split("-")
                current_title = "-".join(current_title_parts[0:2])
                current_description = item[PROPERTIES].get(DESCRIPTION) or ""
                new_title = f"{day_number}. {day_point_number_as_string}-{match.group(3)}"
                if current_description:
                    new_description = f"{current_description}. Original title: {current_title}"
                else:
                    new_description = f"Original title: {current_title}"
                item[PROPERTIES][TITLE] = new_title
                item[PROPERTIES][DESCRIPTION] = new_description
        feature_list.append(item)

# for item in feature_list:
#     print(type(item))
#     from pprint import pprint
#     pprint(item)
#     print()
# exit()
result_dict = {
    FEATURES: feature_list,
    TYPE: "FeatureCollection",
}

print(json.dumps(result_dict, indent=2))
