#!/usr/bin/env python
import subprocess as sp
import os
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-r","--readable",dest="readable",action="store_true",help="print readable message")
parser.add_option("-c","--check",dest="check",action="store_true",help="only check last energy for each file")
parser.add_option("-n","--num",dest="num",help="number of file to gather",default=100)

(opt, args) = parser.parse_args()

string="cat ./try_%d/OUTCAR | grep 'free  energy'"
for i in range(int(opt.num)):
    if os.path.exists("try_%d"%i):
        if opt.readable:
            print "%d\t:"%i
        ans = sp.check_output(string%i,shell=True).split("\n")
        if not opt.readable:
            ans = ans[:-1]
        if opt.check:
            if opt.readable:
                i = ans[-2]
            else:
                i = ans[-1]
            print i[i.find("=")+1:i.find("eV")]
        else:
            for i in ans:
                print i[i.find("=")+1:i.find("eV")]
