#!/usr/bin/env python
import os
import time

from words import command

def char_stream(stream):
    while True:
        c = stream.read(1)
        if len(c) == 0:
            return #eof
        c = c.lower()
        if not (c == '\r' or c == '\n' or c == '\t'):
            yield c


class ReplayAlgorithm:
    def __init__(self, board, input, animator=None):
        """ input must be an iterable sequence of characters """
        self.board = board
        self.input = input
        self.animator = animator

    def start(self):
        for i, c in enumerate(self.input):
            if self.board.is_complete():
                print("Board complete, terminating")
                return
            cmd = command.get(c.lower())
            if cmd is None:
                print("Hit invalid character {}, aborting".format(c))
                break
            self.board.step(CommandAction(cmd))
            if self.animator is not None:
                self.animator.next_frame()

            print("Step {}: {} => {}".format(i, c, cmd))
            print(self.board)
            print("")
            print("  Score: {}".format(self.board.score))
        print("End of input")
        if self.board.is_complete():
            print("Which is convenient, as we ran out of board")
