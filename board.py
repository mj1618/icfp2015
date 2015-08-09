#!/usr/bin/env python
from render import *
from point import *
from unit import *
from words import *
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

    def __init__(self, width, height, grid, units, seed, sources_length, step_hook=None):
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
        self.old_lines_cleared = 0
        self.word_count = {} #map from power word -> number of times used
        self.score = 0
        self.sources_remaining = sources_length
        self.error = False
        self.is_full = False
        self.step_hook = step_hook
        self.moves = 0

        self.step()

    def install_step_hook(self, step_hook):
        self.step_hook = step_hook

    def step(self,cmd=None):
        if self.current_unit is None:
            self.next_unit_action()
        elif isinstance(cmd, Command):
            self.command(cmd)
        elif isinstance(cmd, PowerWord):
            self.power_word(cmd)
        else:
            raise TypeError(type(cmd))
        current_step = Step(self.current_actions)
        self.steps.append(current_step)
        self.current_actions=[]
        if self.step_hook is not None:
            self.step_hook(self, False, cmd)
        return current_step

    def place_unit(self,unit):
        for pt in unit.get_pts():
            self.grid[pt.y][pt.x] = 1

    def undo_last_step(self):
        self.error=False
        self.is_full = False
        step = self.steps.pop()
        for action in step.actions:
            action.undo(self)
            if self.step_hook is not None and type(action) is CommandAction:
                self.step_hook(self, True, action.cmd)
        return step

    def is_complete(self):
        return (self.sources_remaining==0 and self.current_unit is None) or self.is_full

    # returns the list of commands/power words needed to reach the current state
    def get_solution(self):
        solution = []
        for step in self.steps:
            for action in step.actions:
                if type(action) is CommandAction:
                    solution.append(action.cmd)
                elif type(action) is Power:
                    solution.append(action)
        return solution

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
        act = CommandAction(cmd)
        self.current_actions.append(act)
        act.do(self)
        return not self.error

    def power_word(self, word):
        act = Power(word)
        act.do(self)
        self.current_actions.append(act)
        return act.completed

    def is_cell_valid(self, point):
        return not ((point.x < 0) or (point.x >= self.width) or (point.y < 0) or (point.y >= self.height))

    def is_lock(self):
        if self.current_unit is not None:
            for pt in self.current_unit.get_pts():
                if not self.is_cell_valid(pt) or self.grid[pt.y][pt.x]==1:
                    return True
        else: return True
        return False

    def calculate_score(self, lines_cleared):
        points = len(self.current_unit.mask) + 100*(1+lines_cleared)*lines_cleared//2
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
        grid = render_grid(self.width, self.height, self.query_cell)
        status = ""
        if self.error: status="ERROR"
        elif self.is_complete(): status="DONE"
        detail = " %5s   Score: %d   Moves: %d   Remain: %d" % (status, self.score, self.moves, self.sources_remaining)
        return grid + detail

    def get_base_heightmap(self):
        heightmap = [0 for i in range(self.width)]
        
        column = 0
        row = 0

        def _follow(point, heightmap):
            print("Begin trace at {}".format(point))
            p = point
            path = set()
            finished = False
            hm = copy.copy(heightmap)
            _hash = lambda x: hash(repr(x))
            _value = lambda p: (1 if p.y >= self.height else 0) or (self.is_cell_valid(p) and (self.grid[p.y][p.x] == 1))

            while not finished:

                ne = p.move(NE)
                if (_hash((ne, NE)) not in path) and _value(ne):
                    path.add(_hash((ne, NE)))
                    hm[ne.x] = max(hm[ne.x], ne.y)
                    p = ne
                    #print("({}) {}".format(NE, ne))
                    continue

                # if we reach the other side, then we have a closed surface and can update the heightmap
                if p.x == (self.width-1):
                    finished = p.x
                    continue

                e = p.move(E)
                if (_hash((e, E)) not in path) and _value(e):
                    path.add(_hash((e, E)))
                    hm[e.x] = max(hm[e.x], e.y)
                    p = e
                    #print("({}) {}".format(E, e))
                    continue
                        
                se = p.move(SE)
                if (_hash((se, SE)) not in path) and _value(se):
                    path.add(_hash((se, SE)))
                    hm[se.x] = max(hm[se.x], se.y)
                    p = se
                    #print("({}) {}".format(SE, se))
                    continue

                sw = p.move(SW)
                if (_hash((sw, SW)) not in path) and _value(sw):
                    path.add(_hash((sw, SW)))
                    p = sw
                    #print("({}) {}".format(SW, sw))
                    continue

                w = p.move(W)
                if (_hash((w, W)) not in path) and _value(w):
                    path.add(_hash((w, W)))
                    p = w
                    #print("({}) {}".format(W, w))
                    continue

                nw = p.move(NW)
                if (_hash((nw, NW)) not in path) and _value(nw):
                    path.add(_hash((nw, NW)))
                    p = nw
                    #print("({}) {}".format(NW, nw))
                    continue

                print("Trace bombed out!\n")
                # we've hit a loop
                return -1
            for i in range(len(heightmap)):
                heightmap[i] = hm[i]
            print("Trace finished!\n")
            return finished
            

        while (column < self.width):
            for row in range(self.height):
                if self.grid[row][column] == 1:
                    result = _follow(Pt(column, row), heightmap)
                    if result != -1:
                        heightmap[column] = row
                        column = result
                        break
                elif row == self.height-1:
                    result = _follow(Pt(column, row+1), heightmap)
                    if result != -1:
                        heightmap[column] = row+1
                        column = result
                        break
            column += 1

        return heightmap



    def is_hole(self, point, include_unit=False):
        assert self.is_cell_valid(point)

        unit_points = self.current_unit.get_pts()

        def _fetch(pt):
            if not self.is_cell_valid(pt):
                return 1
            if include_unit and (pt in unit_points):
                return 1
            return self.grid[pt.y][pt.x]

        if _fetch(point) == 1:
            return 0

        l = _fetch(point.move(W))
        r = _fetch(point.move(E))
        tl = _fetch(point.move(NW))
        tr = _fetch(point.move(NE))
        bl = _fetch(point.move(SW))
        br = _fetch(point.move(SE))
        
        hole = 0
        #hole |= (l and r) or (tl and br) or (bl and tr)
        hole |= (l and tr and br) or (r and tl and bl)
        hole |= (l and r and bl and br)
        #if hole:
        #    print("{},{},{},{},{},{} = {}".format(l, tl, tr, r, br, bl, hole))
        #    print('{},{}'.format(x,y))

        return hole

    def get_holes(self, include_unit=False):
        count = 0
        holes = set()

        for y in range(self.height):
            for x in range(self.width):
                point = Pt(x, y)
                if self.is_hole(point, include_unit=include_unit):
                    holes.add(point)
        return holes
 
    def get_max_altitude(self, include_unit=False):

        alt = self.height
        for i, row in enumerate(self.grid):
            if any(row):
                alt = i
        if include_unit:
            for pt in self.current_unit.get_pts():
                if pt.y < alt:
                    alt = pt.y
        return self.height-alt

    def get_cell_count(self):
        return sum([sum(r) for r in self.grid])


