#!/usr/bin/env python
import copy
from point import *

class Unit:
    def __init__(self, pts, center):
        self.center = center
        self.pts = pts
        self.previous = None
        self.mask = None
        self.moves=[]
        for pt in pts:
            self.mask.append([pt.__sub__(center)])

    def pre_move(self):
        self.previous = copy.deepcopy(self)

    def move_w(self):
        self.pre_move()
        for pt in self.pts:
            pt += Pt.E

    def move_e(self):
        self.pre_move()
        for pt in self.pts:
            pt += Pt.W

    def move(self,cmd):
        if cmd==E:
            self.move_e()
        elif cmd==W:
            self.move_w()
        self.moves.append(cmd)
