class Pt:
    """ An absolute point on the game board. """
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Pt(self.x*n, self.y*n)

    def __rmul__(self, n):
        return Pt.__mul__(self, n)

    def __repr__(self):
        return "(%dX %dY)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(repr(self))

    def move(self, hex):
        bias = self.y % 2
        x = self.x + hex.e + (hex.se - hex.sw + bias) // 2
        y = self.y + hex.se + hex.sw
        return Pt(x, y)

    def delta(self, pivot):
        """ Returns a HexPt that takes you from pivot -> self """
        dx = self.x - pivot.x
        dy = self.y - pivot.y
        bias = pivot.y % 2
        # get first solution by setting se = 0
        e, sw, se = dx - (-dy + bias) // 2, dy, 0
        if (e > 0 and sw > 0) or (e < 0 and sw < 0):
            # convert to canonical form
            n = e if abs(e) < abs(sw) else sw
            e -= n; sw -= n; se += n
        return HexPt(e, se, sw)

class HexPt:
    def __new__(cls, e=0, se=0, sw=0, ident=None):
        if ident is None and len([x for x in [e, se, sw] if x == 0]) == 2:
            if e == 1: return E
            elif e == -1: return W
            elif se == 1: return SE
            elif se == -1: return NW
            elif sw == 1: return SW
            elif sw == -1: return NE
        return super(HexPt, cls).__new__(cls)

    """ A relative point based on hex directions. """
    def __init__(self, e, se, sw, ident=None):
        if 'e' in self.__dict__:
            return
        self.e = e
        self.se = se
        self.sw = sw
        self.ident = ident

    def __add__(self, other):
        return HexPt(self.e + other.e, self.se + other.se, self.sw + other.sw)

    def __sub__(self, other):
        return HexPt(self.e - other.e, self.se - other.se, self.sw - other.sw)

    def __neg__(self):
        return HexPt(-self.e, -self.se, -self.sw)

    def __repr__(self):
        if self.ident is not None:
            return "(%s)" % self.ident
        return "(%dE %dSE %dSW)" % (self.e, self.se, self.sw)

    def __eq__(self, other):
        return self.e == other.e and self.se == other.se and self.sw == other.sw

    def __hash__(self):
        return hash(repr(self))

    def clockwise(self):
        """Rotates this point clockwise around 0E 0SE 0SW"""
        return HexPt(-self.sw, self.e, self.se)

    def counterwise(self):
        """Rotates this point counter-clockwise around 0E 0SE 0SW"""
        return HexPt(self.se, self.sw, -self.e)

NW = HexPt(0, -1, 0, "NW")
NE = HexPt(0, 0, -1, "NE")
E = HexPt(1, 0, 0, "E")
SE = HexPt(0, 1, 0, "SE")
SW = HexPt(0, 0, 1, "SW")
W = HexPt(-1, 0, 0, "W")

Clockwise = HexPt.clockwise
Counterwise = HexPt.counterwise

if __name__ == "__main__":
    def check(start, dir, end):
        try:
            assert start.move(dir) == end
            assert end.delta(start) == dir
        except AssertionError:
            print(start, dir, end, start.move(dir), end.delta(start))
            raise
    check(Pt(1,1), W, Pt(0,1))
    check(Pt(1,1), E, Pt(2,1))
    check(Pt(1,1), NW, Pt(1,0))
    check(Pt(1,1), NE, Pt(2,0))
    check(Pt(1,1), SW, Pt(1,2))
    check(Pt(1,1), SE, Pt(2,2))
    check(Pt(1,2), W, Pt(0,2))
    check(Pt(1,2), E, Pt(2,2))
    check(Pt(1,2), NW, Pt(0,1))
    check(Pt(1,2), NE, Pt(1,1))
    check(Pt(1,2), SW, Pt(0,3))
    check(Pt(1,2), SE, Pt(1,3))
    check(Pt(1,1), HexPt(0,2,0), Pt(2,3))
    check(Pt(1,2), HexPt(0,2,0), Pt(2,4))
    check(Pt(2,3), HexPt(0,-2,0), Pt(1,1))
    check(Pt(2,3), HexPt(0,0,-2), Pt(3,1))
    check(Pt(2,3), HexPt(0,-1,-2), Pt(3,0))
    check(Pt(2,4), HexPt(1,1,0), Pt(3,5))
    check(Pt(4,1), NE, Pt(5,0))
