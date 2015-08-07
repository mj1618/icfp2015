#!/usr/bin/env python
from render import *
from point import *
import copy
from actions import *
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

    def __init__(self, width, height, grid, units, seed):
        self.grid = grid
        self.width = width
        self.height = height
        self.units = units
        self.seed = seed
        self.steps = []
        self.current_actions=[]
        self.old_seed = None
        self.current_unit = None
        self.current_lines_cleared = 0
        self.old_lines_cleared = 0
        self.score = 0

        self.step()

    def step(self,cmd=None):
        if self.current_unit is None:
            self.next_unit_action()
        else:
            self.command(cmd)
        self.steps.append(Step(self.current_actions))
        self.current_actions=[]

    def next_unit_action(self):
        a = NewUnitAction(self.current_unit)
        a.do(self)
        self.current_actions.append(a)

    def rng_action(self):
        a = RngAction(self.current_unit)
        r = a.do(self)
        self.current_actions.append(a)
        return r

    def command(self, cmd):
        self.current_unit.command(cmd)
        lock = self.is_lock()
        if lock:
            self.current_unit.undo(cmd)
            self.calculate_score()
            self.next_unit_action()
        self.current_actions.append(CommandAction(cmd,lock))

    def is_lock(self):
        for pt in self.current_unit.get_pts():
            if pt.x>self.width or pt.y>self.height or pt.x<0 or pt.y<0 or self.grid[pt.y][pt.x]==1:
                return True
        return False

    def calculate_score(self):
        points = len(self.current_unit.mask) + 100*(1+self.current_lines_cleared)/2
        if self.old_lines_cleared > 1:
            line_bonus = (self.old_lines_cleared-1)*points/10
        else:
            line_bonus=0
        move_score = points+line_bonus
        return move_score

    def __str__(self):
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


