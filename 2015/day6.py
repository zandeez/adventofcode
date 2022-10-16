#!/usr/bin/env python3
import re


# Part 1 toggle function
def toggle(cell_value):
    return not cell_value


# Part 1 turn on function
def turn_on(cell_value):
    return True


# Part 1 turn off function
def turn_off(cell_value):
    return False


# Part 2 turn on function
def increment_1(cell_value):
    return cell_value + 1


# Part 2 toggle function
def increment_2(cell_value):
    return cell_value + 2


# Part 2 turn off function
def decrement(cell_value):
    # Brightness value cannot go below 0
    if cell_value == 0:
        return 0
    return cell_value - 1


# Instruction parser regular expression. isolate and extract the function name, start and end coordinates.
INSTRUCTION_REGEX = re.compile(
    r'^(?P<instruction>turn on|turn off|toggle) (?P<startx>\d+),(?P<starty>\d+) through (?P<endx>\d+),(?P<endy>\d+)$'
)

# Part 1 instruction mapping table
INSTRUCTION_MAP_PART_1 = {
    'turn off': turn_off,
    'turn on': turn_on,
    'toggle': toggle
}

# Part 2 instruction mapping table
INSTRUCTION_MAP_PART_2 = {
    'turn off': decrement,
    'turn on': increment_1,
    'toggle': increment_2
}

# Width and height of the grid, as specified in the problem description
WIDTH = 1000
HEIGHT = 1000

with open('day6input.txt', 'r') as f:
    # Part 1 is simple on or off
    lights_part1 = [False] * WIDTH * HEIGHT
    # Part 2 is a brightness integer value
    lights_part2 = [0] * WIDTH * HEIGHT

    for line in f.readlines():
        # Parse the instruction and make sure it's not None
        parsed = INSTRUCTION_REGEX.match(line)
        assert parsed is not None

        # Loop through the x and y coordinates of the square to operate on
        for x in range(int(parsed.group('startx')), int(parsed.group('endx')) + 1):
            for y in range(int(parsed.group('starty')), int(parsed.group('endy')) + 1):
                # Run the part 1 instruction on the selected data
                lights_part1[y * WIDTH + x] = INSTRUCTION_MAP_PART_1[parsed.group('instruction')](
                    lights_part1[y * WIDTH + x])

                # Run the part 2 instruction on the selected data
                lights_part2[y * WIDTH + x] = INSTRUCTION_MAP_PART_2[parsed.group('instruction')](
                    lights_part2[y * WIDTH + x])

    # Part 1 is the number of elements that are on
    print(len([x for x in lights_part1 if x]))
    # Part 2 is the total brightness
    print(sum(lights_part2))
