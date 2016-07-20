#/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import random
import shutil
import subprocess as sp
import mpi4py.MPI as MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

#读取POSCAR
with open("POSCAR","r") as pos_file:
    pos=pos_file.read()

#解析POSCAR
start=pos.find("{{")
end=pos.find("}}")
control=pos[start+2:end].split()
h=float(control[0])
pp=int(control[1])
sym_table=control[2:]
l=len(sym_table)
to_replace=pos[:start]

#调用vasp并解析输出
def get_energy(var):
    this_name="try_%d"%hash(str(var))
    this_pos=to_replace
    for i in range(len(sym_table)):
        this_pos=this_pos.replace("{%s}"%sym_table[i],
            "%%.%df"%pp%var[i])
    os.makedirs(this_name)
    shutil.copy("INCAR","%s/INCAR"%this_name)
    shutil.copy("POTCAR","%s/POTCAR"%this_name)
    shutil.copy("KPOINTS","%s/"%this_name)
    with open("%s/POSCAR"%this_name,"w") as this_pos_file:
        this_pos_file.write(this_pos)
    os.system("cd %s;../vasp 1>/dev/null"%this_name)
    with open("%s/OUTCAR"%this_name,"r") as to_ana_file:
        to_ana=to_ana_file.read()
        temp=to_ana.find("TOTEN",0)
        offset=0
        while(temp!=-1):
             offset=temp+1
             temp=to_ana.find("TOTEN",offset)
        data=to_ana[to_ana.find("=",offset)+1:  \
            to_ana.find("eV",offset)].strip()
    data=float(data)
    shutil.rmtree(this_name)
    return float(data)

times=2

for i in range(times):
    S=[random.random()*2*h-h for i in range(l)]
    SE=get_energy(S)
    combine_S=comm.gather(S,root=0)
    combine_E=comm.gather(SE,root=0)
    if comm_rank==0:
        for j in range(comm_size):
            print combine_S[j]
            print combine_E[j]
