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
import sys

def axis_sort(p):
    dirs = [(p.e, E), (p.se, SE), (p.sw, SW), (-p.e, W)]
    dirs.sort(key=lambda x: x[0], reverse=True)
    return dirs

axis_word_cache = {}
# returns the power words from the given list, grouped by predominant direction
def get_axis_words(power):
    # cache result, since PathFinder is constructed many times
    words = axis_word_cache.get(power)
    if words is not None:
        return words
    words = {E: [], SE: [], SW: [], W: []}
    for pw in power.words:
        dir = axis_sort(pw.net_displacement)[0][1]
        words[dir].append(pw)
    axis_word_cache[power] = words
    return words

def next_cmd(axes, words, rots, tried):
    for pw in words[axes[0][1]]:
        if pw not in tried:
            tried.add(pw)
            return Power(pw, True)
    for axis in axes:
        dir = axis[1]
        if Move(dir) not in tried:
            tried.add(Move(dir))
            return CommandAction(Move(dir))
    for rot in rots:
        if rot not in tried:
            tried.add(rot)
            return CommandAction(rot)

    return None

class PathFinder:
    def __init__(self,board,unit_start,unit_ends,power):
        self.board=board
        self.unit_start = unit_start
        self.unit_ends = unit_ends
        self.phrases = power
        self.words = get_axis_words(power)
        self.steps = []
        self.lowest_y = 0
        self.checking_lowest = False
        self.lowest_unit = copy.deepcopy(self.unit_start)

    def complete(self):
        return self.unit_start == self.unit_ends[0] or (self.checking_lowest and self.board.current_unit.pivot.y == self.lowest_y)

    def finish_unit_basic(self):
        ba = BasicAlgorithm(self.board, self.phrases)
        unit = self.board.current_unit
        while self.board.current_unit == unit:
            ba.step()

    def check_lowest(self):
        if self.checking_lowest is False and self.board.current_unit.pivot.y > self.lowest_y:
            self.lowest_unit = copy.deepcopy(self.unit_ends[0])
            self.lowest_y = self.lowest_unit.pivot.y

    def find_path(self):
        ms = [Move(E),Move(SE),Move(SW),Move(W)]
        rotations = [Rotation(Clockwise),Rotation(Counterwise)]
        original_steps = len(self.board.steps)

        if self.unit_ends is None or len(self.unit_ends) == 0:
            self.finish_unit_basic()
        else:
            self.board.current_unit = self.unit_start
            tried = set()
            try_history = []
            been = set()
            self.board.set_path_target(self.unit_ends[0].pivot)

            # while not self.board.current_unit.rotation_matches(self.unit_end.current_rotation):
            #     self.board.step(Rotation(Clockwise))

            while not self.complete():
                been.add((self.board.current_unit.pivot,self.board.current_unit.current_rotation))
                self.check_lowest()
                d = self.unit_ends[0].pivot.delta(self.unit_start.pivot)
                axes = axis_sort(d)

                cmd = next_cmd(axis_sort(d), self.words, rotations, tried)

                if cmd is not None:
                    self.board.step(cmd)
                    if self.board.error or self.board.current_unit != self.unit_start or (self.board.current_unit.pivot,self.board.current_unit.current_rotation) in been:
                        self.board.undo_last_step()
                    else:
                        try_history.append(tried)
                        tried = set()
                else:
                    if len(try_history)>0:
                        self.board.undo_last_step()
                        tried = try_history.pop()
                    elif len(self.unit_ends)>1:
                        self.unit_ends.pop(0)
                        try_history = []
                        been = set()
                        tried = set()
                        self.board.set_path_target(self.unit_ends[0].pivot)
                    elif self.checking_lowest is False and self.lowest_unit is not None:
                        # res=""
                        # for step in self.board.steps:
                        #     res+=str(step.command())
                        # print(res)
                        # print(self.board)
                        print("PathFinder: No commands left to try...trying lowest unit", file=sys.stderr)
                        #
                        # self.finish_unit_basic()
                        # break
                        self.checking_lowest = True
                        self.unit_ends.pop(0)
                        self.unit_ends.append(copy.deepcopy(self.lowest_unit))
                        try_history = []
                        been = set()
                        tried = set()
                    else:
                        print("PathFinder: No commands left to try, even lowest unit", file=sys.stderr)
                        self.finish_unit_basic()
                        break


                # input("PathFinder: Press enter to continue")
        self.board.set_path_target(None)

        if self.board.current_unit == self.unit_start:
            # lock the piece by crashing into a neighbouring cell
            for cmd in ms + rotations:
                self.board.step(CommandAction(cmd))
                if self.board.current_unit == self.unit_start:
                    self.board.undo_last_step()
                else:
                    break
            if self.board.current_unit == self.unit_start:
                self.finish_unit_basic()
            if self.board.current_unit == self.unit_start:
                print(self.lowest_unit, file=sys.stderr)
                print(self.board, file=sys.stderr)
                raise Exception("path_finder failed to lock unit")

        # cmds=[]
        # for i in range(original_steps, len(self.board.steps)):
        #     cmds.append(self.board.steps[i])
        # return cmds
