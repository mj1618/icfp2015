#!/usr/bin/env python
import copy

from point import *
from render import *

UNIT_EMPTY = u" "
UNIT_UNIT = u"U"
UNIT_PIVOT = u"¨"
UNIT_UNIT_PIVOT = u"Ü"

class Command:
    # the keys specify the set of possible commands. instances are initialised lazily
    instances = {W: None, E: None, SW: None, SE: None, Clockwise: None, Counterwise: None}
    def __deepcopy__(self,dict):
        return self

class Move(Command):
    def __new__(cls, dir):
        if Command.instances[dir] is None:
            Command.instances[dir] = super(Move, cls).__new__(cls)
        return Command.instances[dir]
    def __init__(self, dir):
        self.dir = dir
    def __repr__(self):
        return "Move" + str(self.dir)

class Rotation(Command):
    instances = {Clockwise: None, Counterwise: None}
    def __new__(cls, rot):
        if Command.instances[rot] is None:
            Command.instances[rot] = super(Rotation, cls).__new__(cls)
        return Command.instances[rot]
    def __init__(self, rot):
        self.rot = rot
    def __repr__(self):
        return "Rotation(%swise)" % ("Clock" if self.rot is Clockwise else "Counter")


def bounds(pts):
    # left right top bottom
    l, r, t, b = pts[0].x, pts[0].x, pts[0].y, pts[0].y
    for p in pts[1:]:
        if p.x < l: l = p.x;
        elif p.x > r: r = p.x;
        if p.y < t: t = p.y;
        elif p.y > b: b = p.y;
    return l, r, t, b

class Unit:
    def __init__(self, pts, pivot, board_width,center=True):
        if center:
            l, r, t, b = bounds(pts)
            col0 = (board_width - (r - l + 1)) // 2
            offset = Pt(col0 - l, -t)
            self.pivot = pivot + offset
            self.mask = [(pt + offset).delta(self.pivot) for pt in pts]
            self.old_states = []
            self.current_rotation=NE
        else:
            self.pivot = pivot
            self.mask = [(pt).delta(self.pivot) for pt in pts]
            self.old_states = []
            self.current_rotation=NE


    def command(self,cmd):
        self.old_states.append([self.pivot,self.current_rotation])
        if isinstance(cmd, Move):
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
            self.rotate(Counterwise)
        else:
            self.rotate(Clockwise)
        self.old_states.pop()

    def is_error(self):
        for state in self.old_states:
            if self.pivot == state[0] and self.rotation_matches(state[1]):
                # print("Error state")
                return True
        return False

    def rotation_matches(self,rotation):
        if self.current_rotation == rotation:
            return True
        n = shortest_rotation(self.current_rotation, rotation)
        mask2 = [pt.rotaten(n) for pt in self.mask]
        for m in self.mask:
            if m not in mask2:
                return False
        return True

    def get_pts(self):
        return [self.pivot.move(m) for m in self.mask]

    def is_filled(self,y,x):
        for pt in self.get_pts():
            if pt.x==x and pt.y == y:
                return True
        return False

    def __eq__(self, other):
        if other is None:
            return False
        pts = self.get_pts()
        for pt in other.get_pts():
            if pt not in pts:
                return False

        return True

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

