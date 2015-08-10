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
from basic_algorithm import *
import sys
class PfpAlgorithm:
    def __init__(self,board,power):
        self.board=board
        self.power = power
        self.last_pos = [0,0]
        self.i = 0
        self.cmds = []

    def start(self):
        while not self.board.is_complete():
            self.step()

    def step(self):
        pa = PlacerAlgorithm(self.board)
        # pa.board.install_step_hook(None)
        try:
            units = pa.step()
        except:
            units = None

        pf = PathFinder(self.board, self.board.current_unit, units, self.power)
        pf.find_path()
        # for cmd in pf.find_path():
        #    if cmd is not None:
        #        self.cmds.append(cmd)

        # input("PFP: Press enter to continue")
