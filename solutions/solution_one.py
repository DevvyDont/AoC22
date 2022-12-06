from typing import List

from solution import Solution


class Snack:

    def __init__(self, calories: int):
        self.calories: int = calories

    def __repr__(self):
        return f"Snack with {self.calories} calories"


class Elf:

    # Snacks are list of calories per snack
    def __init__(self, snacks: List[Snack]):
        self.snacks: List[Snack] = snacks

    def __repr__(self):
        return f"Elf with {self.get_total_calories()} calories ({len(self.snacks)} snacks)"

    def get_total_calories(self) -> int:

        total = 0
        for snack in self.snacks:
            total += snack.calories

        return total


class SolutionOne(Solution):

    def _construct_elves(self) -> List[Elf]:

        elves: List[Elf] = []
        current_snacks: List[Snack] = []

        # Loop through every line in the input
        for line in self.readlines():

            # If the line is a blank and theres information stored in current snacks, append a new elf
            if line.strip() == '' and len(current_snacks) > 0:
                elves.append(Elf(current_snacks.copy()))
                current_snacks.clear()
                continue

            # Edge case, if the line is just blank go next
            if line.strip() == '':
                continue

            # We most likely have a snack calorie number, add it to the list
            current_snacks.append(Snack(int(line)))

        return elves

    def solve_p1(self):
        elves = self._construct_elves()
        return max(elves, key=lambda elf: elf.get_total_calories())

    def solve_p2(self):
        elves = self._construct_elves()
        elves.sort(key=lambda elf: elf.get_total_calories(), reverse=True)
        top_3 = elves[:3]
        total = 0
        for elf in top_3:
            total += elf.get_total_calories()

        return total
