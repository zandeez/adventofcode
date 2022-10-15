#!/usr/bin/env python3

with open('day2input.txt', 'r') as f:
    paper_total, ribbon_total = 0, 0

    for preset in f.readlines():
        # Split and sort the dimensions, as we need the smallest side specifically.
        x, y, z = sorted(map(int, preset.split('x')))
        # Total cuboid surface area + an extra smallest face, so 3 x the smallest face and 2 x each of the others.
        this_present_paper = 3 * x * y + 2 * y * z + 2 * x * z
        # Total volume + smallest face perimeter
        this_present_ribbon = x * y * z + 2 * x + 2 * y
        # Add them to the running totals.
        paper_total += this_present_paper
        ribbon_total += this_present_ribbon

    print(paper_total)
    print(ribbon_total)
