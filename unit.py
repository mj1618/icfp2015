#!/usr/bin/env python
import copy
from point import *

class Unit:
    def __init__(self, pts, pivot):
        self.pivot = pivot
        self.pts = pts
        self.previous = None
        self.mask = None
        self.moves=[]
        for pt in pts:
            self.mask.append([pt.__sub__(pivot)])

    def pre_move(self):
        self.previous = copy.deepcopy(self)

    def move_w(self):
        self.pre_move()
        for pt in self.pts:
            pt += W

    def move_e(self):
        self.pre_move()
        for pt in self.pts:
            pt += E
    def move_sw(self):
        self.pre_move()
        for pt in self.pts:
            pt += SW

    def move_se(self):
        self.pre_move()
        for pt in self.pts:
            pt += SE
    def move_nw(self):
        self.pre_move()
        for pt in self.pts:
            pt += NW

    def move_ne(self):
        self.pre_move()
        for pt in self.pts:
            pt += NE

    def move(self,cmd):
        if cmd=='E':
            self.move_e()
        elif cmd=='W':
            self.move_w()
        if cmd=='SE':
            self.move_se()
        elif cmd=='SW':
            self.move_sw()
        self.moves.append(cmd)

    def move_opposite(self,cmd):
        if cmd=='E':
            self.move_w()
        elif cmd=='W':
            self.move_e()
        if cmd=='SE':
            self.move_nw()
        elif cmd=='SW':
            self.move_ne()
        self.moves.append(cmd)

    def is_filled(self,x,y):
        for pt in self.pts:
            if pt.x==x and pt.y ==y:
                return True
        return False
