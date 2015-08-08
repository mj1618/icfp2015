#!/usr/bin/env python
from pprint import pprint
import loader
from board import *
from unit import *
from point import *
from actions import *
from basic_algorithm import *
from replay_algorithm import *
# import pdb

def replay_test():
    prob = loader.get_qualifier_problems(6)[0]
    board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=0)
    print(len(board.units))
    alg = ReplayAlgorithm(board, "iiiiiiimimiiiiiimmimiiiimimimmimimimimmeemmimimiimmmmimmimiimimimmimmimeeemmmimimmimeeemiimiimimimiiiipimiimimmmmeemimeemimimimmmmemimmimmmiiimmmiiipiimiiippiimmmeemimiipimmimmipppimmimeemeemimiieemimmmm", animation_delay=0.1)
    alg.start()


def main():
    probs = loader.get_qualifier_problems(1)
    
    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0])
    print("loaded")

    # while not test_board.is_complete():
    # for i in range(0,8):
    #     test_board.step(Move(SE))
    # test_board.step(Move(SE))
    # test_board.step(Rotation(Clockwise))
    # pdb.set_trace()

    algo = BasicAlgorithm(test_board)
    algo.start()

    print("%d"%test_board.score)

    print(test_board)

    for step in test_board.steps:
        for action in step.actions:
            pprint(vars(action))
    #
    # for step in test_board.steps:
    #     for action in step.actions:
    #         if type(action) is CommandAction:
    #

if __name__ == "__main__":
    main()
