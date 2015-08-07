#!/usr/bin/env python
from point import *

class Command:
    pass

class Move(Command):
    def __init__(self, dir):
        self.dir = dir

class Rotation(Command):
    def __init__(self, clockwise):
        self.clockwise = clockwise

class Unit:
    def __init__(self, pts, pivot):
        self.pivot = pivot
        self.pts = pts
        self.mask = None
        self.moves=[]
        for pt in pts:
            self.mask.append([pt.__sub__(pivot)])

    def move(self,dir):
        self.pts = [p + dir for p in self.pts]
        self.moves.append(Move(dir))

    def undo_last_move(self):
        last_move = self.moves.pop()
        self.pts = [p - move.dir for p in self.pts]

    def is_filled(self,x,y):
        for pt in self.pts:
            if pt.x==x and pt.y ==y:
                return True
        return False
