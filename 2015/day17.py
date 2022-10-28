#!/usr/bin/env python3
import itertools

with open('day17input.txt', 'r') as f:
    # The flags we want to keep track of. How many ways, for part 1, the smallest possible combination and how many
    # combinations for part 2
    ways, smallest, ways_smallest = 0, 0, 0
    # Input file is just a list for numbers
    containers = [int(x) for x in f.readlines()]
    # Starting with sets of length 1, iterate over all combinations of all possible lengths of sub-lists
    for i in range(1, len(containers)):
        for combination in itertools.combinations(containers, i):
            # if the total is 150, we need to accept this as a valid combination
            if sum(combination) == 150:
                # If we've not yet found a valid combination, we can record this as the shortest length.
                if ways == 0:
                    smallest = i
                # If this is a valid combination of the shortest length, increase the counter for part 2
                if i == smallest:
                    ways_smallest += 1
                # Increase the counter for part 1
                ways += 1

    print(ways)
    print(ways_smallest)
