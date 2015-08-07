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

    def is_filled(self,x,y):
        for pt in self.pts:
            if pt.x==x and pt.y ==y:
                return True
        return False
