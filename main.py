#!/usr/bin/env python
import argparse
import time

from pprint import pprint
import loader
from board import *
from unit import *
from point import *
from actions import *
from words import *
from basic_algorithm import *
from replay_algorithm import *
from placer_algorithm import *
# import pdb
import sys
import codecs
from path_finder import *

def replay_test():
    prob = loader.get_qualifier_problems(6)[0]
    board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=0, sources_length=prob["sourceLength"])
    print(len(board.units))
    alg = ReplayAlgorithm(board, "iiiiiiimimiiiiiimmimiiiimimimmimimimimmeemmimimiimmmmimmimiimimimmimmimeeemmmimimmimeeemiimiimimimiiiipimiimimmmmeemimeemimimimmmmemimmimmmiiimmmiiipiimiiippiimmmeemimiipimmimmipppimmimeemeemimiieemimmmm", Animator())
    alg.start()

def placer_test():
    prob = loader.get_qualifier_problems(0)[0]
    board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=0, sources_length=prob["sourceLength"])
    alg = PlacerAlgorithm(board)
    alg.start()

def path_finder_test():
    prob = loader.get_qualifier_problems(2)[0]
    board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=1, sources_length=prob["sourceLength"])
    board.install_step_hook(step_hook=animate(5/10))
    pf = PathFinder(board,Unit([Pt(0,0)],Pt(0,0),board.width,False),Unit([Pt(10,10)],Pt(10,10),board.width,False))
    pf.find_path()

def display(board, is_undo, cmd):
    print("%s: %s" % ("UNDO" if is_undo else "DO", str(cmd)))
    print(board)
    print("   Score:", board.score)
    print("")

class Animator:
    def __init__(self, delay=0.1):
        self.last_frame = None
        self.delay = delay

    def next_frame(self):
        # sleep until next frame, if necessary
        now = time.time()
        if self.last_frame is not None:
            deadline = self.last_frame + self.delay
            while now < deadline:
                time.sleep(deadline - now)
                now = time.time()
        self.last_frame = now
        # clear screen
        print("\033[H\033[J")
        #os.system('cls' if os.name == 'nt' else 'clear')

# returns a step_hook suitabe function
def animate(delay=0.1):
    animator = Animator(delay)
    def show_frame(board, is_undo, cmd):
        animator.next_frame()
        display(board, is_undo, cmd)
    return show_frame

def main(args):


    probs = loader.get_qualifier_problems(args.p)
    
    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0],sources_length=test_prob["sourceLength"])
    print("loaded")

    # while not test_board.is_complete():
    # for i in range(0,8):
    #     test_board.step(Move(SE))
    # test_board.step(Move(SE))
    # test_board.step(Rotation(Clockwise))
    # pdb.set_trace()

    hook = None
    if args.v:
        hook = display
    elif args.a:
        hook = animate(args.a/10)


    submit_data = []

    algo = BasicAlgorithm(test_board, step_hook=hook)
    algo.start()

    exit()

    print("%d"%test_board.score)
    print(test_board)
    print(test_board.solutions[0])
    print(KnownWords.encode(test_board.solutions[0]))

    submit_data.append({
        "problemId": args.p,
        "seed": test_prob["sourceSeeds"][0],
        "tag": time.strftime("%H:%M:%S"),
        "solution": KnownWords.encode(test_board.solutions[0])
    })


    for step in test_board.steps:
        for action in step.actions:
            pprint(vars(action))
    if args.s:
        loader.submit(submit_data)
    #
    # for step in test_board.steps:
    #     for action in step.actions:
    #         if type(action) is CommandAction:
    #

opts = argparse.ArgumentParser()
group = opts.add_mutually_exclusive_group()
group.add_argument("-v", help="display board state at each step", action="store_true")
group.add_argument("-a", help="animate board state (specify again for slower frames)", action="count")
group.add_argument("-r", help="run replay test", action="store_true")
group.add_argument("-pf", help="run path finder test", action="store_true")
opts.add_argument("-p", type=int, help="select a qualifying problem", default=1)
opts.add_argument("-s", help="submit solution to the specified problem", action="count")


if __name__ == "__main__":
    args = opts.parse_args()
    if args.r:
        replay_test()
    if args.pf:
        path_finder_test()
    else:
        main(args)
