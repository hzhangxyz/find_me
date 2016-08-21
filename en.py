#!/usr/bin/env python
import subprocess as sp
string="cat ./try_%d/OUTCAR | grep TOTEN | tail -n 1 2>/dev/null"
for i in range(100):
    ans = sp.check_output(string%i,shell=True).replace("\n","")
    if ans != "":
        print "%d\t%s"%(i,ans)
