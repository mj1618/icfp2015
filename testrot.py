import pathlib
from loader import *
from point import *

for f in pathlib.Path('qualifiers').iterdir():
    if not f.is_file():
        continue
    with f.open() as fd:
        data = loader(fd.read())
    #board = Board(data["width"], data["height"], data["grid"], data["units"], seed=data["sourceSeeds"][0])
    print("QUALIFIER", f)
    for i,u in enumerate(data["units"]):
        print("UNIT", i)
        for _ in range(6):
            print(u.pivot, u.mask, u.get_pts())
            print(u)
            u.rotate(Clockwise)
        for _ in range(6):
            print(u.pivot, u.mask, u.get_pts())
            print(u)
            u.rotate(Counterwise)
