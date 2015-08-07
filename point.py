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

    def move(self, hex):
        bias = self.y % 2
        x = self.x + hex.e + (hex.se - hex.sw + bias) // 2
        y = self.y + hex.se + hex.sw
        return Pt(x, y)

    def delta(self, pivot):
        bias = pivot.y % 2
        dx = pivot.x - self.x
        dy = pivot.y - self.y
        if dy >= 0:
            se = dy if abs(dx) > abs(dy) else dx
            return HexPt(dx - se, se, dy - se)
        return HexPt(0,0,0)

#-    def to_hex(self):
#-        """ Converts to hex coordinates. """
#-        if self.y >= 0:
#-            se = self.y if abs(self.x) > abs(self.y) else self.x
#-            return HexPt(self.x - se, se, self.y - se)
#-        else:
#-            ne = self.y if abs(self.x) > abs(self.y) else self.x
#-            return HexPt(self.x - ne, self.y + ne, -ne)


class HexPt:
    """ A relative point based on hex directions. """
    def __init__(self, e, se, sw):
        self.e = e
        self.se = se
        self.sw = sw

    def __add__(self, other):
        return HexPt(self.e + other.e, self.se + other.se, self.sw + other.sw)

    def __sub__(self, other):
        return HexPt(self.e - other.e, self.se - other.se, self.sw - other.sw)

    def __repr__(self):
        return "(%dE %dSE %dSW)" % (self.e, self.se, self.sw)

    def clockwise(self):
        """Rotates this point clockwise around 0E 0SE 0SW"""
        return HexPt(-self.sw, self.e, self.se)

    def counterwise(self):
        """Rotates this point counter-clockwise around 0E 0SE 0SW"""
        return HexPt(self.se, self.sw, -self.e)

    def to_pt(self):
        # first, get normalized values for easting and south-eastings
        norm_e = self.e - self.sw
        norm_se = self.se + self.sw

        # hex grid is shunted right every 2 lines
        x = norm_e+(norm_se)//2
        y = norm_se

        return Pt(x, y)

NW = HexPt(0, -1, 0)
NE = HexPt(0, 0, -1)
E = HexPt(1, 0, 0)
SE = HexPt(0, 1, 0)
SW = HexPt(0, 0, 1)
W = HexPt(-1, 0, 0)

Clockwise = HexPt.clockwise
Counterwise = HexPt.counterwise

if __name__ == "__main__":
    assert Pt(1,1).move(W) == Pt(0,1)
    assert Pt(1,1).move(E) == Pt(2,1)
    assert Pt(1,1).move(NW) == Pt(1,0)
    assert Pt(1,1).move(NE) == Pt(2,0)
    assert Pt(1,1).move(SW) == Pt(1,2)
    assert Pt(1,1).move(SE) == Pt(2,2)
    assert Pt(1,2).move(W) == Pt(0,2)
    assert Pt(1,2).move(E) == Pt(2,2)
    assert Pt(1,2).move(NW) == Pt(0,1)
    assert Pt(1,2).move(NE) == Pt(1,1)
    assert Pt(1,2).move(SW) == Pt(0,3)
    assert Pt(1,2).move(SE) == Pt(1,3)
    assert Pt(1,1).move(HexPt(0,2,0)) == Pt(2,3)
    assert Pt(1,2).move(HexPt(0,2,0)) == Pt(2,4)
    assert Pt(2,3).move(HexPt(0,-2,0)) == Pt(1,1)
    assert Pt(2,3).move(HexPt(0,0,-2)) == Pt(3,1)
    assert Pt(2,3).move(HexPt(0,-1,-2)) == Pt(3,0)
    assert Pt(2,4).move(HexPt(1,1,0)) == Pt(3,5)
