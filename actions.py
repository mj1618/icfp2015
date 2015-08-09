#!/usr/bin/env python
from render import *
from point import *
import copy
import logger

RNG_MOD = 2**32
RNG_MULT = 1103515245
RNG_INC = 12345
RNG_MASK = 0x7fff0000
RNG_TRUNC = 16

class Action:
    # helper method for performing subactions
    def subaction(self,action,board):
        result = action.do(board)
        self.subactions.append(action)
        return result

    # subclass needs to manually invoke
    def subundo(self,board):
        for act in reversed(self.subactions):
            act.undo(board)

    def do(self,board):
        if logger.active:
            logger.msg("DO: " + str(self))
        result = self._do(board)
        self._done(board)
        return result
    def undo(self,board):
        if logger.active:
            logger.msg("UNDO: " + str(self))
        result = self._undo(board)
        self._undone(board)
        return result
    def _done(self,board):
        pass
    def _undone(self,board):
        pass

# BoardAction sends the current board state to the logger after each do/undo
class BoardAction(Action):
    def _done(self,board):
        if logger.active:
            logger.board(board)
    def _undone(self,board):
        if logger.active:
            logger.board(board)

class CommandAction(BoardAction):
    def __init__(self,cmd):
        self.subactions=[]
        self.cmd=cmd
        self.lock=False
    def _do(self,board):
        board.current_unit.command(self.cmd)
        board.error = board.current_unit.is_error()
        if not board.error:
            self.lock = board.is_lock()
            if self.lock:
                board.current_unit.undo(self.cmd)
                self.subaction(NewUnitAction(), board)
        board.moves += 1
    def _undo(self,board):
        board.moves -= 1
        if self.lock:
            self.subundo(board)
        elif not board.error:
            board.current_unit.undo(self.cmd)
        board.error = False
    def __repr__(self):
        return str(self.cmd)

class RowAction(BoardAction):
    def __init__(self,y):
        self.y=y
    def _do(self,board):
        for x in range(0,board.width):
            board.grid[0][x] = 0
        for y in range(self.y, 0, -1):
            for x in range(0,board.width):
                board.grid[y][x]=board.grid[y-1][x]

    def _undo(self,board):
        for y in range(1,self.y + 1):
            for x in range(0,board.width):
                board.grid[y-1][x]=board.grid[y][x]
        for x in range(0,board.width):
            board.grid[self.y][x] = 1
    def __repr__(self):
        return "ClearRow(%d)" % self.y

class ScoreAction(Action):
    def __init__(self,amount):
        self.amount=amount
    def _do(self,board):
        board.score+=self.amount
    def _undo(self,board):
        board.score-=self.amount
    def __repr__(self):
        return "Score(+%d)" % self.amount


class RngAction(Action):
    def __init__(self,board):
        self.board = board
        self.seed = None
        self.old_seed = None

    def _do(self,board):
        self.old_seed = board.old_seed
        self.seed=board.seed
        board.old_seed = board.seed
        board.seed = ((RNG_MULT*board.seed+RNG_INC) % RNG_MOD)
        return ((board.old_seed & RNG_MASK) >> RNG_TRUNC) % len(board.units)

    def _undo(self,board):
        board.seed=self.seed
        board.old_seed=self.old_seed
        # return ((board.old_seed & RNG_MASK) >> RNG_TRUNC) % len(board.units)

class Power(Action):
    def __init__(self,word,single_unit=False):
        self.subactions=[]
        self.word=word
        self.completed = False
        #True causes the action to immediately stop if spawning a new unit
        self.single_unit = single_unit

    def _do(self,board):
        unit = None
        if self.single_unit:
            unit = board.current_unit
        for cmd in self.word.cmds:
            self.subaction(CommandAction(cmd), board)
            if board.error or board.current_unit == None:
                return False
            if self.single_unit and board.current_unit != unit:
                return False
        board.score+=2*len(self.word)
        count = board.word_count.get(self.word, 0)
        if count == 1:
            board.score += 300 #bonus for using power word a second time
        board.word_count[self.word] = count + 1
        self.completed=True
        return True

    def _done(self, board):
        if logger.active and self.completed:
            logger.msg("DONE: invoked phrase of power: " + str(self.word))

    def _undo(self,board):
        self.subundo(board)
        if self.completed:
            board.score-=2*len(self.word)
            count = board.word_count[self.word]
            if count == 2:
                board.score -= 300
            board.word_count[self.word] = count - 1
    def _undone(self, board):
        if logger.active:
            logger.msg("UNDONE: revoked phrase of power: " + str(self.word))

    def __repr__(self):
        return "PowerAction(%s)" % self.word



class NewUnitAction(Action):
    def __init__(self):
        self.unit=None
        self.index = 0
        self.subactions = []
        self.saved_old_lines = 0

    def _do(self,board):
        self.unit = board.current_unit
        self.saved_old_lines = board.old_lines_cleared

        # convert previous current_unit into filled cells
        if board.current_unit != None:
            rows = []
            for pt in board.current_unit.get_pts():
                board.grid[pt.y][pt.x] = 1
                if pt.y not in rows:
                    rows.append(pt.y)
            # check for completed rows, top to bottom
            rows.sort()
            lines_cleared = 0
            for y in rows:
                # could avoid scanning whole row by tracking how many cells are filled per row
                if sum(board.grid[y]) == board.width:
                    self.subaction(RowAction(y), board)
                    lines_cleared += 1
            self.subaction(ScoreAction(board.calculate_score(lines_cleared)), board)
            board.old_lines_cleared = lines_cleared

        if board.sources_remaining==0:
            board.current_unit = None
            return

        r = self.subaction(RngAction(board), board)
        self.index = r
        new_unit = copy.deepcopy(board.units[r])
        board.sources_remaining-=1

        board.current_unit = new_unit
        for p in new_unit.get_pts():
            if board.grid[p.y][p.x] == 1:
                board.is_full = True
                break


    def _undo(self,board):
        self.subundo(board)
        if self.unit is not None:
            for pt in self.unit.get_pts():
                board.grid[pt.y][pt.x] = 0
        board.is_full = False
        if board.current_unit is not None:
            board.sources_remaining+=1
        board.old_lines_cleared = self.saved_old_lines
        board.current_unit=self.unit
