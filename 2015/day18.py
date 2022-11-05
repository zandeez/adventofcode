#!/usr/bin/env python3
import operator
from functools import reduce

# Width and height of the grid. Used in some calculations later.
WIDTH = 100
HEIGHT = 100

# These are the coordinate transformations to use to check the state of the neighbours
TESTS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]


def evolve(state):
    """
    This function takes a state, and applies the transformations, returning a new state
    :param state: The current state
    :return: The evolved state
    """

    # Create a copy. Probably not 100% necessary as we overwrite the whole thing.
    new_state = state[:]
    # Use separate x and y coordinates. This syntax also produces the product in the same way itertools.product(
    # range(100), range(100)) would but means this look is only one indentation deep rather than nesting two loops.
    # The reason I haven't done it using flat indexes is we need to do two-dimensional bounds checking to check if
    # we're on an edge.
    for this_x, this_y in [(x, y) for x in range(WIDTH) for y in range(HEIGHT)]:
        # How many neighbours are on.
        count = 0
        # Loop over the neighbour coordinates
        for test_x, test_y in [(this_x + x, this_y + y) for x, y in TESTS]:
            # Make sure we're inside the square
            if min(test_x, test_y) < 0 or max(test_x, test_y) > WIDTH - 1:
                continue
            # If the neighbour is on, increade the count.
            if state[test_y * WIDTH + test_x] == '#':
                count += 1

            # Our new state depends on the old state, and the count of neoghbours that are on.
            # If we're off, and exactly 3 neighbours are on.
            if state[this_y * WIDTH + this_x] == '.' and count == 3:
                new_state[this_y * WIDTH + this_x] = '#'
            # If we're on, and either 2 or 3 neighbours are on.
            elif state[this_y * WIDTH + this_x] == '#' and (count == 2 or count == 3):
                new_state[this_y * WIDTH + this_x] = '#'
            # Otherwise, off
            else:
                new_state[this_y * WIDTH + this_x] = '.'

    return new_state


def setcorners(state):
    """
    For part 1, turn the corner lights on.
    :param state: the state to on which to turn on all corner lights.
    :return: None
    """
    state[0] = '#'
    state[WIDTH - 1] = '#'
    state[(HEIGHT - 1) * WIDTH] = '#'
    state[(HEIGHT - 1) * WIDTH + WIDTH - 1] = '#'


with open('day18input.txt', 'r') as f:
    # I'm old school and where you have an array with fixed dimensions, I like to just use a flat list and offsets
    # for each row. This also means we don't have to deep copy when setting up a new state, etc
    part1_state = reduce(operator.add, [list(x.strip()) for x in f.readlines()])
    # Take a copy for part 2, and set the corner lights.
    part2_state = part1_state[:]
    setcorners(part2_state)

    # Both part 1 and 2 are 100 iterations. Evolve both states and make sure the corners are on for the part 2 state
    for i in range(100):
        part1_state = evolve(part1_state)
        part2_state = evolve(part2_state)
        setcorners(part2_state)

    # Count the number of lights on in each part
    print(len([x for x in part1_state if x == '#']))
    print(len([x for x in part2_state if x == '#']))
