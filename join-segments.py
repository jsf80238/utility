import json
from collections import defaultdict

input_file = "/home/jason/Downloads/Colorado_Trail_Plan_2.json"
with open(input_file, 'r') as f:
    data = json.load(f)

GEOMETRY = "geometry"
COORDINATES = "coordinates"
LINE_STRING = "LineString"
TYPE = "type"
FEATURES = "features"
PROPERTIES = "properties"
TITLE = "title"

'''
{
  "features": [
    {
      "geometry": {
        "coordinates": [],
        "type": "LineString"
      }
  "type": "FeatureCollection"
}
'''

coordinate_dict = defaultdict(list)

for item in data[FEATURES]:
    if GEOMETRY not in item:
        continue
    if item.get(GEOMETRY).get(TYPE) == LINE_STRING:
        segment_name = item[PROPERTIES][TITLE]
        for latitude, longitude in item[GEOMETRY].get(COORDINATES):
            coordinate_dict[segment_name].append((round(latitude, 4), round(longitude, 4)))

coordinate_list = list()
for key, value in sorted(coordinate_dict.items()):
    coordinate_list.extend(value)

geometry = {
    COORDINATES: coordinate_list,
    TYPE: LINE_STRING,
}
result_dict = {
    TYPE: "FeatureCollection",
    FEATURES: [
        {
            GEOMETRY: geometry,
        }
    ],
}

print(json.dumps(result_dict, indent=2))
