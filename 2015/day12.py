#!/usr/bin/env python3
import json
import re

# Part 1, te quick, nasty way. It works.
NUMBERS = re.compile(r'(-?\d+)')


# Part 2. JSON parses to a tree structure, the easiest way to examine a whole tree is to use a recursive function to
# examine the subtrees by calling itself.
def examine(node):
    # If this node is a dictionary, and none of the values are RED, return the sum of the subtrees
    if isinstance(node, dict) and "red" not in node.values():
        return sum(examine(v) for v in node.values())
    # If it's a list, sum of the subtrees
    elif isinstance(node, list):
        return sum(examine(v) for v in node)
    # And just a number, out leaf node and terminating condition.
    elif isinstance(node, int):
        return node
    # Return 0 if we encounter anything else.
    return 0


with open('day12input.txt', 'r') as f:
    line = f.readline()

    # Part 1, just find all the numbers and add them all together.
    print(sum([int(x) for x in NUMBERS.findall(line)]))

    # Part 2, ignore any subtrees that are in a dictionary where there's a value that is "red"
    tree = json.loads(line)
    print(examine(tree))
