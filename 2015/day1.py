#!/usr/bin/env python3

# This isn't 100% necessary, but makes life easier alter when mapping the character to a movement.
MOVES = {
    '(': 1,
    ')': -1
}

# Open the input file
with open('day1input.txt', 'r') as f:
    # read all the data and initialise out position to 0, and our basement flag, to determine whether or not we've
    # visited position -1 yet.
    data = f.readline()
    pos = 0
    basement = False

    # Enumerate the list, gives us the current index that we're on as well as the character
    for i, x in enumerate(data):
        # Update the position using the mapping declared above
        pos += MOVES[x]

        # Check if we're on level -1, for the first time
        if not basement and pos == -1:
            # print the current index, +1. Enumerate starts at 0, and the problem says to start at 1
            print(i+1)
            # register that we've been to the basement
            basement = True

    # print the final position
    print(pos)
