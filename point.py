class Pt:
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

    def rotate(self, dir):
        if dir is clockwise:
            return self.to_hex().clockwise().to_pt()
        else:
            return self.to_hex().counterwise().to_pt()

    def to_hex(self):
        """ Converts to hex coordinates. """
        if self.y >= 0:
            se = self.y if abs(self.x) > abs(self.y) else self.x
            return HexPt(self.x - se, se, self.y - se)
        else:
            ne = self.y if abs(self.x) > abs(self.y) else self.x
            return HexPt(self.x - ne, self.y + ne, -ne)

NW = Pt(0, -1)
NE = Pt(1, -1)
E = Pt(1, 0)
SE = Pt(1, 1)
SW = Pt(0, 1)
W = Pt(-1, 0)

clockwise = True
counterwise = False

def sgnmul(n, pos, neg):
    if n > 0:
        return n*pos
    elif n < 0:
        return -n*neg
    return 0*pos

class HexPt:
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
        #return sgnmul(self.e, E, W) + sgnmul(self.se, SE, NW) + sgnmul(self.sw, SW, NE)
        # first, get normalized values for easting and south-eastings
        norm_e = self.e - self.sw
        norm_se = self.se + self.sw

        # hex grid is shunted right every 2 lines
        x = norm_e+(norm_se)/2
        y = norm_se

        return Pt(x, y)

