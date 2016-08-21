#!/usr/bin/env python
import subprocess as sp
import os
string="cat ./try_%d/OUTCAR | grep 'free  energy'"
for i in range(100):
    if os.path.exists("try_%d"%i):
        ans = sp.check_output(string%i,shell=True)
        print "%d\n%s"%(i,ans)
