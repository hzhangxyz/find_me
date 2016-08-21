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
#tag = 0

def main(s_id,pre_var):
    tag=s_id
    var = map(lambda x:pre_var[x],"x1 x2 x3 x4 x5 x6 x7 x8 x9".split())
    pos = []
    for i in range(len(var)/3+2):
        if i == 0:
            pos.append((0,0,0))
        elif i == 1:
            pos.append((0,0,var[0]))
        elif i == 2:
            pos.append((0,var[1],var[2]))
        else:
            pos.append((var[i*3-6],var[i*3-5],var[i*3-4]))
    def dis(p1,p2):
        s=(p1[0]-p2[0])**2+\
        (p1[1]-p2[1])**2+\
        (p1[2]-p2[2])**2
        import math
        return math.sqrt(s)
    for i in range(len(pos)):
        for j in range(len(pos)):
            if i != j:
                if dis(pos[i],pos[j])<0.2:
                    return 100
    pre_ans = run_vasp(scale,
         mul,
         precision,
         title,
         atoms,
         num,
         tag,
         var,
         potpath
    )
    length = len(pre_ans)
    ans = []
    while length != 0:
        ans.append(pre_ans[-length])
        length = length/2
    return [[dict(map(lambda x:("x%d"%x,i[0][x-1]), range(1,10))),i[1]] for i in ans]
