#!/usr/bin/env python
from point import *
import copy
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
        self.mask = [pt - pivot for pt in pts]
        self.old_states = []
        self.current_rotation=NE

    def command(self,cmd):
        self.old_states.append([copy.deepcopy(self.pivot),self.current_rotation])
        if type(cmd) is Move:
            self.move(cmd.dir)
        else:
            self.rotate(cmd.dir)

    def move(self, dir):
        self.pivot = self.pivot.move(dir)

    def rotate(self, dir):
        self.mask = [pt.rotate(dir) for pt in self.mask]


    def undo(self,last_command):
        if type(last_command) is Move:
            self.pivot -= last_command.dir
        else:
            self.mask = [pt.rotate(not last_command.dir) for pt in self.mask]
        self.old_states.pop()

    def is_error(self):
        for state in self.old_states:
            if self.pivot == state[0] and self.rotation_matches(state[1]):
                print("Error state")
                return True
        return False

    def rotation_matches(self,rotation):
        unit = copy.deepcopy(self)
        while unit.current_rotation != rotation:
            unit.rotate(Clockwise)
        for m in self.mask:
            if m not in unit.mask:
                return False
        return True

    def get_pts(self):
        pts = []
        for m in self.mask:
            pts.append( m + self.pivot )
        return pts

    def is_filled(self,y,x):
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
