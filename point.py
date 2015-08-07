class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "(%d,%d)" % (self.x, self.y)

NW = Pt(0, -1)
NE = Pt(1, -1)
E = Pt(1, 0)
SE = Pt(1, 1)
SW = Pt(0, 1)
W = Pt(-1, 0)    
