#!/usr/bin/env python
import random
from words import *
from render import *
from point import *
import copy
from actions import *
from random import randint
from unit import *
from basic_algorithm import *
class PathFinder:
    def __init__(self,board,unit_start,unit_end):
        self.board=board
        self.unit_start = unit_start
        self.unit_end = unit_end
        self.steps = []



    def complete(self):
        return self.unit_start == self.unit_end

    def finish_unit_basic(self):
        ba = BasicAlgorithm(self.board)
        unit = self.board.current_unit
        while self.board.current_unit == unit:
            ba.step()

    def find_path(self):
        ms = [Move(E),Move(SE),Move(SW),Move(W)]
        original_steps = len(self.board.steps)

        if self.unit_end is None:
            self.finish_unit_basic()
        else:
            self.board.current_unit = self.unit_start
            tried = []
            try_history = []
            been = []

            while not self.board.current_unit.rotation_matches(self.unit_end.current_rotation):
                self.board.step(Rotation(Clockwise))

            while not self.complete():
                been.append(self.board.current_unit.pivot)
                sources = self.board.sources_remaining
                d = self.unit_end.pivot.delta(self.unit_start.pivot)
                cmd = None

                for w in KnownWords.words:
                    if w not in tried:
                        cmd = Power(w,KnownWords.decode(w))
                        tried.append(w)
                        break
                if cmd is None:
                    if d.e > 0 and Move(E) not in tried :
                        cmd = Move(E)
                    elif d.se > 0 and Move(SE) not in tried:
                        cmd = Move(SE)
                    elif d.sw > 0 and Move(SW) not in tried:
                        cmd = Move(SW)
                    elif d.e < 0 and Move(W) not in tried:
                        cmd = Move(W)

                if cmd is None:
                    for m in ms:
                        if m not in tried:
                            cmd = m
                            break

                if cmd is not None:
                    if type(cmd) is Power:
                        self.board.power_step(cmd)
                    else:
                        self.board.step(cmd)
                    if self.board.error or self.board.current_unit != self.unit_start or self.board.current_unit.pivot in been:
                        self.board.undo_last_step()
                        tried.append(cmd)
                    else:
                        try_history.append(tried)
                        tried = []
                else:
                    if len(try_history)>0:
                        self.board.undo_last_step()
                        tried = try_history.pop()
                    else:
                        res=""
                        for step in self.board.steps:
                            res+=str(step.command())
                        print(res)
                        print(self.board)
                        print("PathFinder: No commands left to try...")

                        self.finish_unit_basic()
                        break
                # input("PathFinder: Press enter to continue")


        if self.board.current_unit == self.unit_start:
            # lock the piece by crashing into a neighbouring cell
            for cmd in ms:

                if type(cmd) is Power:
                    self.board.power_step(cmd)
                else:
                    self.board.step(cmd)

                if self.board.current_unit == self.unit_start:
                    self.board.undo_last_step()
                else:
                    break
            if self.board.current_unit == self.unit_start:
                raise Exception("path_finder failed to lock unit")

        cmds=[]
        for i in range(original_steps, len(self.board.steps)):
            cmds.append(self.board.steps[i].command())
        return cmds