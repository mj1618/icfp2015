#!/usr/bin/env python
import random
from words import *
from render import *
from point import *
import copy
from actions import *
from random import randint
from unit import *
class PathFinder:
    def __init__(self,board,unit_start,unit_end):
        self.board=copy.deepcopy(board)
        self.unit_start = unit_start
        self.unit_end = unit_end
        self.actions = []

    def complete(self):
        return self.unit_start == self.unit_end

    def find_path(self):
        self.board.current_unit = self.unit_start

        last_tried = None

        ms = [Move(E),Move(SE),Move(SW),Move(W)]
        while not self.complete():
            sources = self.board.sources_remaining
            d = self.unit_end.pivot.delta(self.unit_start.pivot)
            cmd = None
            if d.e > 0 and last_tried is None :
                cmd = Move(E)
            elif d.e < 0 and ms.index(last_tried)<1:
                cmd = Move(W)
            elif d.se > 0 and ms.index(last_tried)<2:
                cmd = Move(SE)
            elif d.sw > 0 and ms.index(last_tried)<3:
                cmd = Move(SW)

            if cmd is None:
                if last_tried is None :
                    cmd = Move(E)
                elif ms.index(last_tried)<1:
                    cmd = Move(W)
                elif ms.index(last_tried)<2:
                    cmd = Move(SE)
                elif ms.index(last_tried)<3:
                    cmd = Move(SW)


            if cmd is not None:
                self.board.step(cmd)
                if self.board.error or sources != self.board.sources_remaining:
                    last_tried = self.board.undo_last_step().command()
                else:
                    last_tried = None
            else:
                last_tried = self.board.undo_last_step().command()

        res=""
        for step in self.board.steps:
            res+=str(step.command())

        print(res)