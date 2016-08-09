#!/usr/bin/env python
#

import os
import shutil
from math import *

# parse POSCAR

with open("POSCAR","r") as pos_file:
    pos=pos_file.read()

start=pos.find("{{")
end=pos.find("}}")
control=pos[start+2:end].split()

def get_param(name):
    try:
        ans = control[control.index(name)+1]
        return ans
    except:
        return None

omega = float(get_param("omega"))
phip = float(get_param("phip"))
phig = float(get_param("phig"))

precision = int(get_param("precision"))
times = int(get_param("times"))
cores = int(get_param("cores"))

raw_sym_table=control[control.index("vars")+1:]
dim=len(raw_sym_table)/3
sym_table=[raw_sym_table[3*i] for i in range(dim)]
sym_region=[[float(raw_sym_table[3*i+1]),
    float(raw_sym_table[3*i+2])] for i in range(dim)]

to_replace=pos[:start]

# use vasp and parse result

def get_energy_vasp(var,tag1,tag2):
    this_name="try_%d_%d"%(tag1,tag2)
    this_pos=to_replace
    while this_pos.find("{")!=-1:
        starter=this_pos.find("{")
        ender=this_pos.find("}")
        to_calc=this_pos[starter+1:ender]
        for i in range(dim):
            to_calc=to_calc.replace("(%s)"%sym_table[i],
                "(%%.%df)"%precision%var[i])
        calc_res="%%.%df"%precision%eval(to_calc)
        this_pos="%s%s%s"%(this_pos[:starter],calc_res,this_pos[ender+1:])
    shutil.rmtree(this_name,ignore_errors=True)
    os.makedirs(this_name)
    shutil.copy("INCAR","%s/INCAR"%this_name)
    shutil.copy("POTCAR","%s/POTCAR"%this_name)
    shutil.copy("KPOINTS","%s/"%this_name)
    with open("%s/POSCAR"%this_name,"w") as this_pos_file:
        this_pos_file.write(this_pos)
    os.system("cd %s;vasp_without_mpi 1>output"%this_name)
    with open("%s/OUTCAR"%this_name,"r") as to_ana_file:
        to_ana=to_ana_file.read()
        temp=to_ana.find("TOTEN",0)
        offset=0
        while(temp!=-1):
             offset=temp+1
             temp=to_ana.find("TOTEN",offset)
        if offset!=0:
            data=float(to_ana[to_ana.find("=",offset)+1:                        \
                to_ana.find("eV",offset)].strip())
        else:
            data="2147483647"
    return float(data)

get_energy=get_energy_vasp
