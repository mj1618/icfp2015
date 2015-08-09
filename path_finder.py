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
        self.unit_start = copy.deepcopy(unit_start)
        self.unit_end = copy.deepcopy(unit_end)
        self.actions = []

    def complete(self):
        return self.unit_start == self.unit_end

    def find_path(self):
        self.board.current_unit = self.unit_start
        self.board.steps = []
        last_tried = None
        been = []

        while not self.board.current_unit.rotation_matches(self.unit_end.current_rotation):
            self.board.step(Rotation(Clockwise))

        ms = [Move(E),Move(SE),Move(SW),Move(W)]
        while not self.complete():
            been.append(self.board.current_unit.pivot)
            sources = self.board.sources_remaining
            d = self.unit_end.pivot.delta(self.unit_start.pivot)
            cmd = None
            if d.e > 0 and last_tried is None :
                cmd = Move(E)
            elif d.se > 0 and (last_tried is None or ms.index(last_tried)<1):
                cmd = Move(SE)
            elif d.sw > 0 and (last_tried is None or ms.index(last_tried)<2):
                cmd = Move(SW)
            elif d.e < 0 and (last_tried is None or ms.index(last_tried)<3):
                cmd = Move(W)

            if cmd is None:
                if last_tried is None :
                    cmd = Move(E)
                elif last_tried is None or ms.index(last_tried)<1:
                    cmd = Move(SE)
                elif last_tried is None or ms.index(last_tried)<2:
                    cmd = Move(SW)
                elif last_tried is None or ms.index(last_tried)<3:
                    cmd = Move(W)


            if cmd is not None:
                self.board.step(cmd)
                if self.board.error or sources != self.board.sources_remaining or self.board.current_unit.pivot in been:
                    last_tried = self.board.undo_last_step().command()
                else:
                    last_tried = None
            else:
                if len(self.board.steps)>0:
                    last_tried = self.board.undo_last_step().command()
                else:
                    res=""
                    for step in self.board.steps:
                        res+=str(step.command())
                    print(res)
                    print(self.board)
                    input("PathFinder: No commands left to try...")
            # input("PathFinder: Press enter to continue")

        res=""
        cmds = []
        for step in self.board.steps:
            res+=str(step.command())
            cmds.append(step.command())

        source = self.board.sources_remaining
        for cmd in ms:
            self.board.step(cmd)
            if source == self.board.sources_remaining:
                self.board.undo_last_step()
            else:
                cmds.append(cmd)
                break

        print(res)
        return cmds
