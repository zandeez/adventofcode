#!/usr/bin/env python3

import re

# BEGIN PART 1 HELPERS

# Simple list of vowels
VOWELS = 'aeiou'

# This reges uses a backreference (\1) to match again a group that has already matched. In this case, the group will be
# a single letter, a-z, and the backreference then matches it. so aa, bb, cc, etc will match.
REPEATED_REGEX = re.compile(r'([a-z])\1')

# A simple list again of defined strings
NAUGHTY_SUBSTINGS = [
    'ab', 'cd', 'pq', 'xy'
]


# Check if a string has 3 vowels
def has_3_vowels(input_string):
    # Simple, filter out all the non-vowels, count what remains.
    return len([x for x in input_string if x in VOWELS]) >= 3


# Check for double-letter patterns
def has_repeated_letters(input_string):
    # Dead simple, just perform the regex and ensure that it doesn't return None.
    return REPEATED_REGEX.search(input_string) is not None


# Check for the naughty strings
def has_no_naughty_substring(input_string):
    # Again, super simple. Over the list of strings, map to a list of True/False on whether it is present
    # in the input_string. Then use any() while will return True is any of the items in the new list are True.
    return not any([x in input_string for x in NAUGHTY_SUBSTINGS])


# Compund predicate for part 1, that performs all three checks together.
def is_nice_part1(input_string):
    return has_3_vowels(input_string) and has_repeated_letters(input_string) and has_no_naughty_substring(input_string)


# BEGIN PART 2 HELPERS

# As before, use a backrefence to match a set of two letters, that is then repeated, but somewhere else. The .* allows
# for them to maybe not be directly next to each other.
DOUBLE_REPEATED_REGEX = re.compile(r'([a-z]{2}).*\1')
# This is for the aba or xyx pattern, basically a letter followed by any letter, then itself again.
ABA_REGEX = re.compile(r'([a-z])[a-z]\1')


def is_nice_part2(input_string):
    # Slightly simpler one this time, just perform both regexes on the string.
    return ABA_REGEX.search(input_string) and DOUBLE_REPEATED_REGEX.search(input_string)


with open('day5input.txt', 'r') as f:
    # Read all lines straight in, we're going to operate on them twice
    lines = f.readlines()
    # Filter out naughty lines according to part 1 rules
    nice_lines_part1 = [x for x in lines if is_nice_part1(x)]
    # Filter out naughty lines according to part 2 rules
    nice_lines_part2 = [x for x in lines if is_nice_part2(x)]

    # Print the number of lines remaining
    print(len(nice_lines_part1))
    print(len(nice_lines_part2))
