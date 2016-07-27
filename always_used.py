#!/usr/bin/env python
# this file is interface to VASP
# require file:
# INCAR,POTCAR,KPOINTS,POSCAR
# INCAR and KPOINTS should be the same with this repo
# POTCAR depends on the system to calculate
# POSCAR has different syntax with VASP

import os
import shutil
import math

#read POSCAR

with open("POSCAR","r") as pos_file:
    pos=pos_file.read()

#parse POSCAR

start=pos.find("{{")
end=pos.find("}}")
control=pos[start+2:end].split()

pp=int(control[0])
omega=float(control[1])
phip=float(control[2])
phig=float(control[3])
times=int(control[4])
core=int(control[5])

raw_sym_table=control[6:]
l=len(raw_sym_table)/3
sym_table=[raw_sym_table[3*i] for i in range(l)]
sym_region=[[float(raw_sym_table[3*i+1]),
    float(raw_sym_table[3*i+2])] for i in range(l)]
to_replace=pos[:start]

#use vasp and parse result

def get_energy_vasp(var,tag1,tag2):
    this_name="try_%d_%d"%(tag1,tag2)
    this_pos=to_replace
    while this_pos.find("{")!=-1:
        starter=this_pos.find("{")
        ender=this_pos.find("}")
        to_calc=this_pos[starter+1:ender]
        for i in range(l):
            to_calc=to_calc.replace("(%s)"%sym_table[i],
                "(%%.%df)"%pp%var[i])
        calc_res="%%.%df"%pp%eval(to_calc)
        this_pos="%s%s%s"%(this_pos[:starter],calc_res,this_pos[ender+1:])
    os.makedirs(this_name)
    shutil.copy("INCAR","%s/INCAR"%this_name)
    shutil.copy("POTCAR","%s/POTCAR"%this_name)
    shutil.copy("KPOINTS","%s/"%this_name)
    with open("%s/POSCAR"%this_name,"w") as this_pos_file:
        this_pos_file.write(this_pos)
    os.system("cd %s;vasp_without_mpi 1>/dev/null"%this_name)
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
            data="100"
    return float(data)

get_energy=get_energy_vasp
