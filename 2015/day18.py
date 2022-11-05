#!/usr/bin/env python3
import operator
from functools import reduce

WIDTH = 100
HEIGHT = 100

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
    new_state = state[:]
    for this_x, this_y in [(x, y) for x in range(WIDTH) for y in range(HEIGHT)]:
        count = 0
        for test_x, test_y in [(this_x + x, this_y + y) for x, y in TESTS]:
            if min(test_x, test_y) < 0 or max(test_x, test_y) > WIDTH - 1:
                continue
            if state[test_y * WIDTH + test_x] == '#':
                count += 1

            if state[this_y * WIDTH + this_x] == '.' and count == 3:
                new_state[this_y * WIDTH + this_x] = '#'
            elif state[this_y * WIDTH + this_x] == '#' and (count == 2 or count == 3):
                new_state[this_y * WIDTH + this_x] = '#'
            else:
                new_state[this_y * WIDTH + this_x] = '.'

    return new_state


def setcorners(state):
    state[0] = '#'
    state[WIDTH - 1] = '#'
    state[(HEIGHT - 1) * WIDTH] = '#'
    state[(HEIGHT - 1) * WIDTH + WIDTH - 1] = '#'


with open('day18input.txt', 'r') as f:
    part1_state = reduce(operator.add, [list(x.strip()) for x in f.readlines()])
    part2_state = part1_state[:]
    setcorners(part2_state)

    for i in range(100):
        part1_state = evolve(part1_state)
        part2_state = evolve(part2_state)
        setcorners(part2_state)

    print(len([x for x in part1_state if x == '#']))
    print(len([x for x in part2_state if x == '#']))
