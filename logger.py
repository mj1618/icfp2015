# it's assumed that no logging calls will be made while active == False
active = False

impl = None

def enable(logger):
    global impl
    global active
    impl = logger
    active = True

def disable():
    global impl
    global active
    active = False
    impl = None

def msg(msg):
    impl.msg(msg)

def board(board):
    impl.board(board)

class Print:
    def msg(self, msg):
        print(msg)
    def board(self, board):
        print(board)

class Animate:
    def __init__(self, animator):
        self.anim = animator
        self.msgs = []

    def msg(self, msg):
        self.msgs.append(msg)

    def board(self, board):
        self.anim.next_frame()
        print(board)
        for msg in self.msgs:
            print(msg)
        self.msgs.clear()
