#!/usr/bin/env python
import random
from words import *
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

        pws = PowerWords()
        success = False
        for w in pws.words:
            step = self.board.action_step(Power(w,pws.decode(w)))
            if self.board.is_complete():
                return
            elif self.board.error:
                self.board.undo_last_step()
            else:
                success=True
                break
        if not success:
            for cmd in random.shuffle([Move(E),Move(SE),Move(SW),Move(W)]):
                step = self.board.step(cmd)
                if self.board.is_complete():
                    return
                elif self.board.error:
                    self.board.undo_last_step()
                else:
                    success=True
                    break