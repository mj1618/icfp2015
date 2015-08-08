#!/usr/bin/env python
import os
import time

from words import chars_reverse

class ReplayAlgorithm:
    def __init__(self, board, input_string, animation_delay=None):
        self.board = board
        self.input_string = input_string.lower()
        self.animation_delay = animation_delay

    def start(self):
        for i, c in enumerate(self.input_string):
            if self.board.is_complete():
                print("Board complete, terminating")
                return
            if c not in chars_reverse:
                print("Hit invalid character {}, aborting".format(c))
                return
            self.board.step(chars_reverse[c])
            if self.animation_delay:
                os.system('cls' if os.name == 'nt' else 'clear')

            print("Step {}: {} => {}".format(i, c, chars_reverse[c]))
            print(self.board)
            print("")
            if self.animation_delay:
                time.sleep(self.animation_delay)
        print("It's over!")
