#!/usr/bin/env python
from render import *
from point import *
import copy

RNG_MOD = 2**32
RNG_MULT = 1103515245
RNG_INC = 12345
RNG_MASK = 0x7fff0000
RNG_TRUNC = 16

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
    def __str__(self):
        return str(self.cmd)+str(self.lock)

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
        board.score+=self.amount
    def undo(self,board):
        board.score-=self.amount


class RngAction(Action):
    def __init__(self,board):
        self.board = board
        self.seed = None
        self.old_seed = None

    def do(self,board):
        self.old_seed = board.old_seed
        self.seed=board.seed
        board.old_seed = board.seed
        board.seed = (RNG_MULT*board.seed+RNG_INC % RNG_MOD)
        return ((board.old_seed & RNG_MASK) >> RNG_TRUNC) % len(board.units)

    def undo(self,board):
        board.seed=self.seed
        board.old_seed=self.seed
        # return ((board.old_seed & RNG_MASK) >> RNG_TRUNC) % len(board.units)

class Power(Action):
    def __init__(self,word,cmds):
        self.cmds=cmds
        self.word=word
        self.completed = False
        self.steps=[]

    def undo_last_step(self,board,step):
        board.error=False
        board.is_full = False
        for action in step.actions:
            action.undo(board)
    def do(self,board):
        for cmd in self.cmds:
            board.step(cmd)
            self.steps.append(board.steps.pop())
            if board.error or (board.is_lock() and self.cmds.index(cmd) < len(self.cmds)-1):
                for step in reversed(self.steps):
                    self.undo_last_step(board,step)
                return False
        board.score+=2*len(self.cmds)
        self.completed=True
        return True

    def undo(self,board):
        if self.completed:
            for cmd in self.cmds:
                board.undo_last_step()
            board.score-=2*len(self.cmds)


class NewUnitAction(Action):
    def __init__(self):
        self.unit=None
        self.index = 0
    def do(self,board):

        if board.current_unit != None:
            for pt in board.current_unit.get_pts():
                board.grid[pt.y][pt.x] = 1


        if len(board.units)==0:
            board.current_unit = None
            return

        r = board.rng_action()
        self.unit = copy.deepcopy(board.current_unit)
        self.index = r
        board.current_unit = board.units[r]
        board.units.pop(r)

    def undo(self,board):
        if board.current_unit is not None:
            for pt in board.current_unit.get_pts():
                board.grid[pt.y][pt.x] = 0
        board.current_unit=self.unit
        if self.unit is not None:
            board.units.insert(self.index,self.unit)
