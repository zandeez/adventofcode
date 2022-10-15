#!/usr/bin/env python3
from collections import defaultdict

# Transformations to apply to the location coordinates per each instruction
MOVES = {
    '^': (0, 1),
    '>': (1, 0),
    'v': (0, -1),
    '<': (-1, 0)
}

with open('day3input.txt', 'r') as f:
    # Our location. We start at 0,0 and move following our instructions. Part 2 uses the same insturctions, but has 2
    # movers, Santa and Robo-Santa.
    part1_location = (0, 0)
    part2_locations = [(0, 0), (0, 0)]

    # Keep track of how many times we've visited each location. Use a dictionary for fast and easy lookups.
    # Using a defaultdict we can set the default value of unknown keys to 0
    present_counts_part1 = defaultdict(lambda: 0)
    present_counts_part2 = defaultdict(lambda: 0)
    # The starting location gets a present
    present_counts_part1[part1_location] += 1
    present_counts_part2[part2_locations[0]] += 1

    # Loop over all the instructions
    for index, instruction in enumerate(f.readline()):
        # Grab and apply the transformation to locations
        move = MOVES[instruction]
        part1_location = part1_location[0] + move[0], part1_location[1] + move[1]
        # Increment the present count for the new location
        present_counts_part1[part1_location] += 1

        # Ok, now for the part2 bit, we need to use a different location depending on if we're an even or odd move.
        mover = index % 2
        part2_locations[mover] = part2_locations[mover][0] + move[0], part2_locations[mover][1] + move[1]
        present_counts_part2[part2_locations[mover]] += 1

    print(len(present_counts_part1.keys()))
    print(len(present_counts_part2.keys()))
