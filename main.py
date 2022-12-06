from typing import List

from solutions.solution_five import SolutionFive
from solutions.solution_four import SolutionFour
from solutions.solution_one import SolutionOne
from solutions.solution_six import SolutionSix
from solutions.solution_two import SolutionTwo
from solutions.solution_three import SolutionThree

from solution import Solution


def main():
    sols: List[Solution] = [
        SolutionOne('input/day1'),
        SolutionTwo('input/day2'),
        SolutionThree('input/day3'),
        SolutionFour('input/day4'),
        SolutionFive('input/day5'),
        SolutionSix('input/day6'),
    ]

    for index, sol in enumerate(sols):
        print(f"Problem {index + 1}:\n\t- {sol.solve_p1()}\n\t- {sol.solve_p2()}\n\n")


if __name__ == '__main__':
    main()

