#!/usr/bin/env python3
import itertools
import re
from typing import Tuple, Dict, Set

# This problem basically needs us to check all permutations of all nodes, cacluating the total distance of each.
# We are provided a list of distances between all points.

# Regular expression to read the usable data out of the file. I've not used labels this time, so I can do some sorting.
PARSE_REGEX = re.compile(r'^(.*?) to (.*?) = (\d+)$')

with open('day9input.txt', 'r') as f:
    # You could do this with objects in a graph, but I'm just going to shove all the distances in a dictionary of
    # Distances using the pair of locations as the key, lexicographically sorted, so (A,B) and not (B,A)
    distances: Dict[Tuple[str, str], int] = {}
    # The set of nodes. Sets don't allow duplicates, so I don't need to check if anything already exists before adding.
    nodes: Set[str] = set()

    for line in f.readlines():
        # Get the details out of the line, if we sort them, the distance will always be the first group, being numeric,
        # followed by the start and end node names in alphabetical order, so we can simply explode them out.
        parsed = PARSE_REGEX.match(line)
        assert parsed is not None
        distance, start, end = sorted(parsed.groups())

        # Add both nodes to the node set
        nodes.add(start)
        nodes.add(end)

        # Add this distance to the distances table
        distances[(start, end)] = int(distance)

    # Start with a stupid high value to be less than.
    shortest_distance = 9999999999
    # And 0 for counting the longest distance. (Part 2)
    longest_distance = 0

    # Loop over all possible permutations of all the nodes, each appearing exactly once.
    for permutation in itertools.permutations(nodes, len(nodes)):
        # Keep a running total of this route
        this_distance = 0
        # Get the distance of each pair of nodes. There is 1 less connection than there are nodes, hence the -1
        for i in range(len(permutation) - 1):
            # To look up the distance between the nodes, we need to isolate i and i+1 from the list. This is then sorted
            # to make the lookup key match what we store in the dictionary. Sorted returns an iterable which is why we
            # then convert to a list to explode.
            start, end = list(sorted(permutation[i:i + 2]))
            # Simply add the distances looked up from the dictionary
            this_distance += distances[(start, end)]

        # Check if this is a new record for either the longest or shortest, and update accordingly.
        if this_distance < shortest_distance:
            shortest_distance = this_distance
        elif this_distance > longest_distance:
            longest_distance = this_distance

    print(shortest_distance)
    print(longest_distance)
