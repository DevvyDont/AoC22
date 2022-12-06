from typing import SupportsIndex, List

from solution import Solution


class Crate:

    def __init__(self, letter: str):
        self.letter: str = letter

    def __repr__(self):
        return self.letter


class CrateStack(list):

    def queue(self, element: Crate):
        self.append(element)

    def __repr__(self):
        return f"Stack: {super().__repr__()}"


class SolutionFive(Solution):

    def __init__(self, inputfile):
        super().__init__(inputfile)

        self.stacks: List[CrateStack] = []

        all_lines = self.readlines_clean()

        # Find the index of the first occurence of a blank line
        where_to_split = all_lines.index('')
        # The initial crate config is the beginning to this split
        self.crate_construct = all_lines[:where_to_split]
        # The rest are the instructions
        self.crate_instructions = all_lines[where_to_split+1:]

    # Given only the lines that contain stack information construct the stacks
    def _construct_stacks(self, lines: List[str]):

        self.stacks.clear()

        # By analyzing the last line, we can find how many stacks we need to construct
        num_stacks = int(lines[-1][-1])
        for _ in range(num_stacks):
            self.stacks.append(CrateStack())

        # Now that the stacks are made we can start making the stacks, we just iterate over the lines we have
        # from the bottom up but do not include the last element as its just the numbers
        for initial_config_line in lines[-1::-1]:
            # We are given a line like so: [F] [N] [F] [V] [Q] [Z] [Z] [T] [Q]
            # Iterate over the string starting at index 1, step by 4. real stack index will be index / 4
            for string_index in range(1, len(initial_config_line), 4):
                stack_index = string_index // 4
                char = initial_config_line[string_index]

                # If the character here is a space, then we don't have to do anything
                if char == ' ':
                    continue

                # Otherwise, add the crate to its stack
                self.stacks[stack_index].queue(Crate(char))

        # The stacks should now be constructed

    def _perform_one_at_a_time_move(self, amount, source, destination):
        # For as many times as we are moving a crate
        for _ in range(amount):
            # From the source, pop the crate
            popped_crate: Crate = self.stacks[source].pop()
            # Queue it to the destination
            self.stacks[destination].queue(popped_crate)

    def _perform_multiple_move(self, amount, source, destination):
        # Pop the crates off into a separate list
        popped_crates: List[Crate] = []
        for _ in range(amount):
            crate = self.stacks[source].pop()
            popped_crates.append(crate)

        # Now place the crates on the new stack in reverse order
        for crate in popped_crates[::-1]:
            self.stacks[destination].queue(crate)

    # Perform the operations given only the instructions
    def _perform_instructions(self, lines: List[str], one_at_a_time=True):
        # Given a list of lines formatted like so: move 1 from 8 to 1
        # We can split these instructions by spaces to get a list
        for instruction in lines:
            # Extract the information from the list, double underscore vars are just garbage and we dont need them
            __move, move_amount, __from, source_index, __to, destination_index = instruction.split(' ')

            # Transform the vars we care about into ints
            move_amount = int(move_amount)
            source_index = int(source_index)
            destination_index = int(destination_index)

            # Our indeces are 0 based, the instructions are 1 based, subtract them by 1
            source_index -= 1
            destination_index -= 1

            if one_at_a_time:
                self._perform_one_at_a_time_move(move_amount, source_index, destination_index)
            else:
                self._perform_multiple_move(move_amount, source_index, destination_index)

    def solve_p1(self):
        # Create the initial configuration
        self._construct_stacks(self.crate_construct)

        # Perform the instructions given
        self._perform_instructions(self.crate_instructions, one_at_a_time=True)

        # Report what is at the top of each stack
        return''.join([stack[-1].letter for stack in self.stacks])

    def solve_p2(self):
        # Create the initial configuration
        self._construct_stacks(self.crate_construct)

        # Perform the instructions given
        self._perform_instructions(self.crate_instructions, one_at_a_time=False)

        # Report what is at the top of each stack
        return ''.join([stack[-1].letter for stack in self.stacks])
