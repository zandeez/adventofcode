#!/usr/bin/env python3
from typing import List

# We're going to shift everything to 0 from the ascii codes they are and just operate on simple numbers.
BASE = ord('a')
# Top end limit to loop around on
LIMIT = ord('z') - BASE + 1

# These are the letters that can't appear at all.
BANNED = [
    ord('i') - BASE,
    ord('l') - BASE,
    ord('o') - BASE
]


# Rule 1: 3 consecutive letters, eg, abc, def
def rule1(password: List[int]):
    # Simple, loop over length - 2, check for the increments.
    for i in range(len(password) - 2):
        if password[i] + 1 == password[i + 1] and password[i] + 2 == password[i + 2]:
            return True
    return False


# Rule 2: No banned letters, i, l or o
def rule2(password: List[int]):
    # make sure that none of the banned letters are in the password
    return not any([
        x in password for x in BANNED
    ])


# Rule 3, two sets of unique pairs
def rule3(password: List[int]):
    # Create a set for the pairs (sets don't allow duplicates)
    pairs = set()
    # Loop over the password checking for pairs
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            # Add the pair to the set
            pairs.add(password[i])
    # Make sure we have at least 2
    return len(pairs) >= 2


# List of rule functions
RULES = [
    rule1,
    rule2,
    rule3
]


# Valid if all rules are true
def valid(password: List[int]):
    return all(
        x(password) for x in RULES
    )


# Code to do the increment
def increment(password: List[int]):
    # Increase the last letter
    password[-1] += 1
    # Then check for ovcerflows, starting at the end
    for i in range(len(password) - 1, -1, -1):
        # if any is at the limit, increment the item to the left, and reset to 0
        if password[i] >= LIMIT:
            password[i] = 0
            # unless we're at the first character, because there's nothing to the left!
            if i > 0:
                password[i - 1] += 1
    return password


with open('day11input.txt', 'r') as f:
    # Read the password
    this_password = [ord(x) - BASE for x in f.readline().strip()]
    # Part 2 is the next password after then end of part 1. So jus do it twice.
    for i in range(2):
        # because the current passwrd is valid, we need to increment once before we start.
        increment(this_password)
        # and keep incrementing until we have a valid password
        while not valid(this_password):
            increment(this_password)

        # Convert back to a string and print
        print(''.join([
            chr(x + BASE) for x in this_password
        ]))
