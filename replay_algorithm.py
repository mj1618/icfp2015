#!/usr/bin/env python
import os
import time

from words import command

class ReplayAlgorithm:
    def __init__(self, board, input_string, animator=None):
        self.board = board
        self.input_string = input_string.lower()
        self.animator = animator

    def start(self):
        for i, c in enumerate(self.input_string):
            if self.board.is_complete():
                print("Board complete, terminating")
                return
            cmd = command.get(c)
            if cmd is None:
                print("Hit invalid character {}, aborting".format(c))
                break
            self.board.step(cmd)
            if self.animator is not None:
                self.animator.next_frame()

            print("Step {}: {} => {}".format(i, c, cmd))
            print(self.board)
            print("")
            print("  Score: {}".format(self.board.score))
        print("End of input")
        if self.board.is_complete():
            print("Which is convenient, as we ran out of board")
