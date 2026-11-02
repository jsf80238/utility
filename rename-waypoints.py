import json
import mimetypes
import sys
from collections import defaultdict
from math import sin, cos, sqrt, atan2, pi
import re

input_file = "/home/jason/Downloads/Colorado_Trail_Plan.json"
with open(input_file, 'r') as f:
    data = json.load(f)

RADIUS_OF_EARTH = 6371 * 3281  # feet
GEOMETRY = "geometry"
COORDINATES = "coordinates"
LINE_STRING = "LineString"
TYPE = "type"
FEATURES = "features"
PROPERTIES = "properties"
TITLE = "title"
POINT = "Point"
TURN_PATTERN = re.compile(r'title": "(\d+)-(\d+\w+)-(\S+)"')

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
        if item.get(GEOMETRY).get(TYPE) == LINE_STRING:
            segment_name = item[PROPERTIES][TITLE]
            for longitude, latitude in item[GEOMETRY].get(COORDINATES):
                day_dict[segment_name].append((round(latitude, 4), round(longitude, 4)))


def get_day_name(target_latitude: float, target_longitude: float) -> str:
    closest_day_name = None
    minimum_distance = sys.maxsize
    for day, coordinate_list in day_dict.items():
        for latitude, longitude in coordinate_list:
            distance = haversine_distance(target_latitude, target_longitude, latitude, longitude)
            if distance < minimum_distance:
                minimum_distance = distance
                closest_day_name = day
    if closest_day_name:
        return closest_day_name
    raise ValueError("No closest day found")


feature_list = list()
for item in data[FEATURES]:
    if GEOMETRY in item:
        if "camp" in item[PROPERTIES][TITLE].lower():
            item[PROPERTIES]["marker-symbol"] = "camping"
        if item.get(GEOMETRY).get(TYPE) == POINT:
            pass
    feature_list.append(item)

result_dict = {
    TYPE: "FeatureCollection",
    FEATURES: feature_list,
}

print(json.dumps(result_dict, indent=2))
