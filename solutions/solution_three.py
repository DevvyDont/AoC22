from typing import List

from solution import Solution


# Essentially a letter, putting into a class to make it more readable
class RucksackItem:

    def __init__(self, letter):
        self.letter = letter

    # Convert the char to a number with 'a' being 1, 'z' being 26, 'A' being 27, 'Z' being 52
    def priority(self):

        # If the ord is somewhere between a and z,
        if ord('a') <= ord(self.letter) <= ord('z'):
            return ord(self.letter) - ord('a') + 1

        # if the ord is somewhere between A and Z
        if ord('A') <= ord(self.letter) <= ord('Z'):
            return ord(self.letter) - ord('A') + 27

        raise Exception(f"Invalid item: {self.letter}")

    def __eq__(self, other):
        return other.letter == self.letter

    def __repr__(self):
        return self.letter


class RucksackCompartment:

    def __init__(self, items: List[RucksackItem]):
        self.items: List[RucksackItem] = items

    def __iter__(self):
        return self.items.__iter__()

    def __contains__(self, item: RucksackItem):
        for contained_item in self.items:
            if contained_item == item:
                return True

        return False

    def __repr__(self):
        return ''.join([repr(item) for item in self.items])


class Rucksack:

    def __init__(self, raw_string: str):

        # Split the string into two
        partition = int(len(raw_string) / 2)
        left = raw_string[:partition]
        right = raw_string[partition:]

        if len(left) != len(right):
            raise Exception

        # Make the left compartment out of the left items
        left_items: List[RucksackItem] = []
        for item in left:
            left_items.append(RucksackItem(item))

        self.left_compartment = RucksackCompartment(left_items)

        # Now same for the right
        right_items: List[RucksackItem] = []
        for item in right:
            right_items.append(RucksackItem(item))

        self.right_compartment = RucksackCompartment(right_items)

    def all(self) -> List[RucksackItem]:
        return self.left_compartment.items + self.right_compartment.items

    def __contains__(self, item: RucksackItem):
        for contained_item in self.all():
            if contained_item == item:
                return True

        return False

    def __repr__(self):
        return f"left: {self.left_compartment} | right: {self.right_compartment}"


class SolutionThree(Solution):

    def __init__(self, inputfile):
        super().__init__(inputfile)

        # Construct the rucksacks
        self.rucksacks: List[Rucksack] = []
        for line in self.readlines():
            self.rucksacks.append(Rucksack(line.strip()))

    def solve_p1(self):

        # Keep track of rucksack items that are duplicates
        duplicate_items: List[RucksackItem] = []

        # Loop through all the rucksacks
        for rucksack in self.rucksacks:

            # Keep track of duplicates specifically for this rucksack
            rucksack_duplicates: List[RucksackItem] = []

            # For this rucksack, loop through the first compartment
            for item in rucksack.left_compartment:

                # If this item was already checked skip
                if item in rucksack_duplicates:
                    continue

                # For every item in this compartment, check for duplicates in the other compartment
                if item in rucksack.right_compartment:
                    rucksack_duplicates.append(item)
                    break

            # Now add the dupes we found to the total
            duplicate_items.extend(rucksack_duplicates)

        # Add up all the priorities of these duplicates
        total = 0
        for dupe in duplicate_items:
            total += dupe.priority()

        return total

    def solve_p2(self):

        all_duplicates: List[RucksackItem] = []

        # Iterate by 3 over all the rucksacks
        for index in range(0, len(self.rucksacks), 3):
            # Extract the group of three
            one, two, three = self.rucksacks[index:index + 3]

            # No need to check something twice
            already_checked_items: List[RucksackItem] = []

            # Since we are looking for a duplicate in all 3, we only need to check one rucksack and see if an item
            # is contained in both two and three
            for item in one.all():

                if item in already_checked_items:
                    continue

                already_checked_items.append(item)

                if item in two and item in three:
                    all_duplicates.append(item)

        total = 0
        for dupe in all_duplicates:
            total += dupe.priority()

        return total
