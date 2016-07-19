#!/usr/bin/env python
import os
import subprocess as sp

def get_energy():
    os.system("vasp 1>/dev/null 2>/dev/null")
    data=sp.check_output("grep TOTEN OUTCAR | tail -n 1",shell=True)
    os.system("rm WAVECAR CHGCAR CHG CONTCAR EIGENVAL OUTCAR vasprun.xml DOSCAR OSZICAR PCDAT XDATCAR")
    return float(data[data.find("=")+1:data.find("eV")].strip())

if __name__=="__main__":
    print get_energy()
