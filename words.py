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
    assert KnownWords.decode("ei!") == [Move(E), Move(SW), Move(W)]
