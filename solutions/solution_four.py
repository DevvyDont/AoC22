from solution import Solution


class SolutionFour(Solution):

    def __init__(self, inputfile):
        super().__init__(inputfile)
        self.pairs = []

        for line in self.readlines():
            range_1, range_2 = line.split(',')
            range_1_min, range_1_max = range_1.split('-')
            range_2_min, range_2_max = range_2.split('-')
            self.pairs.append(
                ((int(range_1_min), int(range_1_max)), (int(range_2_min), int(range_2_max)))
            )

    def overlaps_completely(self, pair1: tuple, pair2: tuple):
        # An overlap occurs if in either pair, the max and min are both contained in its partner
        pair1_min, pair_1_max = pair1
        pair2_min, pair_2_max = pair2
        # First check pair 1
        if pair1_min >= pair2_min and pair_1_max <= pair_2_max:
            return True

        # Now check pair 2
        if pair2_min >= pair1_min and pair_2_max <= pair_1_max:
            return True

        # No complete overlaps
        return False

    def overlaps_partially(self, pair1: tuple, pair2: tuple):
        # An overlap occurs if in either pair, either the min or max is on or in between the other min or max
        pair1_min, pair_1_max = pair1
        pair2_min, pair_2_max = pair2

        # First check pair 1
        if pair2_min <= pair1_min <= pair_2_max or pair2_min <= pair_1_max <= pair_2_max:
            return True

        # Now check pair 2
        if pair1_min <= pair2_min <= pair_1_max or pair1_min <= pair_2_max <= pair_1_max:
            return True

        return False

    def solve_p1(self):

        num_overlap = 0
        # Loop through all pairs, see if there is overlap
        for pair in self.pairs:
            range1, range2 = pair
            if self.overlaps_completely(range1, range2):
                num_overlap += 1

        return num_overlap

    def solve_p2(self):

        num_overlap = 0
        # Loop through all pairs, see if there is overlap
        for pair in self.pairs:
            range1, range2 = pair
            if self.overlaps_partially(range1, range2):
                num_overlap += 1

        return num_overlap
