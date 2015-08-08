#!/usr/bin/env python
import os
import time

from words import command

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
            cmd = command.get(c)
            if cmd is None:
                print("Hit invalid character {}, aborting".format(c))
                break
            self.board.step(cmd)
            if self.animation_delay:
                os.system('cls' if os.name == 'nt' else 'clear')

            print("Step {}: {} => {}".format(i, c, cmd))
            print(self.board)
            print("")
            if self.animation_delay:
                time.sleep(self.animation_delay)
        print("It's over!")
