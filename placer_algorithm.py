#!/usr/bin/env python
import copy
import os

from actions import *
from point import *
from unit import *

class Nothing(Move):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls, *args, **kwargs)
    
    def __init__(self):
        super(Nothing, self).__init__(HexPt(0, 0, 0))

class PlacerAlgorithm:

    test = False

    def __init__(self, board, step_hook=None):
        self.board = copy.deepcopy(board)
        
        if step_hook is not None:
            self.board.install_step_hook(step_hook)


    def start(self):
        while not self.board.is_complete():
            self.step()
            input("Press enter to contiue")
            os.system("clear")

        

    def step(self):
        heightmap = self.board.get_base_heightmap()
        #unit = copy.deepcopy(self.board.current_unit)
        old_holes = self.board.get_holes()
        if self.test: print("Heightmap: {}".format(heightmap))
        if self.test: print("Old hole count: {}".format(old_holes))

        unit= self.board.current_unit
        if self.test: print(unit)
        points = unit.get_pts()

        candidate_surfaces = set()
        for p in points:
            if (p.move(SW) not in points) or (p.move(SE) not in points):
                delta = p.delta(unit.pivot)
                if self.test: print((p, delta))
                candidate_surfaces.add(-delta)

        candidate_pivots = set()

        # for each of the generated unit placement spots
        for x, y in enumerate(heightmap):
            target = Pt(x, y-1)
           
            # for each target surface on unit
            for c in candidate_surfaces:
                candidate_pivots.add(target.move(c))
        
        score_table = []

        for p in candidate_pivots:
            # place the unit at the spot temporarily
            unit.pivot = p
            if self.board.is_lock():
                continue

            # score the board

            holes = self.board.get_holes(include_unit=True)
            max_alt = self.board.get_max_altitude(include_unit=True)
            line_bonus = {}
            #for p in unit.get_pts():
            #    if p.y not in line_bonus:
            #        line_bonus[p.y] = 0
            #    line_bonus[p.y] += 1
            #for y in line_bonus:
            #    line_bonus[y] += sum(self.board.grid[y])
            #    line_bonus[y] = 200//(self.board.width+1-line_bonus[y])

            score = len(holes)*20 + max_alt*1 #+ sum(line_bonus)
    
            if self.test: print("{} => Score {} (Hole count: {}, Max altitude: {}, Line Bonus: {})".format(p, score, holes, max_alt, line_bonus))
            if self.test: print(self.board)

            # record the score, undo placement
            score_table.append((score, p))

        score_table.sort(key=lambda x: x[0])

        # carry out best move
        if self.test: print("WINNER: {}".format(score_table[0]))
        unit.pivot = score_table[0][1]
        if self.test: print(self.board)
        # dummy advance to get a new unit
        for pt in self.board.current_unit.get_pts():
            self.board.grid[pt.y][pt.x] = 1
        #
        # r = self.board.rng_action()
        # self.board.current_unit = copy.deepcopy(self.board.units[r])

        units = []
        for s in score_table:
            unit.pivot = s[1]
            units.append(copy.deepcopy(unit))

        return units


