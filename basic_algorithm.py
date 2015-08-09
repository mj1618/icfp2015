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
    def __init__(self,board,step_hook=None):
        self.board=board
        self.last_pos = [0,0]
        self.i = 0
        if step_hook is not None:
            board.install_step_hook(step_hook)


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

        pws = KnownWords
        success = False
        self.i += 1
        random.shuffle(pws.words)
        if self.i%3 ==0:
            for w in pws.words:
                pw=Power(w,pws.decode(w))
                step = self.board.power_step(pw)
                if self.board.is_complete():
                    return
                elif self.board.error:
                    self.board.undo_last_step()
                elif pw.completed:
                    success=True
                    break



        # if not success:
        ms = [Move(SE),Move(SW),Move(W),Move(E)]
        for cmd in ms:
            sources = self.board.sources_remaining
            # print("sources before: %d"%sources)

            step = self.board.step(cmd)
            # print("sources after: %d"%self.board.sources_remaining)
            if self.board.is_complete():
                print("completing")
                return
            elif self.board.error:
                self.board.undo_last_step()
            elif ms.index(cmd)==3:
                success=True
                break
            elif sources != self.board.sources_remaining:
                self.board.undo_last_step()
            else:
                success=True
                break


