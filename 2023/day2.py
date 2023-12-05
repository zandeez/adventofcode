#!/usr/bin/env python3
import re
from typing import Dict, List

# Top level line expression
GAME_LINE = re.compile(r"^Game (?P<game_id>\d+): (?P<turns>.*)$")
# Each turn for a game
DRAW = re.compile("(?P<qty>\d+) (?P<colour>red|green|blue)")

with open("day2.txt", "r") as f:
    data = f.readlines()

# This is a fancy dictionary comprehension the parses the whole input in a single expression, using the new walrus
# operator to get the results of the regular expression. The ourtermost comprehension gets the game ID and the turns,
# The mid expression creates the list of turns in that game, and the most inner one parses individual cube counts.
GAMES: Dict[int, List[Dict[str, int]]] = {int(match.group("game_id")): [
    {m.group("colour"): int(m.group("qty")) for y in turn.split(',') if (m := DRAW.search(y))
     } for turn in match.group("turns").split(";")
] for line in data if (match := GAME_LINE.match(line))}


# A helper function that finds the maximum number of a named colour in a list of turns.
def max_of_colour(turns: List[Dict[str, int]], colour: str) -> int:
    return max([x.get(colour, 0) for x in turns])


# Part 1, get the game IDs of the games where the maximum number of each colour is less than the specified amount
PT1 = sum([k for k, v in GAMES.items() if
           max_of_colour(v, 'red') < 13 and max_of_colour(v, 'green') < 14 and \
           max_of_colour(v, 'blue') < 15])
print(PT1)

# Part 1, get the maximum of each colour from each game, multiply together, then sum
PT2 = sum([max_of_colour(i, 'red') * max_of_colour(i, 'green') * max_of_colour(i, 'blue') for i in GAMES.values()])
print(PT2)
