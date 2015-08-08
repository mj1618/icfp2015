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

    solutions = []

    def __init__(self, width, height, grid, units, seed, step_hook=None):
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
        self.word_count = {} #map from power word -> number of times used
        self.score = 0
        self.error = False
        self.is_full = False
        self.step_hook = step_hook

        self.step()

    def install_step_hook(self, step_hook):
        self.step_hook = step_hook

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
        if self.step_hook is not None:
            self.step_hook(self, False, cmd)
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
        step = self.steps.pop()
        for action in self.steps.pop().actions:
            action.undo(self)
            if self.step_hook is not None and type(action) is CommandAction:
                self.step_hook(self, True, action.cmd)

    def is_complete(self):
        return ( len(self.units)==0 and self.current_unit is None ) or self.is_full

    def record_solution(self):
        solution = []
        for step in self.steps:
            for action in step.actions:
                if type(action) is CommandAction:
                    solution.append(action.cmd)
                elif type(action) is Power:
                    solution.append(action)
        self.solutions.append(solution)

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


    def is_cell_valid(self, point):
        return not ((point.x < 0) or (point.x >= self.width) or (point.y < 0) or (point.y >= self.height))

    def is_lock(self):
        if self.current_unit is not None:
            for pt in self.current_unit.get_pts():
                if not self.is_cell_valid(pt) or self.grid[pt.y][pt.x]==1:
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
        assert self.is_cell_valid(Pt(x,y))
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


    def get_base_heightmap(self):
        heightmap = [0 for i in range(self.width)]
        
        column = 0
        row = 0

        def _follow(p):
            ne = p.move(NE)
            
            if self.is_cell_valid(ne) and self.grid[ne.y][ne.x] == 1:
                result = _follow(ne)
                if result != -1:
                    heightmap[ne.x] = max(heightmap[ne.x], ne.y)
                return result
            
            if p.x ==self.width-1:
                return p.x

            e = p.move(E)
            if (e.y == self.height) or (self.is_cell_valid(e) and self.grid[e.y][e.x]) == 1:
                result = _follow(e)
                if result != -1:
                    heightmap[e.x] = max(heightmap[e.x], e.y)
                return result
                    
            se = p.move(SE)
            if self.is_cell_valid(se) and self.grid[se.y][se.x] == 1:
                result = _follow(se)
                if result != -1:
                    heightmap[se.x] = max(heightmap[se.x], se.y)
                return result

            # skip backtracking for now
            # for now, return how far we got.
            return p.x
            

        while (column < self.width):
            for row in range(self.height):
                if self.grid[row][column] == 1:
                    result = _follow(Pt(column, row))
                    if result != -1:
                        heightmap[column] = max(heightmap[column], row)
                        column = result
                        break
                elif row == self.height-1:
                    result = _follow(Pt(column, row+1))
                    if result != -1:
                        heightmap[column] = max(heightmap[column], row+1)
                        column = result
                        break
            column += 1

        return heightmap



    def is_hole(self, point, include_unit=False):
        assert self.is_cell_valid(point)

        unit_points = self.current_unit.get_pts()

        def _fetch(y, x):
            if include_unit and (Pt(y, x) in unit_points):
                return 1
            return self.grid[y][x]

        if _fetch(point.y, point.x) == 1:
            return 0

        x, y = point.x, point.y
        l = 1 if (x == 0) else _fetch(y, x-1)
        r = 1 if (x == self.width-1) else _fetch(y, x+1)
        tl = 1 if (y == 0) else (1 if ((x==0) and (y-1)%2) else _fetch(y-1, x-((y-1)%2)))
        tr = 1 if (y == 0) else  (1 if ((x==self.width-1) and (y%2)) else _fetch(y-1, x+(y%2)))
        bl = 1 if (y == self.height-1) else (1 if ((x==0) and (y-1)%2) else _fetch(y+1, x-((y+1)%2)))
        br = 1 if (y == self.height-1) else (1 if ((x==self.width-1) and y%2) else _fetch(y+1, x+(y%2)))
        
        hole = 0
        hole |= (l and r) or (tl and br) or (bl and tr)
        hole |= (l and tr and br) or (r and tl and bl)
        #if hole:
        #    print("{},{},{},{},{},{} = {}".format(l, tl, tr, r, br, bl, hole))
        #    print('{},{}'.format(x,y))

        return hole

    def get_hole_count(self, include_unit=False):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                count += self.is_hole(Pt(x,y), include_unit=include_unit)
        return count
 
    def get_max_altitude(self):
        for i, row in enumerate(self.cells):
            if any(row):
                return i
        return self.height

    def get_cell_count(self):
        return sum([sum(r) for r in self.cells])


