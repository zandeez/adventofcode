#!/usr/bin/env python3
import itertools
import operator
import re
from functools import reduce

# I wonder if you can see a pattern here? I like REGEX for stripping out the useful information from strings.
PARSER = re.compile(r'^(?P<ingredient>.*?): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), '
                    r'flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)$')

# These are the properties that we use to score on.
PROPERTIES = ['capacity', 'durability', 'flavor', 'texture']

with open('day15input.txt', 'r') as f:
    # Read in our ingredients data
    ingredients = {}
    for line in f.readlines():
        parsed = PARSER.match(line.strip())
        assert parsed is not None

        properties = parsed.groupdict()
        # Some dictionary comprehension to build up the data set
        ingredients[properties['ingredient']] = {k: int(v) for k, v in properties.items() if k != 'ingredient'}

    best_score_part1, best_score_part2 = 0, 0
    # As always, there are probably easier ways to do this. Loop over all possible combinations of ingredients.
    for combination in itertools.combinations_with_replacement(ingredients.keys(), 100):
        # Condense them into a dictionary of counts of each ingredient
        counts = {k: len([x for x in combination if x == k]) for k in ingredients.keys()}

        # Ignore any recipes where the quantity of an ingredient is 0. Not 100% sure this is needed.
        if any([x == 0 for x in counts.values()]):
            continue

        # Now build a list of scores for each property. This is a bit on the wtf side for a single line. It's a dict
        # comprehension again, using to total score for each item, sum, then max with 0 so anything less than 0 is set
        # to 0
        scores = {p: max(0, sum([ingredients[k][p] * v for k, v in counts.items()]))
                  for p in PROPERTIES}

        # multiply all values to get the score
        score = reduce(operator.mul, scores.values())
        # keep the best
        best_score_part1 = max(score, best_score_part1)
        # If this recipe has exactly 500 calories, see if it is the best 500 calorie recipe for part 2
        if sum([ingredients[k]['calories'] * v for k, v in counts.items()]) == 500:
            best_score_part2 = max(score, best_score_part2)

    print(best_score_part1)
    print(best_score_part2)
