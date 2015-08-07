#!/usr/bin/env python

import loader
from board import *
from unit import *
from point import *

# import pdb

def main():
    probs = loader.get_qualifier_problems(0, 1)
    
    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0])

    test_board.step(Move(E))

    test_board.step(Move(SE))
    # pdb.set_trace()

    print(test_board)


if __name__ == "__main__":
    main()
