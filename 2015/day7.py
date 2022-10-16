#!/usr/bin/env python3
import re
from typing import Optional, Dict

# This problem involves running through a list of instructions that aren't in an order that necessarily makes sense. The
# approach I have gone for is a state machine that retries failed instructions, so I don't really have to worry about
# instruction ordering.

# REGEXES for parsing individual lines of the file. I did eventually discover that numbers and wire labels can be used
# interchangeably in the input, so I moved from a simple dictionary to a State class with a resolve method. So these
# expressions just match and pull out all the operands. In theory, we can probably work out which one to use with basic
# substring matches, but I can't be arsed.
INPUT_REGEX = re.compile(r'^(?P<value>[a-z]+|\d+) -> (?P<output>[a-z]+)$')
AND_REGEX = re.compile(r'^(?P<input_a>[a-z]+|\d+) AND (?P<input_b>[a-z]+|\d+) -> (?P<output>[a-z]+)$')
OR_REGEX = re.compile(r'^(?P<input_a>[a-z]+|\d+) OR (?P<input_b>[a-z]+|\d+) -> (?P<output>[a-z]+)$')
NOT_REGEX = re.compile(r'^NOT (?P<input>[a-z]+|\d+) -> (?P<output>[a-z]+|\d+)$')
LSHIFT_REGEX = re.compile(r'^(?P<input>[a-z]+|\d+) LSHIFT (?P<param>\d+) -> (?P<output>[a-z]+)$')
RSHIFT_REGEX = re.compile(r'^(?P<input>[a-z]+|\d+) RSHIFT (?P<param>\d+) -> (?P<output>[a-z]+)$')


class State:
    """
    State class, stores the current wire values and resolved inputs to their values, either by returning them directly
    for numeric ones, or reading them from memory. Also provides a write method for setting wire values. For part 2, it
    asks to override the input value of b with the output value of a from part 1, so to facilitate this I allowed for
    specifying initial values and made it write-once, so subsequent writes to the same wire are ignored otherwise you
    get the wrong answer for part 2, but didn't affect part 1 for me.
    """

    def __init__(self, initial: Optional[Dict[str, int]] = None):
        # Create an initial memory storage dictionary
        self.__memory: Dict[str, int] = {}
        # If an initial dictionary has been passed, merge in those values
        if initial:
            self.__memory.update(initial)

    def resolve_value(self, identifier: str) -> Optional[int]:
        """
        Resolve and identifier into a usable value. If the identifier is numeric, convert to an int. Otherwise, attempt
        to look it up in the state memory. If it doesn't exist, return None so that the instruction can fail gracefully.

        :param identifier: the identifier for which to resolve the value
        :return: the value of the identifier, or None if it can't be resolved
        """
        if identifier.isnumeric():
            return int(identifier)
        elif identifier in self.__memory:
            return self.__memory[identifier]
        return None

    def write_memory(self, location: str, value: int) -> None:
        """
        Write a value to a given memory location, but only if the value hasn't already been written.

        :param location: the memory location to write
        :param value: the value to write to the location
        :return: None
        """
        if location not in self.__memory:
            self.__memory[location] = value


class Node:
    """
    Base class for all operations, define the basic methods and constructors. I probably should create this as an
    Abstract Base Class, but for an informal programming challenge I don't think correctness is that important.

    This class was called Node because originally I was going to model the entire system as a graph, wires being the
    edges and these operations being the vertices, but I'm happy with the implementation I ended up with.
    """

    def __init__(self, output: str):
        """
        Initialise a Node instance, with the provided output memory location,
        :param output: the memory location in which to write the result
        """
        self._output = output

    def execute(self, state: State) -> bool:
        """
        Execute the instruction against the state. Returns False if the operation can't complete because a wire value
        hasn't been written yet, allowing for re-queuing failed instructions.

        :param state: The state to operate on
        :return: True if the instruction was successful, False otherwise.
        """
        return True

    @staticmethod
    def try_parse(expression):
        """
        Try to parse the instruction, returning a new instance of this node.
        :param expression: the instruction line to try to parse
        :return: A node or subclass instance if the parse was successful, None otherwise.
        """
        return None


class InputNode(Node):
    """
    Copy the input value into the output location.
    """

    def __init__(self, output: str, value: str):
        super(InputNode, self).__init__(output)
        self.__value = value

    def execute(self, state: State) -> bool:
        value = state.resolve_value(self.__value)
        if value is not None:
            state.write_memory(self._output, value)
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = INPUT_REGEX.match(expression)
        if output:
            return InputNode(output.group('output'), output.group('value'))
        return None


