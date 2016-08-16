#!/usr/bin/env python

from shared import run_vasp

potpath = "/home/hzhang/vasp-opt/paw-pbe"
scale = 2.
mul = 5
precision = 2
title = "CH4"
atoms = "C H"
num = "1 4"
var = [1.09,-0.36,1.03,-0.36,-0.34,0.97,-0.36,-0.34,-0.97]
tag = 0

print run_vasp(scale,
         mul,
         precision,
         title,
         atoms,
         num,
         tag,
         var,
         potpath
)
