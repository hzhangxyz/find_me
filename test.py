#!/usr/bin/env python

from shared import run_vasp

potpath = "/home/hzhang/vasp-opt/paw-pbe"
scale = 2.
mul = 5
precision = 2
title = "CH4"
atoms = "C H"
num = "1 4"
#var = [1.09,-0.36,1.03,-0.36,-0.34,0.97,-0.36,-0.34,-0.97]
tag = 0

def main(s_id,pre_var):
    var = map(lambda x:pre_var[x],"x1 x2 x3 x4 x5 x6 x7 x8 x9".split())
    ans = run_vasp(scale,
         mul,
         precision,
         title,
         atoms,
         num,
         tag,
         var,
         potpath
    )
    return [[dict(map(lambda x:("x%d"%x,i[0][x]), range(1,10))),i[1]] for i in ans]