class NotNode(Node):
    """
    A node that inverts all the bits in the input. The problem specification says they're fixed-width 16-bit integers,
    but python integers are not fixed length, so we need to be a little clever about this, setting the 17th bit by
    or-ing 65536 before the inversion.
    """

    def __init__(self, output: str, input_a: str):
        super(NotNode, self).__init__(output)
        self.__input = input_a

    def execute(self, state: State) -> bool:
        value = state.resolve_value(self.__input)
        if value is not None:
            state.write_memory(self._output, ~ (value | 65536))
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = NOT_REGEX.match(expression)
        if output:
            return NotNode(output.group('output'), output.group('input'))
        return None


class BinaryNode(Node):
    """
    Base class for operators that take two inputs
    """

    def __init__(self, output: str, input_a: str, input_b: str):
        super(BinaryNode, self).__init__(output)
        self._input_a = input_a
        self._input_b = input_b


class AndNode(BinaryNode):
    """
    Performs a bitwise and on the two inputs
    """

    def execute(self, state: State) -> bool:
        value_a, value_b = state.resolve_value(self._input_a), state.resolve_value(self._input_b)
        if value_a is not None and value_b is not None:
            state.write_memory(self._output, value_a & value_b)
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = AND_REGEX.match(expression)
        if output:
            return AndNode(output.group('output'), output.group('input_a'), output.group('input_b'))
        return None


class OrNode(BinaryNode):
    """
    Performs a bitwise or on the two inputs
    """

    def execute(self, state: State) -> bool:
        value_a, value_b = state.resolve_value(self._input_a), state.resolve_value(self._input_b)
        if value_a is not None and value_b is not None:
            state.write_memory(self._output, value_a | value_b)
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = OR_REGEX.match(expression)
        if output:
            return OrNode(output.group('output'), output.group('input_a'), output.group('input_b'))
        return None


class ShiftNode(Node):
    """
    Base class for shift operations
    """

    def __init__(self, output: str, input_a: str, param: int):
        super(ShiftNode, self).__init__(output)
        self._input = input_a
        self._param = param


class LShiftNode(ShiftNode):
    """
    Left bit shit
    """

    def execute(self, state: State) -> bool:
        value = state.resolve_value(self._input)
        if value is not None:
            state.write_memory(self._output, value << self._param)
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = LSHIFT_REGEX.match(expression)
        if output:
            return LShiftNode(output.group('output'), output.group('input'), int(output.group('param')))
        return None


class RShiftNode(ShiftNode):
    """
    Right bit shift
    """

    def execute(self, state) -> bool:
        value = state.resolve_value(self._input)
        if value is not None:
            state.write_memory(self._output, value >> self._param)
            return True
        return False

    @staticmethod
    def try_parse(expression: str) -> Optional[Node]:
        output = RSHIFT_REGEX.match(expression)
        if output:
            return RShiftNode(output.group('output'), output.group('input'), int(output.group('param')))
        return None


# Simple list of parse functions we can loop over and try on each line.
PARSERS = [
    InputNode.try_parse,
    NotNode.try_parse,
    AndNode.try_parse,
    OrNode.try_parse,
    LShiftNode.try_parse,
    RShiftNode.try_parse
]

with open('day7input.txt', 'r') as f:
    # Initial state for part 1 and a list to store the instructions.
    part1_state = State()
    part1_instructions = []

    # Parse the code file into the instructions list by trying each parse expression until one matches. When it does,
    # append it to the list of instructions.
    for line in f.readlines():
        for parser in PARSERS:
            res = parser(line)
            if res:
                part1_instructions.append(res)
                break
        else:
            # Safety net if a line fails to parse.
            raise Exception(f"Parsing failed: {line}")

    # Part 2 uses the same instructions as part one, but we use the list as a dequeue, so we need to take a copy.
    part2_instructions = part1_instructions[:]

    # Loop until we have no further instructions, take the first one, try to run it, and if it fails add it back to the
    # end of the list to try again later. If an instruction fails, it will be because an input is not yet available but
    # may be later.
    while part1_instructions:
        instruction = part1_instructions.pop(0)
        if not instruction.execute(part1_state):
            part1_instructions.append(instruction)

    # The result for part 1 is the value for wire a
    part1_result = part1_state.resolve_value('a')

    # And the initial state for part 2 is setting b to the value of a from part 1
    part2_state = State({'b': part1_result})

    # Do the same as for part 1.
    while part2_instructions:
        instruction = part2_instructions.pop(0)
        if not instruction.execute(part2_state):
            part2_instructions.append(instruction)

    # And as part 1, the result is the value at a
    part2_result = part2_state.resolve_value('a')

    # Print the results
    print(part1_result)
    print(part2_result)
