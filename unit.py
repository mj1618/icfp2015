#!/usr/bin/env python
import copy

from point import *
from render import *

UNIT_EMPTY = u" "
UNIT_UNIT = u"U"
UNIT_PIVOT = u"¨"
UNIT_UNIT_PIVOT = u"Ü"

class Command:
    pass

class Move(Command):
    def __init__(self, dir):
        self.dir = dir
    def __repr__(self):
        return str(self.dir)

class Rotation(Command):
    def __init__(self, rot):
        self.rot = rot

class Unit:
    def __init__(self, pts, pivot):
        self.pivot = pivot
        self.mask = [pt.delta(pivot) for pt in pts]
        self.old_states = []
        self.current_rotation=NE


    def command(self,cmd):
        self.old_states.append([copy.deepcopy(self.pivot),self.current_rotation])
        if type(cmd) is Move:
            self.move(cmd.dir)
        else:
            self.rotate(cmd.rot)

    def move(self, dir):
        self.pivot = self.pivot.move(dir)

    def rotate(self, rotate):
        self.mask = [rotate(pt) for pt in self.mask]
        self.current_rotation = rotate(self.current_rotation)


    def undo(self,last_command):
        if type(last_command) is Move:
            self.pivot = self.pivot.move(-last_command.dir)
        elif last_command.rot is Clockwise:
            self.mask = [Counterwise(pt) for pt in self.mask]
        else:
            self.mask = [Clockwise(pt) for pt in self.mask]
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
        return [self.pivot.move(m) for m in self.mask]

    def is_filled(self,y,x):
        for pt in self.get_pts():
            if pt.x==x and pt.y == y:
                return True
        return False

    def row(self,y):
        return [ pt for pt in self.get_pts() if (pt.y == y)]

    def top_left_pt(self):
        return min(self.row(0), key=lambda pt: pt.x)
    def top_right_pt(self):
        return max(self.row(0), key=lambda pt: pt.x)

    def __str__(self):
        bbox = [self.pivot.x, self.pivot.y, self.pivot.x, self.pivot.y]
        points = []
        #print("origin: {}".format(self.pivot))
        #print("points in:")
        for m in self.mask:
            p = self.pivot.move(m)
            points.append(p)
            #print("{} => {}".format(m,p))

            bbox[0] = min(bbox[0], p.x)
            bbox[1] = min(bbox[1], p.y)
            bbox[2] = max(bbox[2], p.x)
            bbox[3] = max(bbox[3], p.y)
        offset = Pt(bbox[0], bbox[1])
        dims = Pt(bbox[2]+1, bbox[3]+1) - offset

        #print("offset, dims")
        #print((offset, dims))
        
        #print("{} {}".format("ODD" if self.pivot.y%2 else "EVEN", "ODD" if offset.y%2 else "EVEN"))

        if ((self.pivot.y-offset.y+1) % 2) and (dims.y > 1) and not ((self.pivot.y+1%2) and (offset.y+1%2)):
            offset.y -= 1
            dims.y += 1
        elif (self.pivot.y+1%2) and (offset.y%2):
            offset.y -= 1
            dims.y += 1
        grid = [[0 for x in range(dims.x)] for y in range(dims.y)]

        #print("points out:")
        for p in points:
            p_abs = p-offset
            #print("{} => {}".format(p, p_abs))
            grid[p_abs.y][p_abs.x] = 1
        grid[self.pivot.y-offset.y][self.pivot.x-offset.x] |= 2


        def query_func(y, x):
            choices = (UNIT_EMPTY, UNIT_UNIT, UNIT_PIVOT, UNIT_UNIT_PIVOT)
            return choices[grid[y][x]]

        return render_grid(dims.x, dims.y, query_func)

