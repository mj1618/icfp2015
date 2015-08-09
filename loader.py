#!/usr/bin/env python
import http.client
import json
import urllib.request
import urllib.parse
import ssl
import os.path
from point import Pt
from unit import Unit
import base64

QUALIFIER_PROBLEM_URL = "http://icfpcontest.org/problems/problem_{}.json"
LOCAL_PATH = "qualifiers/{}.json"

def get_problem_data(i):
    local = LOCAL_PATH.format(i)
    if os.path.exists(local):
        print("Loading qualifier {} from local cache...".format(i))
        with open(local) as f:
            return f.read()
    url = QUALIFIER_PROBLEM_URL.format(i)
    print("Loading {}...".format(url))
    return urllib.request.urlopen(url).read().decode("utf8")

def get_qualifier_problems(*args):
    if len(args) == 0:
        args = range(24)
    problem_data = []
    for i in args:
        problem_data.append(loader(get_problem_data(i)))

    return problem_data

def submit(data):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('C:\\Users\\Matt\\cacert.pem')
    h = http.client.HTTPSConnection('davar.icfpcontest.org',443,context=context)
    # url_params = urllib.parse.urlencode(json.dumps(data))
    print("Submitting: "+json.dumps(data))
    headers = { 'Content-Type' : 'application/json', "Authorization" : 'Basic '+base64.b64encode(b":lI/jYDtQwdrf4s+SDq6WW91LW5bXpH04ZWhIUI+clxo=").decode("ascii") }
    h.request('POST', '/teams/77/solutions', json.dumps(data), headers)
    r1 = h.getresponse()
    print(r1.status, r1.reason)

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
        
        unit = Unit(members, pivot_p, data["width"])
        data["units"].append(unit)


    return data
    
     
