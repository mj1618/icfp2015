#!/usr/bin/env python
__import__('render.py')
__import__('point')

RNG_MOD = 2**32
RNG_MULT = 1103515245
RNG_INC = 12345
RNG_MASK = 0x7fff0000
RNG_TRUNC = 16

class Board:

    solutions = None

    def __init__(self, width, height, fills, units, seed):
        self.board = [[0 for x in range(width)] for x in range(height)]
        self.width = width
        self.height = height
        self.units = units
        self.seed = seed
        self.old_seed = None

        for fill in fills:
            self.board[fill.x][fill.y] = 1

        self.next_unit()

    def next_unit(self):
        self.current_unit = self.units[self.rng(self)]
        while self.current_unit.top_left_pt() <  (self.width - self.current_unit.top_right_pt()):
            self.current_unit.move_right()

    def rng(self):
        self.old_seed = self.seed
        self.seed = (RNG_MULT*self.seed+RNG_INC % RNG_MOD)
        return (self.old_seed & RNG_MASK) >> RNG_TRUNC


    def move(self, cmd):
