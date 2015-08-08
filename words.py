from unit import *
from point import *

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

class PowerWords:
    def __init__(self, *words):
        self.words = [ w.lower() for w in words]
        self.words.sort(key=lambda w: len(w), reverse=True)

    def encode(self, cmds):
        return [chars[cmd][0] for cmd in cmds]

    def decode(self, word):
        return [command[c] for c in word]

KnownWords = PowerWords("Ei!","Ia! Ia!","R'lyeh","Yuggoth","cthulhu")

if __name__ == "__main__":
    w, sw, se, e = Move(W), Move(SW), Move(SE), Move(E)
    cw, ccw = Rotation(Clockwise), Rotation(Counterwise)
    assert KnownWords.decode("ei!") == [e, sw, w]
    assert KnownWords.decode("ia! ia!") == [sw, sw, w, se, sw, sw, w]
    assert KnownWords.decode("yuggoth") == [e, ccw, sw, sw, se, ccw, sw]
    assert KnownWords.decode("cthulhu") == [e, ccw, sw, ccw, se, sw, ccw]
    assert KnownWords.decode("r'lyeh") == [cw, w, se, e, e, sw]
