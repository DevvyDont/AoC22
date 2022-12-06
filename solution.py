from typing import List


class Solution:

    def __init__(self, inputfile):
        self.inputfile = inputfile

    def readlines(self) -> List[str]:
        with open(self.inputfile, 'r') as f:
            return f.readlines()

    # Same as readlines, but removes \n chars
    def readlines_clean(self) -> List[str]:
        old = self.readlines()
        for index in range(len(old)):
            old[index] = old[index].replace('\n', '')

        return old

    def solve_p1(self):
        raise NotImplementedError

    def solve_p2(self):
        raise NotImplementedError
