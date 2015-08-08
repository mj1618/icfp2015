#!/usr/bin/env python
from render import *
from point import *
import copy
from actions import *
from random import randint
from unit import *
class BasicAlgorithm:
    def __init__(self,board):
        self.board=board
        self.last_pos = [0,0]
        self.i = 0


    def start(self):
        while not self.board.is_complete():
            self.step()

    def step(self):
        #
        # r = randint(0,3)
        # cmd = None
        # if r==0:
        #     cmd = Move(E)
        # elif r==1:
        #     cmd=Move(SE)
        # elif r==2:
        #     cmd=Move(SW)
        # elif r==3:
        #     cmd=Move(W)

        cmd = None
        if self.i%3==0:
            cmd = Move(E)
        elif self.i%3==1:
            cmd = Move(SW)
        elif self.i%3==2:
            cmd = Move(W)

        self.i+=1
        if self.board.current_unit is not None:
            self.last_pos = self.board.current_unit.pivot
        step = self.board.step(cmd)

        # if self.board.is_complete() and self.last_pos.y < self.board.height/2:
        #     self.board.undo_last_step()
        if self.board.is_complete():
            return
        elif self.board.error:
            self.board.undo_last_step()
