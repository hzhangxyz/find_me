#!/usr/bin/env python

"""
read find_me.json
output config.json for spearmint
"""

try: import simplejson as json
except: import json

with open("find_me.json","r") as f:
    opt = json.load(f)

spearmint_config = {
    "language"        : "PYTHON",
    "main-file"       : "test.py",
    "experiment-name" : "test_relaxation",
    "likelihood"      : "NOISELESS",
    "polling-time"    : 1,
    "max-concurrent"  : opt["maxcur"],
    "variables"        : {}
}

var_temp = {
          "type" : "FLOAT",
          "size" : 1,
          "min"  : -opt["scale"],
          "max"  : opt["scale"]
}

for i in range(1,1+sum(map(int,opt["num"].split()))):
    spearmint_config["variables"]["x%d"%i] = var_temp
