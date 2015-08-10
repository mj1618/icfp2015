#!/usr/bin/env python
import os
import time
import sys

from actions import *
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
                print("Board complete, terminating", file=sys.stderr)
                return
            cmd = command.get(c.lower())
            if cmd is None:
                print("Hit invalid character {}, aborting".format(c), file=sys.stderr)
                break
            self.board.step(CommandAction(cmd))
            if self.animator is not None:
                self.animator.next_frame()

            print("Step {}: {} => {}".format(i, c, cmd), file=sys.stderr)
            print(self.board, file=sys.stderr)
            print("", file=sys.stderr)
            print("  Score: {}".format(self.board.score), file=sys.stderr)
        print("End of input", file=sys.stderr)
        if self.board.is_complete():
            print("Which is convenient, as we ran out of board", file=sys.stderr)
