#!/usr/bin/env python3
import re
from typing import List

# Part 1: Find the first number, then optionally a second but with a GREEDY match anything in the middle, to get the
# last one.
PT1 = re.compile(r"^.*?(\d)(.*(\d))?.*?$")
# Part 2: as above, but also match the word forms of the numbers.
PT2 = re.compile(
    r"^.*?(\d|one|two|three|four|five|six|seven|eight|nine)(.*(\d|one|two|three|four|five|six|seven|eight|nine))?.*?$")

# Table for replacing the word values with numeric ones.
REPLACE = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


# This function returns the replacement from the table above, if it exists. If not, returns the argument unmodified.
# This will replace word form numbers with the corresponding character, but leave anything already numeric alone.
def replace_name(input_string: str) -> str:
    if input_string in REPLACE:
        return REPLACE[input_string]
    return input_string


# Funky python function that takes a pattern (for part 1 or 2), the input data, and returns the result needed. This is
# one big nested list comprehension that looks awful, but it works.
def decode(pattern: re.Pattern, data: List[str]) -> int:
    # return value is the sum of all entries
    return sum(
        # we're working with strings at this point, so everything needs converting to an int
        int(
            # The number is the first digit and the last digit. There could only be one element, in which case it should
            # be duplicated.
            y[0] + y[-1]
            # for each line, once that line has been processed
        ) for y in [
            # This goes through each line, matches the pattern filters out None elements, then calls replace_name to
            # convert each matched item to its numeral.
            [replace_name(i) for i in pattern.match(line).groups() if i is not None] for line in data
        ])


with open("day1.txt", "r") as f:
    lines = f.readlines()

print(decode(PT1, lines))
print(decode(PT2, lines))
