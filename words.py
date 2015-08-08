from unit import *
from point import *

chars = {}
chars[Move(W)] = "p'!.03"
chars[Move(E)] = "bcefy2"
chars[Move(SW)] = "aghij4"
chars[Move(SE)] = "lmno 5"
chars[Rotation(Clockwise)] = "dqrvz1"
chars[Rotation(Counterwise)] = "kstuwx"




class PowerWords:



    def __init__(self):
        words = ["Ei!","Ia! Ia!","R'lyeh","Yuggoth","cthulhu","pentagram"]
        self.words = [ w.lower() for w in words]
        self.words.sort(key=lambda w: len(w), reverse=True)

    def encode(self, cmds):
        return [chars[cmd][0] for cmd in cmds]

    def decode(self,word):
        cmds = []
        for w in word:
            for move,chs in chars.items():
                if w in chs:
                    cmds.append(move)
        return cmds
