#!/usr/bin/env python
import copy
import os

from point import *
from unit import *

class Nothing(Move):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls, *args, **kwargs)
    
    def __init__(self):
        super(Nothing, self).__init__(HexPt(0, 0, 0))

class PlacerAlgorithm:
    def __init__(self, board, step_hook=None):
        self.board = board
        
        if step_hook is not None:
            board.install_step_hook(step_hook)


    def start(self):
        while not self.board.is_complete():
            self.step()
            input("Press enter to contiue")
            os.system("clear")

        

    def step(self):
        heightmap = self.board.get_base_heightmap()
        #unit = copy.deepcopy(self.board.current_unit)
        old_holes = self.board.get_holes()
        print("Heightmap: {}".format(heightmap))
        print("Old hole count: {}".format(old_holes))

        unit= self.board.current_unit
        print(unit)
        points = unit.get_pts()

        candidate_surfaces = set()
        for p in points:
            if (p.move(SW) not in points) or (p.move(SE) not in points):
                delta = p.delta(unit.pivot)
                print((p, delta))
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
            score = len(holes)*20 + max_alt*3
    
            print("{} => Score {} (Hole count: {}, Max altitude: {})".format(p, score, holes, max_alt))
            print(self.board)

            # record the score, undo placement
            score_table.append((score, p))

        score_table.sort(key=lambda x: x[0])

        # carry out best move
        print("WINNER: {}".format(score_table[0]))
        unit.pivot = score_table[0][1]
        print(self.board)
        # dummy advance to get a new unit
        self.board.step(Move(SE))
        


