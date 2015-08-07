#!/usr/bin/env python
from point import *

class Command:
    pass

class Move(Command):
    def __init__(self, dir):
        self.dir = dir

class Rotation(Command):
    def __init__(self, dir):
        self.dir = dir

class Unit:
    def __init__(self, pts, pivot):
        self.pivot = pivot
        self.mask = None
        self.moves=[]
        self.mask = [pt - pivot for pt in pts]


    def move(self, dir):
        self.pivot += dir
        self.moves.append(Move(dir))

    def rotate(self, dir):
        self.mask = [pt.rotate(dir) for pt in self.mask]
        self.moves.append(Rotation(dir))

    def undo_last_command(self):
        last_command = self.moves.pop()
        if type(last_command) is Move:
            self.pivot -= last_command.dir
        else:
            self.mask = [pt.rotate(not last_command.dir) for pt in self.mask]

    def get_pts(self):
        pts = []
        for m in self.mask:
            pts.append( m + self.pivot )
        return pts

    def is_filled(self,x,y):
        for pt in self.get_pts():
            if pt.x==x and pt.y == y:
                return True
        return False

    def row(self,y):
        return [ pt for pt in self.get_pts() if pt.y==y]


    def top_left_pt(self):
        return min(self.row(0), key=lambda pt: pt.x)
    def top_right_pt(self):
        return max(self.row(0), key=lambda pt: pt.x)
