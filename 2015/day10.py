#!/usr/bin/env python3

# This one is just and iterative process, that loops over a string of numbers and produces a new string of numbers.
# I've simply created a function that does a single iteration, and we can just reuse it over and over.
def process(input_str: str) -> str:
    # This will eventually be the output string
    out = ''
    # An initial count. Once we're processing this it'll never be 0 again.
    count = 0
    # And any non-numeric so the first character is matched. Actually doesn't matter what this is.
    current = 'n'
    # Loop over the string. doesn't actually matter what type they are so don't worry about casting.
    for c in input_str:
        # If it's the same as the last character, increment our counter
        if c == current:
            count += 1
        # Otherwise add the count and character to the string, update the last character, and reset the count to 1
        else:
            if count > 0:
                out += f"{count}{current}"
            count = 1
            current = c
    # Add on anything remaining and return the result.
    out += f"{count}{current}"
    return out


# Single value input, but I like to keep everything uniform, so saved it in a file,
with open('day10input.txt', 'r') as f:
    # Read the single line
    data = f.readline().strip()
    # Do it 40 times, and print the length
    for i in range(40):
        data = process(data)
    print(len(data))

    # Part 2 asks to do it 50 times, so 10 more. Let's just carry on where we left off.
    for i in range(10):
        data = process(data)
    print(len(data))
