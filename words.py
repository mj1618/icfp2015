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

class PowerWord:
    def __init__(self, word):
        self.word = word.lower()
        self.cmds = decode_word(self.word)
        self.net_displacement = HexPt(0,0,0)
        self.net_rotation = 0
        for c in self.cmds:
            if isinstance(c, Move):
                self.net_displacement += c.dir
            elif isinstance(c, Rotation):
                self.net_rotation += 1 if c.rot is Clockwise else -1
        self.net_displacement = self.net_displacement.canonicalise()

    def __str__(self):
        return self.word

    def __len__(self):
        return len(self.word)

class PowerWords:
    def __init__(self, *words):
        self.words = [ PowerWord(w) for w in words]
        self.words.sort(key=lambda w: len(w), reverse=True) #longest words first

    def encode1(self, action):
        if isinstance(action, Command):
            return chars[action][0]
        elif isinstance(action, Power):
            if action.completed:
                return str(action.word)
            # the basic alg sometimes finishes the game halfway through a power word
            # in this case we'd cause an error by encoding the entire word
            return str(action.word)[:len(action.subactions)]
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
    assert PowerWord("yuggoth").net_displacement == HexPt(0, 2, 2)
    assert PowerWord("yuggoth").net_rotation == -2
    assert PowerWord("r'lyeh").net_displacement == HexPt(0, 2, 0)
    assert PowerWord("r'lyeh").net_rotation == 1
