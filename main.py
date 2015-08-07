#!/usr/bin/env python

import loader
from board import *
from unit import *
from point import *
from actions import *

# import pdb

def main():
    probs = loader.get_qualifier_problems(1)
    
    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0])
    print("loaded")

    while not test_board.is_complete():
        test_board.step(Move(SE))
    # test_board.step(Move(SE))
    # test_board.step(Rotation(Clockwise))
    # pdb.set_trace()

    print(test_board)


if __name__ == "__main__":
    main()
