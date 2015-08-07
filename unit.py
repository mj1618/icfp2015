#!/usr/bin/env python

__import__('point.py')

class Unit:

    RIGHT = [1,0]
    LEFT = [-1,0]
    UP = [0,-1]
    DOWN = [0,1]

    def __init__(self, pts, center):
        self.center = center
        self.pts = pts
        self.mask = None
        for pt in pts:
            self.mask.append([pt.__sub__(center)])


    def move_right(self):
        for pt in self.pts:
            pt.__add__(self, Unit.RIGHT)

    def move_left(self):
        for pt in self.pts:
            pt.__add__(self, Unit.LEFT)

    def move_up(self):
        for pt in self.pts:
            pt.__add__(self, Unit.UP)

    def move_down(self):
        for pt in self.pts:
            pt.__add__(self, Unit.DOWN)
