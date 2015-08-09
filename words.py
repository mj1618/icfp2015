from unit import *
from point import *
from actions import *

chars = {}
chars[Move(W)] = "p'!.03"
chars[Move(E)] = "bcefy2"
chars[Move(SW)] = "aghij4"
chars[Move(SE)] = "lmno 5"
chars[Rotation(Clockwise)] = "dqrvz1"
chars[Rotation(Counterwise)] = "kstuwx"

# reverse mapping (character -> command)
command = {}
for key, val in chars.items():
    for char in val:
        command[char] = key

def decode_word(word):
    return [command[c] for c in word]

class PowerWords:
    def __init__(self, *words):
        self.words = [ w.lower() for w in words]
        self.words.sort(key=lambda w: len(w), reverse=True) #longest words first

    def encode1(self, action):
        if isinstance(action, Command):
            return chars[action][0]
        elif isinstance(action, Power):
            return action.word
        raise TypeError(type(action))

    def encode(self, actions):
        return "".join([self.encode1(action) for action in actions])

KnownWords = PowerWords("Ei!","Ia! Ia!","R'lyeh","Yuggoth","cthulhu")

if __name__ == "__main__":
    w, sw, se, e = Move(W), Move(SW), Move(SE), Move(E)
    cw, ccw = Rotation(Clockwise), Rotation(Counterwise)
    assert decode_word("ei!") == [e, sw, w]
    assert decode_word("ia! ia!") == [sw, sw, w, se, sw, sw, w]
    assert decode_word("yuggoth") == [e, ccw, sw, sw, se, ccw, sw]
    assert decode_word("cthulhu") == [e, ccw, sw, ccw, se, sw, ccw]
    assert decode_word("r'lyeh") == [cw, w, se, e, e, sw]
