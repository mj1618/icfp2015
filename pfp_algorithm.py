#!/usr/bin/env python
import random
from words import *
from render import *
from point import *
import copy
from actions import *
from random import randint
from unit import *
from placer_algorithm import *
from path_finder import PathFinder

class PfpAlgorithm:
    def __init__(self,board,step_hook=None):
        self.board=board
        self.last_pos = [0,0]
        self.i = 0
        if step_hook is not None:
            board.install_step_hook(step_hook)


    def start(self):
        while not self.board.is_complete():
            self.step()

    def step(self):
        pa = PlacerAlgorithm(self.board)
        pa.board.install_step_hook(None)
        unit = pa.step()
        pf = PathFinder(self.board, self.board.current_unit, unit)
        for cmd in pf.find_path():
           if cmd is not None:
               self.board.step(cmd)
        self.board.step(Move(SE))
        # input("PFP: Press enter to continue")
