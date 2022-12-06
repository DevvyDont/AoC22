from typing import Dict, List

from solution import Solution

# Enums for the choices, double as point values as well
ROCK = 1
PAPER = 2
SCISSORS = 3

# String representation if we ever need it
CHOICE_REPR = {
    ROCK: 'Rock',
    PAPER: 'Paper',
    SCISSORS: 'Scissors'
}

# Keys for the guide
OPPONENT_CHOICE_ROCK = 'A'
OPPONENT_CHOICE_PAPER = 'B'
OPPONENT_CHOICE_SCISSORS = 'C'

BEST_CHOICE_ROCK = 'X'
BEST_CHOICE_PAPER = 'Y'
BEST_CHOICE_SCISSORS = 'Z'

OUTCOME_LOSE = 'X'
OUTCOME_DRAW = 'Y'
OUTCOME_WIN = 'Z'

# Allows us to get the choice from the guide
GUIDE_KEY_TO_CHOICE = {
    OPPONENT_CHOICE_ROCK: ROCK,
    BEST_CHOICE_ROCK: ROCK,
    OPPONENT_CHOICE_PAPER: PAPER,
    BEST_CHOICE_PAPER: PAPER,
    OPPONENT_CHOICE_SCISSORS: SCISSORS,
    BEST_CHOICE_SCISSORS: SCISSORS,
}

# Score for an outcome of a round
SCORE_LOSE = 0
SCORE_DRAW = 3
SCORE_WIN = 6


class RockPaperScissorsRoundResult:

    def __init__(self, p1_points: int, p2_points: int, reason: str):
        self.p1_points = p1_points
        self.p2_points = p2_points
        self.reason = reason

    def __repr__(self):
        return f" {self.reason} ({self.p1_points} - {self.p2_points})"


class RockPaperScissorsRound:

    def __init__(self, p1, p2):
        self.p1_choice = p1
        self.p2_choice = p2

    # Returns tuple (p1 score, p2 score, reason)
    def result(self) -> RockPaperScissorsRoundResult:

        # If both players picked the same thing
        if self.p1_choice == self.p2_choice:
            return RockPaperScissorsRoundResult(SCORE_DRAW + self.p1_choice, SCORE_DRAW + self.p2_choice, 'DRAW!')

        # If p1 won
        if (self.p1_choice == ROCK and self.p2_choice == SCISSORS) or \
                (self.p1_choice == PAPER and self.p2_choice == ROCK) or \
                (self.p1_choice == SCISSORS and self.p2_choice == PAPER):
            return RockPaperScissorsRoundResult(SCORE_WIN + self.p1_choice, SCORE_LOSE + self.p2_choice,
                                                f"P1 Wins! ({CHOICE_REPR[self.p1_choice]} beats {CHOICE_REPR[self.p2_choice]})")

        # p2 won
        return RockPaperScissorsRoundResult(SCORE_LOSE + self.p1_choice, SCORE_WIN + self.p2_choice,
                                            f"P2 Wins! ({CHOICE_REPR[self.p2_choice]} beats {CHOICE_REPR[self.p1_choice]})")


class StrategyGuide:

    # Given a list of lines construct the guide from it, it will essentially be a dict where round # -> the strategy
    # we should do
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.roundToResult: Dict[int, RockPaperScissorsRoundResult] = {}
        self.construct()

    def construct(self):
        raise NotImplementedError

    def get_round_result(self, round: int) -> RockPaperScissorsRoundResult:
        return self.roundToResult[round]

    def __repr__(self):
        return repr(self.roundToResult)


class PickStrategyGuide(StrategyGuide):

    def construct(self):

        current_round = 1

        for line in self.lines:
            # As always ignore empty lines
            if line.strip() == '':
                continue

            # It is expected that this line has 3 characters, so we should be able to split by space to get our choices
            opponent_choice, what_we_should_do = line.strip().split(' ')

            # Get the result from this potential round and add it to our guide
            round = RockPaperScissorsRound(GUIDE_KEY_TO_CHOICE[opponent_choice], GUIDE_KEY_TO_CHOICE[what_we_should_do])
            # Add the result to our guide
            result = round.result()
            self.roundToResult[current_round] = result

            current_round += 1


class OutcomeStrategyGuide(StrategyGuide):

    # what should we pick to force a win based on a choice
    def force_win(self, opponent_choice):
        return {
            ROCK: PAPER,
            PAPER: SCISSORS,
            SCISSORS: ROCK
        }[opponent_choice]

    # what should we pick to force a draw
    def force_draw(self, opponent_choice):
        return opponent_choice

    # what should we pick to force a loss
    def force_loss(self, opponent_choice):
        return {
            ROCK: SCISSORS,
            PAPER: ROCK,
            SCISSORS: PAPER
        }[opponent_choice]

    def construct(self):
        current_round = 1

        for line in self.lines:
            # As always ignore empty lines
            if line.strip() == '':
                continue

            # It is expected that this line has 3 characters, so we should be able to split by space to get our choices
            opponent_choice_encrypted, outcome_to_force_encrypted = line.strip().split(' ')
            # Convert the opponents choice
            opponent_choice = GUIDE_KEY_TO_CHOICE[opponent_choice_encrypted]
            # Bind methods to outcomes we want
            outcome_force_methods = {
                OUTCOME_LOSE: self.force_loss,
                OUTCOME_DRAW: self.force_draw,
                OUTCOME_WIN: self.force_win,
            }

            # Find what we should pick to force the outcome desired
            method = outcome_force_methods[outcome_to_force_encrypted]
            what_we_should_pick = method(opponent_choice)

            # Get the result from this potential round and add it to our guide
            round = RockPaperScissorsRound(opponent_choice, what_we_should_pick)
            # Add the result to our guide
            result = round.result()
            self.roundToResult[current_round] = result

            current_round += 1


class SolutionTwo(Solution):

    def __init__(self, inputfile):
        super().__init__(inputfile)
        self.pick_strategy_guide: StrategyGuide = PickStrategyGuide(self.readlines())
        self.outcome_strategy_guide: StrategyGuide = OutcomeStrategyGuide(self.readlines())

    def solve_p1(self):
        # Go through every round in the guide and add our points (player 2)
        total = 0
        for result in self.pick_strategy_guide.roundToResult.values():
            total += result.p2_points

        return total

    def solve_p2(self):
        # Go through every round in the guide and add our points (player 2)
        total = 0
        for result in self.outcome_strategy_guide.roundToResult.values():
            total += result.p2_points

        return total
