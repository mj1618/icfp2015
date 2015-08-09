#!/usr/bin/env python
import argparse
import time

from pprint import pprint
import loader
import logger
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
from pfp_algorithm import *

def replay_test(args):
    prob = loader.get_qualifier_problems(args.p)[0]
    board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=0, sources_length=prob["sourceLength"])
    print(len(board.units))
    alg = ReplayAlgorithm(board, char_stream(sys.stdin), Animator())
    alg.start()

def placer_test():
    prob = loader.get_qualifier_problems(1)[0]
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
    print("")

def run_problem(p):
    run_problems(p,p+1)

def run_problems(start,end):


    hook = None
    if args.v:
        hook = display
    elif args.a:
        hook = animate(args.a/10)

    submit_data = []
    for p in range(start,end):
        print("Problem %d"%p)
        probs = loader.get_qualifier_problems(p)
        test_prob = probs[0]
        for seed in test_prob["sourceSeeds"]:

            prob = copy.deepcopy(test_prob)
            test_board = Board(prob["width"], prob["height"], prob["grid"], prob["units"], seed=seed,sources_length=prob["sourceLength"],step_hook=hook)

            algo = PfpAlgorithm(test_board, step_hook=hook)
            algo.start()

            print("%d"%test_board.score)

            submit_data.append({
                "problemId": p,
                "seed": seed,
                "solution": KnownWords.encode(algo.cmds)
            })

    loader.submit(submit_data)


def run_all():
    run_problems(0,25)

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
    
    if args.v:
        logger.enable(logger.Print())
    elif args.a:
        logger.enable(logger.Animate(Animator(args.a/10)))

    test_prob = probs[0]
    test_board = Board(test_prob["width"], test_prob["height"], test_prob["grid"], test_prob["units"], seed=test_prob["sourceSeeds"][0],sources_length=test_prob["sourceLength"])
    print("loaded")

    # while not test_board.is_complete():
    # for i in range(0,8):
    #     test_board.step(Move(SE))
    # test_board.step(Move(SE))
    # test_board.step(Rotation(Clockwise))
    # pdb.set_trace()

    submit_data = []

    algo = PfpAlgorithm(test_board)
    algo.start()


    print(test_board)
    print(test_board.solutions[0])
    print(KnownWords.encode(test_board.solutions[0]))
    print("%d"%test_board.score)

    submit_data.append({
        "problemId": args.p,
        "seed": test_prob["sourceSeeds"][0],
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
dispgroup = opts.add_mutually_exclusive_group()
dispgroup.add_argument("-v", help="display board state at each step", action="store_true")
dispgroup.add_argument("-a", help="animate board state (specify again for slower frames)", action="count")
actgroup = opts.add_mutually_exclusive_group()
actgroup.add_argument("-r", help="run replay test", action="store_true")
actgroup.add_argument("-pf", help="run path finder test", action="store_true")
opts.add_argument("-p", type=int, help="select a qualifying problem", default=1)
opts.add_argument("-runp", type=int, help="select a qualifying problem and submit solution")
opts.add_argument("-all", help="run through and submit all problems", action="store_true")
opts.add_argument("-s", help="submit solution to the specified problem", action="count")


if __name__ == "__main__":
    args = opts.parse_args()
    if args.r:
        replay_test(args)
    elif args.pf:
        path_finder_test()
    elif args.all:
        run_all()
    elif args.runp:
        run_problem(args.runp)
    else:
        main(args)
