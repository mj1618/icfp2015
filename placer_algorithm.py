#!/usr/bin/env python
import copy

from point import *

class PlacerAlgorithm:
    def __init__(self, board, step_hook=None):
        self.board = board
        
        if step_hook is not None:
            board.install_step_hook(step_hook)


    def start(self):
        self.step()
        #while not self.board.is_complete():
        #    self.step()

    def step(self):
        heightmap = self.board.get_base_heightmap()
        #unit = copy.deepcopy(self.board.current_unit)
        unit= self.board.current_unit
        print(unit)
        points = unit.get_pts()
        #unit_y_offset = points[0].y
        #unit_x_left = points[0].x
        #unit_x_right = points[0].x

        ##for pt in points[1:]:
        #    unit_y_offset = max(unit_y_offset, pt.y)
        #    unit_x_left = min(unit_x_left, pt.x)
        #    unit_x_right = max(unit_x_right, pt.x)
        
        #unit_y_offset = unit.pivot.y-unit_y_offset
        #if unit.pivot.y %2:
        #    unit_x_left

        candidate_surfaces = set()
        for p in points:
            if (p.move(SW) not in points) or (p.move(SE) not in points):
                delta = p.delta(unit.pivot)
                print((p, delta))
                candidate_surfaces.add(delta)

        candidate_pivots = set()

        # for each of the generated unit placement spots
        for x, y in enumerate(heightmap):
            target = Pt(x, y-1)
           
            # for each target surface on unit
            for c in candidate_surfaces:
                candidate_pivots.add(target.move(c))
        
        for p in candidate_pivots:
            # place the unit at the spot temporarily
            unit.pivot = p
            if self.board.is_lock():
                continue

            # score the board
            print(self.board)

            # record the score, undo placement
        
        # carry out best move


