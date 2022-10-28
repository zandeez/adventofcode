#!/usr/bin/env python3
import operator
import re
from functools import partial

TARGET = {
    'children': partial(operator.eq, 3),
    'cats': partial(operator.lt, 7),
    'samoyeds': partial(operator.eq, 2),
    'pomeranians': partial(operator.gt, 3),
    'akitas': partial(operator.eq, 0),
    'vizslas': partial(operator.eq, 0),
    'goldfish': partial(operator.gt, 5),
    'trees': partial(operator.lt, 3),
    'cars': partial(operator.eq, 2),
    'perfumes': partial(operator.eq, 1)
}

PARSER = re.compile(
    r'^Sue (?P<number>\d+): (?P<prop1>.*): (?P<val1>\d+), (?P<prop2>.*): (?P<val2>\d+), (?P<prop3>.*): (?P<val3>\d+)$')

with open('day16input.txt', 'r') as f:
    best_part1, score_part1 = 0, 0
    best_part2, score_part2 = 0, 0
    for line in f.readlines():
        parsed = PARSER.match(line.strip())
        assert parsed is not None

        this_aunt = {
            parsed.group('prop1'): int(parsed.group('val1')),
            parsed.group('prop2'): int(parsed.group('val2')),
            parsed.group('prop3'): int(parsed.group('val3'))
        }

        this_aunt_score_part1 = 0

        for k, v in this_aunt.items():
            if TARGET[k].args[0] == v:
                this_aunt_score_part1 += 1

        if this_aunt_score_part1 > score_part1:
            best_part1, score_part1 = int(parsed.group('number')), this_aunt_score_part1

        this_aunt_score_part2 = 0

        for k, v in this_aunt.items():
            if TARGET[k](v):
                this_aunt_score_part2 += 1

        if this_aunt_score_part2 > score_part2:
            best_part2, score_part2 = int(parsed.group('number')), this_aunt_score_part2

    print(best_part1)
    print(best_part2)
