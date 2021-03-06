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
    def __init__(self,board,phrases=KnownWords):
        self.board=board
        self.last_pos = [0,0]
        self.i = 0
        self.phrases = phrases
        random.seed(board.seed)


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

        success = False
        self.i += 1
        if self.i%3 ==0:
            for w in self.phrases.words:
                step = self.board.step(Power(w))
                if self.board.is_complete():
                    return
                elif self.board.error:
                    self.board.undo_last_step()
                elif step is not None:
                    success=True
                    break



        # if not success:
        ms = [Move(SE),Move(SW),Move(W),Move(E)]
        random.shuffle(ms)

        for cmd in ms:
            sources = self.board.sources_remaining
            # print("sources before: %d"%sources)

            step = self.board.step(CommandAction(cmd))
            # print("sources after: %d"%self.board.sources_remaining)
            if self.board.is_complete():
                #print("completing")
                return
            elif self.board.error:
                self.board.undo_last_step()
            elif ms.index(cmd)==3:
                success=True
                break
            # elif sources != self.board.sources_remaining:
            #     self.board.undo_last_step()
            else:
                success=True
                break


