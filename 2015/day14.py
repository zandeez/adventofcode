#!/usr/bin/env python3
import re

# This isn't in the input file, and I don't know if this is different per person. If it is, please let me know.
TARGET = 2503

# Regular expression to get the details we want out of each line in the input file.
PARSER = re.compile(
    r'^(?P<reindeer>.*?) can fly (?P<speed>\d+) km/s for (?P<fly_time>\d+) seconds, but then must rest for '
    r'(?P<rest_time>\d+) seconds.$')

with open('day14input.txt', 'r') as f:
    # The names aren't really relevant, but make it easier to locate the data.
    reindeer = {}
    # Parse the input file.
    for line in f.readlines():
        parsed = PARSER.match(line.strip())
        assert parsed is not None

        # Add the data to our reindeer dictionary
        data = parsed.groupdict()
        reindeer[data['reindeer']] = parsed.groupdict()

    # Build the pattern for each reindeer, and add some 0 defaults.
    # Part 1 asks for the furthest distance travelled, part 2 asks for the most points, a point is awarded to the
    # reindeer who has travelled the furthest at each second.
    for name, data in reindeer.items():
        this_deer = [int(data['speed'])] * int(data['fly_time']) + [0] * int(data['rest_time'])
        data.update({'pattern': this_deer, 'distance': 0, 'score': 0})

    # Just store this globally so we don't have to check it again at the end.
    best_distance = 0

    # Each second
    for i in range(TARGET):
        # Updates each reindeer's distance, based on their pattern
        for name, data in reindeer.items():
            data['distance'] += data['pattern'][i % len(data['pattern'])]

        # Get the best distance so far, and add a point
        best_distance = max(reindeer.items(), key=lambda x: x[1]['distance'])

        reindeer[best_distance[0]]['score'] += 1

    # Print the best distance
    print(best_distance[1]['distance'])

    # Get the best score
    best_score = max(reindeer.items(), key=lambda x: x[1]['score'])

    # Print the best score
    print(best_score[1]['score'])
