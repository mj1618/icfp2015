#!/usr/bin/env python
from render import *
from point import *
RNG_MOD = 2**32
RNG_MULT = 1103515245
RNG_INC = 12345
RNG_MASK = 0x7fff0000
RNG_TRUNC = 16

RENDER_TOP_LEFT = u"╔═══"
RENDER_TOP_MID = u"╦═══"
RENDER_TOP_RIGHT = u"╗\n"
RENDER_BODY_LEFTMID = u"║ {} "
RENDER_BODY_RIGHT = u"║\n"
RENDER_BODY_OFFSET = u"  "
RENDER_ODDJOIN_LEFT = u"╚═╦═"
RENDER_ODDJOIN_MID = u"╩═╦═"
RENDER_ODDJOIN_RIGHT = u"╩═╗\n"
RENDER_EVENJOIN_LEFT = u"╔═╩═"
RENDER_EVENJOIN_MID = u"╦═╩═"
RENDER_EVENJOIN_RIGHT = u"╦═╝\n"
RENDER_BOTTOM_LEFT = u"╚═══"
RENDER_BOTTOM_MID = u"╩═══"
RENDER_BOTTOM_RIGHT = u"╝\n"

RENDER_GRID_FILL = u"#"
RENDER_GRID_EMPTY = u" "


class Board:

    solutions = None

    def __init__(self, width, height, fills, units, seed):
        self.grid = [[0 for x in range(width)] for x in range(height)]
        self.width = width
        self.height = height
        self.units = units
        self.seed = seed
        self.old_seed = None
        self.current_unit = None

        for fill in fills:
            self.grid[fill.x][fill.y] = 1

        self.next_unit()

    def next_unit(self):
        self.current_unit = self.units[self.rng(self)]
        while self.current_unit.top_left_pt() <  (self.width - self.current_unit.top_right_pt()):
            self.current_unit.move_right()

    def rng(self):
        self.old_seed = self.seed
        self.seed = (RNG_MULT*self.seed+RNG_INC % RNG_MOD)
        return (self.old_seed & RNG_MASK) >> RNG_TRUNC

    def is_incorrect(self):
        for pt in self.current_unit.pts:
            if pt.x>self.width or pt.y>self.height or pt.x<0 or pt.y<0 or self.grid[pt.x][pt.y]==1:
                return True
        return False

    def move(self, cmd):
        self.current_unit.move(cmd)
        if self.is_incorrect():
            self.current_unit.move_opposite(cmd)
            for pt in self.current_unit.pts:
                self.grid[pt.x][pt.y] = 1
            self.next_unit()


    def render_grid(self):
        assert len(self.grid) > 0
        assert len(self.grid[0]) > 0

        height = len(self.grid)
        width = len(self.grid[0])
        for row in self.grid:
            assert len(row) == width

        output = RENDER_TOP_LEFT + RENDER_TOP_MID*(width-1) + RENDER_TOP_RIGHT

        row_index = 0
        while row_index < height:

            if row_index % 2:
                output += RENDER_BODY_OFFSET
            for i in range(width):
                output += RENDER_BODY_LEFTMID.format(RENDER_GRID_FILL if self.grid[row_index][i] or self.current_unit.is_filled(row_index,i) else RENDER_GRID_EMPTY)
            output += RENDER_BODY_RIGHT

            if row_index != height-1:
                if row_index % 2:
                    output += RENDER_EVENJOIN_LEFT + RENDER_EVENJOIN_MID*(width-1) + RENDER_EVENJOIN_RIGHT
                else:
                    output += RENDER_ODDJOIN_LEFT + RENDER_ODDJOIN_MID*(width-1) + RENDER_ODDJOIN_RIGHT

            row_index += 1

        if (height-1) % 2:
            output += RENDER_BODY_OFFSET
        output += RENDER_BOTTOM_LEFT + RENDER_BOTTOM_MID*(width-1) + RENDER_BOTTOM_RIGHT

        return output


