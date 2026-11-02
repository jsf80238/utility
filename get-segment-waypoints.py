import json
import re

input_file = "/home/jason/Downloads/waypoints.json"
with open(input_file, 'r') as f:
    data = json.load(f)

GEOMETRY = "geometry"
COORDINATES = "coordinates"
LINE_STRING = "LineString"
TYPE = "type"
FEATURES = "features"
PROPERTIES = "properties"
TITLE = "title"
POINT = "Point"

pattern = re.compile(r"\d+\. Segment", re.IGNORECASE)

feature_list = list()

for item in data[FEATURES]:
    if GEOMETRY not in item:
        continue
    if item.get(GEOMETRY).get(TYPE) == POINT:
        segment_name = item[PROPERTIES][TITLE]
        if segment_name.startswith("00. Waterton") or re.search(pattern, segment_name):
            latitude, longitude, _, _ = item[GEOMETRY].get(COORDINATES)
            feature = {
                GEOMETRY: {
                    COORDINATES: (round(latitude, 4), round(longitude, 4)),
                    TYPE: POINT,
                },
                TYPE: "Feature",
                PROPERTIES: {
                    TITLE: segment_name,
                }
            }
            feature_list.append(feature)

result_dict = {
    TYPE: "FeatureCollection",
    FEATURES: feature_list,
}

print(json.dumps(result_dict, indent=2))

'''
      "id": "e0d08fdc-95a5-49a8-882f-f2ef6f2d17d8",
      "type": "Feature",
      "properties": {
        "title": "00. Waterton Canyon trailhead parking",
'''