#!/usr/bin/env python3

import hashlib

# This puzzle input isn't provided as a file, but I've made it one any.
with open('day4input.txt', 'r') as f:
    secret = f.readline()
    # The current number we're testing.
    index = 0
    # Going to use this as bit flags, bit 1 if we've found part 1, bit 2 for part 2.
    found = 0

    # Loop until both are found, so both the 1 and 2 bits, making 3
    while found < 3:
        # Create the hash as per the problem spec
        this_hash = hashlib.md5((secret + str(index)).encode('ascii'))

        # Have we got 6 0's ? we do this first to prevent 5 0's matching for 6.
        # Check the flags, too to make sure we've not already found 1 or 2
        if found & 2 != 2 and this_hash.hexdigest().startswith('0' * 6):
            # |= is the "or assign" operator, this sets bit 2.
            found |= 2
            print("Part 2:", index)
        elif found & 1 != 1 and this_hash.hexdigest().startswith('0' * 5):
            found |= 1
            print("Part 1:", index)

        # Increment the index
        index += 1
