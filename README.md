Advent of Code
==============

These are my solutions to Advent of Code in Python.

I have gone back to previous years in an attempt to complete all tasks.

My input files are excluded, and there are no guarantees these are the best solutions.

You will probably quickly notice that I like the virtual machine approach. That is building an instruction parser and
executor. The input is fed into an instruction parser, and those instructions are then executed on a backing data store
of some kind, before returning the main result. This can often make part 2 of most puzzles straightforward by simply
expanding the capabilities of the machine produced for part 1.