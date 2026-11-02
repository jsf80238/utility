#!/usr/bin/env python3
import sys
import json
import argparse
import copy


def load_geojson(filepath):
    """Loads GeoJSON feature collection from disk."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error reading input file: {e}\n")
        sys.exit(1)


def is_waypoint(feature):
    """Returns True if feature is a Point/Marker waypoint."""
    geom_type = feature.get('geometry', {}).get('type')
    cls = feature.get('properties', {}).get('class')
    return geom_type == 'Point' or cls == 'Marker'


def is_route(feature):
    """Returns True if feature is a LineString/Shape route."""
    geom_type = feature.get('geometry', {}).get('type')
    cls = feature.get('properties', {}).get('class')
    return geom_type == 'LineString' or cls == 'Shape'


def parse_comma_separated(input_str):
    """Splits a comma-separated string into a list of stripped strings."""
    if not input_str:
        return []
    return [item.strip() for item in input_str.split(',')]


def rename_waypoints(data, old_titles_str, new_titles_str):
    """Renames multiple waypoints sequentially by their title properties."""
    old_list = parse_comma_separated(old_titles_str)
    new_list = parse_comma_separated(new_titles_str)

    if len(old_list) != len(new_list):
        sys.stderr.write("Error: The number of items in --old and --new must match.\n")
        sys.exit(1)

    # Process pairs in sequential order to preserve precedence
    for old_title, new_title in zip(old_list, new_list):
        found = False
        for feature in data.get('features', []):
            if is_waypoint(feature):
                if feature.get('properties', {}).get('title') == old_title:
                    feature['properties']['title'] = new_title
                    found = True
        if not found:
            sys.stderr.write(f"Warning: Waypoint with title '{old_title}' not found.\n")


def rename_routes(data, old_titles_str, new_titles_str):
    """Renames multiple routes sequentially by their title properties."""
    old_list = parse_comma_separated(old_titles_str)
    new_list = parse_comma_separated(new_titles_str)

    if len(old_list) != len(new_list):
        sys.stderr.write("Error: The number of items in --old and --new must match.\n")
        sys.exit(1)

    # Process pairs in sequential order to preserve precedence
    for old_title, new_title in zip(old_list, new_list):
        found = False
        for feature in data.get('features', []):
            if is_route(feature):
                if feature.get('properties', {}).get('title') == old_title:
                    feature['properties']['title'] = new_title
                    found = True
        if not found:
            sys.stderr.write(f"Warning: Route with title '{old_title}' not found.\n")


def split_route(data, route_title, new_title_1=None, new_title_2=None):
    """Splits a route's coordinate array into two roughly equal halves."""
    features = data.get('features', [])
    for idx, feature in enumerate(features):
        if is_route(feature) and feature.get('properties', {}).get('title') == route_title:
            coords = feature.get('geometry', {}).get('coordinates', [])
            if len(coords) < 2:
                sys.stderr.write(f"Error: Route '{route_title}' has too few coordinates to split.\n")
                return

            mid = len(coords) // 2
            coords_part1 = coords[:mid + 1]
            coords_part2 = coords[mid:]

            # Create Part 1
            part1 = copy.deepcopy(feature)
            part1['geometry']['coordinates'] = coords_part1
            part1['properties']['title'] = new_title_1 if new_title_1 else f"{route_title} (Part 1)"

            # Create Part 2
            part2 = copy.deepcopy(feature)
            part2['id'] = part2.get('id', '') + "_split_2"
            part2['geometry']['coordinates'] = coords_part2
            part2['properties']['title'] = new_title_2 if new_title_2 else f"{route_title} (Part 2)"

            # Replace original feature with the two split features
            features[idx:idx + 1] = [part1, part2]
            return

    sys.stderr.write(f"Warning: Route with title '{route_title}' not found.\n")


def join_routes(data, route1_title, route2_title, new_title=None):
    """Joins two routes together in order into a single route feature."""
    features = data.get('features', [])
    r1_idx, r2_idx = None, None
    r1_feature, r2_feature = None, None

    for idx, feature in enumerate(features):
        if is_route(feature):
            title = feature.get('properties', {}).get('title')
            if title == route1_title and r1_idx is None:
                r1_idx = idx
                r1_feature = feature
            elif title == route2_title and r2_idx is None:
                r2_idx = idx
                r2_feature = feature

    if r1_feature is None or r2_feature is None:
        sys.stderr.write(f"Error: Could not find both routes '{route1_title}' and '{route2_title}'.\n")
        return

    coords1 = r1_feature.get('geometry', {}).get('coordinates', [])
    coords2 = r2_feature.get('geometry', {}).get('coordinates', [])

    combined_coords = coords1 + coords2

    joint_feature = copy.deepcopy(r1_feature)
    joint_feature['geometry']['coordinates'] = combined_coords
    joint_feature['properties']['title'] = new_title if new_title else f"{route1_title} + {route2_title}"

    indices_to_remove = sorted([r1_idx, r2_idx], reverse=True)
    for idx in indices_to_remove:
        features.pop(idx)

    features.append(joint_feature)


def main():
    parser = argparse.ArgumentParser(
        description="Modify GeoJSON routes and waypoints and output updated JSON to STDOUT."
    )
    parser.add_argument("file", help="Path to input GeoJSON file")

    subparsers = parser.add_subparsers(dest="command", help="Modification command to perform")

    # Command 1: Rename Waypoint(s)
    p_rw = subparsers.add_parser("rename-waypoint", help="Rename one or more waypoints")
    p_rw.add_argument("--old", required=True, help="Comma-separated list of current waypoint titles")
    p_rw.add_argument("--new", required=True, help="Comma-separated list of new waypoint titles")

    # Command 2: Rename Route(s)
    p_rr = subparsers.add_parser("rename-route", help="Rename one or more routes")
    p_rr.add_argument("--old", required=True, help="Comma-separated list of current route titles")
    p_rr.add_argument("--new", required=True, help="Comma-separated list of new route titles")

    # Command 3: Split Route
    p_sr = subparsers.add_parser("split-route", help="Split a route into roughly equal pieces")
    p_sr.add_argument("--title", required=True, help="Title of route to split")
    p_sr.add_argument("--title1", help="Title for first split segment")
    p_sr.add_argument("--title2", help="Title for second split segment")

    # Command 4: Join Routes
    p_jr = subparsers.add_parser("join-routes", help="Join two routes into one")
    p_jr.add_argument("--route1", required=True, help="First route title")
    p_jr.add_argument("--route2", required=True, help="Second route title")
    p_jr.add_argument("--new-title", help="Title for combined route")

    args = parser.parse_args()

    data = load_geojson(args.file)

    if args.command == "rename-waypoint":
        rename_waypoints(data, args.old, args.new)
    elif args.command == "rename-route":
        rename_routes(data, args.old, args.new)
    elif args.command == "split-route":
        split_route(data, args.title, args.title1, args.title2)
    elif args.command == "join-routes":
        join_routes(data, args.route1, args.route2, args.new_title)

    json.dump(data, sys.stdout, indent=2)


if __name__ == "__main__":
    main()