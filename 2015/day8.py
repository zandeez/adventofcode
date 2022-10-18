#!/usr/bin/env python3
import re

HEX_REGEX = re.compile(r'\\x[0-9a-fA-F]{2}')

with open('day8input.txt', 'r') as f:
    # Newlines are your enemy in this task
    lines = [x.strip() for x in f.readlines()]

    # Part 1 is fairly straightforward.
    stored = sum([len(x) for x in lines])

    # And decode the stored forms using the dead simple rules given.
    # It doesn't actually matter what the hex code is, as we're just worried about the length
    literal = sum([len(
        HEX_REGEX.sub("'", x[1:-1].replace("\\\\", "\\").replace("\\\"", "\""))) for x in lines
    ])

    # Part 2 is to double-encode the already encoded
    double = sum([
        # DO THE SLASHES FIRST. Otherwise, it then doubles up the escapes for the quotes.
        len("\"" + x.replace("\\", "\\\\").replace("\"", "\\\"") + "\"")
        for x in lines])

    print(stored - literal)
    print(double - stored)
