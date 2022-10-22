#!/usr/bin/env python3
import itertools
import re
from collections import defaultdict
from typing import Dict

# This one is a prime example of a directed graph, that is the cost of moving between one node and back again is not
# symmetrical. This task wants us to create a circular graph with the highest total edge score. As always, I'm not quite
# going to do to it quite like that.

# Input parser regular expression.
PARSER = re.compile(
    r'^(?P<person>.*?) would (?P<operator>gain|lose) (?P<quantity>\d+) happiness units by sitting next to '
    r'(?P<neighbour>.*?).$')


def calc_best_score(scores: Dict[str, Dict[str, int]]) -> int:
    # This is circular, so starting point shouldn't matter. We can reduce the number of permutations by selecting a
    # single starting point
    people = list(scores.keys())
    start = people.pop(0)
    best_score = 0

    # We need each possible permutation of the smaller people list
    for permutation in itertools.permutations(people, len(people)):
        # Add our designated start person to both ends of the list.
        this_permutation = [start] + list(permutation) + [start]
        this_score = 0

        # Loop forwards, adding up the scores
        for i in range(len(this_permutation) - 1):
            this_score += scores[this_permutation[i]][this_permutation[i + 1]]

        # And backwards, because each person is sitting next to two people
        for i in range(len(this_permutation) - 1, 0, -1):
            this_score += scores[this_permutation[i]][this_permutation[i - 1]]

        # Store the best score so far
        if this_score > best_score:
            best_score = this_score

    return best_score


with open('day13input.txt', 'r') as f:
    # Scores for sitting next to people.
    global_scores: Dict[str, Dict[str, int]] = defaultdict(dict)

    # Load in the data file
    for line in f.readlines():
        parsed = PARSER.match(line.strip())
        assert parsed is not None

        # load the number of happiness units
        quantity = int(parsed.group('quantity'))
        # if the operator is "lose" negate the amount
        if parsed.group('operator') == 'lose':
            quantity *= -1

        # And add into the dictionary
        global_scores[parsed.group('person')][parsed.group('neighbour')] = quantity

    # Call our function to calculate the best score of this score table
    part1_score = calc_best_score(global_scores)
    print(part1_score)

    # Add ourselves into the mix, setting the happiness scores to 0 both inbound and outbound
    for k in list(global_scores.keys()):
        global_scores[k]['Me'] = 0
        global_scores['Me'][k] = 0

    # And call our function again, based on the new score table
    part2_score = calc_best_score(global_scores)
    print(part2_score)
