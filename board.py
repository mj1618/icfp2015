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

BOARD_FILL = u"#"
BOARD_UNIT = u"U"
BOARD_PIVOT = u"¨"
BOARD_UNIT_PIVOT = u"Ü"
BOARD_EMPTY = u" "


class Board:

    solutions = None

    def __init__(self, width, height, grid, units, seed):
        assert height == len(grid)
        for row in grid:
            assert len(row) == width

        self.width = width
        self.height = height
        self.grid = grid
        self.units = units
        self.old_seed = 0
        self.seed = seed
        self.steps = []
        self.current_actions=[]
        self.current_unit = None
        self.current_lines_cleared = 0
        self.old_lines_cleared = 0
        self.score = 0
        self.error = False
        self.is_full = False

        self.step()

    def step(self,cmd=None):
        if self.current_unit is None:
            self.next_unit_action()
        else:
            self.command(cmd)
        current_step = Step(self.current_actions)
        self.steps.append(current_step)
        self.current_actions=[]
        if self.is_complete():
            self.record_solution()
        return current_step
    def action_step(self,action):
        if self.current_unit is None:
            self.next_unit_action()
        else:
            action.do(self)
            if not action.completed:
                return
            self.current_actions.append(action)
        current_step = Step(self.current_actions)
        self.steps.append(current_step)
        self.current_actions=[]
        if self.is_complete():
            self.record_solution()
        return current_step

    def undo_last_step(self):
        self.error=False
        self.is_full = False
        for action in self.steps.pop().actions:
            action.undo(self)

    def is_complete(self):
        return ( len(self.units)==0 and self.current_unit is None ) or self.is_full

    def record_solution(self):
        solution = []
        for step in self.steps:
            for action in step.actions:
                if type(action) is CommandAction:
                    solution.append(action.cmd)

    def next_unit_action(self):
        a = NewUnitAction()
        a.do(self)
        self.current_actions.append(a)

    def rng_action(self):
        a = RngAction(self.current_unit)
        r = a.do(self)
        self.current_actions.append(a)
        return r

    """ returns True if successful, False if an error move occurred. State is left in Error """
    def command(self, cmd):
        self.current_unit.command(cmd)
        lock = False
        self.error = self.current_unit.is_error()
        if not self.error:
            lock = self.is_lock()
            if lock:
                self.current_unit.undo(cmd)
                score_action = ScoreAction(self.calculate_score())
                score_action.do(self)
                self.current_actions.append(score_action)
                self.next_unit_action()
        self.current_actions.append(CommandAction(cmd,lock))

    def is_lock(self):
        if self.current_unit is not None:
            for pt in self.current_unit.get_pts():
                if pt.x>=self.width or pt.y>=self.height or pt.x<0 or pt.y<0 or self.grid[pt.y][pt.x]==1:
                    return True
        else: return True
        return False

    def calculate_score(self):
        points = len(self.current_unit.mask) + 100*(1+self.current_lines_cleared)*self.current_lines_cleared//2
        if self.old_lines_cleared > 1:
            line_bonus = (self.old_lines_cleared-1)*points//10
        else:
            line_bonus=0
        move_score = points+line_bonus
        return move_score

    def query_cell(self, y, x):
        assert (y >= 0) and (y < self.height)
        assert (x >= 0) and (x < self.width)
        if self.grid[y][x]:
            return BOARD_FILL
        elif self.current_unit is not None:
            fill = self.current_unit.is_filled(y, x)
            pivot = self.current_unit.pivot == Pt(x, y)
            if fill and pivot:
                return BOARD_UNIT_PIVOT
            elif fill:
                return BOARD_UNIT
            elif pivot:
                return BOARD_PIVOT
        return BOARD_EMPTY


    def __str__(self):
        return render_grid(self.width, self.height, self.query_cell)


    def get_hole_count(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    continue
                l = 1 if (x == 0) else self.grid[y][x-1]
                r = 1 if (x == self.width-1) else self.grid[y][x+1]
                tl = 1 if (y == 0) else (1 if ((x==0) and (y-1)%2) else self.grid[y-1][x-((y-1)%2)])
                tr = 1 if (y == 0) else  (1 if ((x==self.width-1) and (y%2)) else self.grid[y-1][x+(y%2)])
                bl = 1 if (y == self.height-1) else (1 if ((x==0) and (y-1)%2) else self.grid[y+1][x-((y+1)%2)])
                br = 1 if (y == self.height-1) else (1 if ((x==self.width-1) and y%2) else self.grid[y+1][x+(y%2)])
                
                hole = False
                hole |= (l and r) or (tl and br) or (bl and tr)
                hole |= (l and tr and br) or (r and tl and bl)
                
                count += hole
                #if hole:
                #    print("{},{},{},{},{},{} = {}".format(l, tl, tr, r, br, bl, hole))
                #    print('{},{}'.format(x,y))
        return count
 
