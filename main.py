#!/usr/bin/env python

import loader
from board import Board

def main():
    probs = loader.get_qualifier_problems(0, 1)
    
    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0])
    print(test_board)


if __name__ == "__main__":
    main()
