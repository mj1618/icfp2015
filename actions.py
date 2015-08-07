#!/usr/bin/env python
from render import *
from point import *
import copy

class Step:
    def __init__(self,actions):
        self.actions=actions
    def undo(self,board):
        for a in self.actions:
            a.undo(board)

class Action:
    pass

class CommandAction(Action):
    def __init__(self,cmd,lock):
        self.cmd=cmd
        self.lock=lock
    def do(self,board):
        board.current_unit.command(self.cmd)
    def undo(self,board):
        if not self.lock:
            board.current_unit.undo(self.cmd)

class RowAction(Action):
    def __init__(self,y):
        self.y=y
    def do(self,board):
        grid = copy.deepcopy(board.grid)
        for x in range(0,board.width):
            grid[0][x] = 0
        for y in range(1,self.y):
            for x in range(0,board.width):
                grid[y][x]=board.grid[y-1][x]

    def undo(self,board):
        grid = copy.deepcopy(board.grid)
        for x in range(0,board.width):
            grid[self.y][x] = 1
        for y in range(1,self.y):
            for x in range(0,board.width):
                grid[y-1][x]=board.grid[y][x]

class ScoreAction(Action):
    def __init__(self,amount):
        self.amount=amount
    def do(self,board):
        pass
    def undo(self,board):
        board.score-=self.amount


class SeedAction(Action):
    def __init__(self,old_seed,seed):
        self.seed = seed
        self.old_seed = old_seed
    def do(self,board):
        pass
    def undo(self,board):
        board.seed=self.seed
        board.old_seed=self.seed

class NewUnitAction(Action):
    def __init__(self,unit):
        self.unit=copy.deepcopy(unit)
    def do(self,board):
        pass
    def undo(self,board):
        for pt in board.current_unit.get_pts():
            board.grid[pt.y][pt.x] = 0
        board.current_unit=self.unit
