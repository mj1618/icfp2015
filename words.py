from unit import *
from points import *

chars = {}
chars[Move(W)] = "p'!.03"
chars[Move(E)] = "bcefy2"
chars[Move(SW)] = "aghij4"
chars[Move(SE)] = "lmno 5"
chars[Rotate(clockwise)] = "dqrvz1"
chars[Rotate(counterwise)] = "kstuwx"

class PowerWords:
    def __init__(self, words):
        self.words = [w.to_lower() for w in words]
        self.words.sort(key=lambda w: len(w), reverse=True)

    def encode(self, cmds):
        return [chars[cmd][0] for cmd in cmds]
