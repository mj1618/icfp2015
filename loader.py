#!/usr/bin/env python

import json
import urllib.request

from point import Pt
from unit import Unit

QUALIFIER_PROBLEM_URL = "http://icfpcontest.org/problems/problem_{}.json"

def get_qualifier_problems(*args):
    if len(args) == 0:
        args = range(24)
    problem_data = []
    for i in args:
        url = QUALIFIER_PROBLEM_URL.format(i)
        print("Loading {}...".format(url))
        data = urllib.request.urlopen(url).read().decode("utf8")
        problem_data.append(loader(data))

    return problem_data


def loader(input_data):
    data_filthy = json.loads(input_data)

    data = {}
    data["id"] = data_filthy.get("id", -1)
    data["width"] = data_filthy.get("width", 0)
    data["height"] = data_filthy.get("height", 0)
    data["grid"] = [[0 for x in range(data["width"])] for y in range(data["height"])]

    is_valid_point = lambda pt: (pt.x >= 0) and (pt.x < data["width"]) and (pt.y >= 0) and (pt.y < data["height"])

    for point in data_filthy.get("filled", []):
        p = Pt(int(point.get("x", -1)), int(point.get("y", -1)))
        assert is_valid_point(p)
        data["grid"][p.y][p.x] = 1

    data["sourceLength"] = data_filthy.get("sourceLength", 0)
    data["sourceSeeds"] = data_filthy.get("sourceSeeds", [])
    data["units"] = []
    for unit in data_filthy.get("units"):
        
        assert ("pivot" in unit)
        pivot_p = Pt(int(unit["pivot"].get("x", -1)), int(unit["pivot"].get("y", -1)))
        assert is_valid_point(pivot_p)

        members = []
        for member in unit.get("members", []):
            member_p = Pt(int(member.get("x", -1)), member.get("y", -1))
            assert is_valid_point(member_p)
            members.append(member_p)
        
        unit = Unit(members, pivot_p)
        data["units"].append(unit)


    return data
    
     
