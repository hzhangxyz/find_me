#/usr/bin/env python
import os
import random
import shutil
import re
import time
import subprocess as sp
import mpi4py.MPI as MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

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

raw_sym_table=control[5:]
l=len(raw_sym_table)/3
sym_table=[raw_sym_table[3*i] for i in range(l)]
sym_region=[[float(raw_sym_table[3*i+1]),
    float(raw_sym_table[3*i+2])] for i in range(l)]
to_replace=pos[:start]

#use vasp and parse result

def get_energy(var,tag1,tag2):
    this_name="try_%d_%d"%(tag1,tag2)
    this_pos=to_replace
    while this_pos.find("{")!=-1:
        starter=this_pos.find("{")
        ender=this_pos.find("}")
        to_calc=this_pos[starter+1:ender]
        for i in range(l):
            to_calc=to_calc.replace(sym_table[i],
                "(%%.%df)"%pp%var[i])
        if re.match(r"^[\d+-/\(\)\*\.]*$",to_calc):
            calc_res="%%.%df"%pp%eval(to_calc)
        else:
            calc_res="%%.%df"%pp%0
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

#pso init

S=[random.random()*(sym_region[j][1]-sym_region[j][0])+                         \
   sym_region[j][0] for j in range(l)]
V=[(2*random.random()-1)*(sym_region[j][1]-sym_region[j][0])                    \
   for j in range(l)]
PE=get_energy(S,comm_rank,-1)
P=[S[i] for i in range(l)]
PG=comm.allgather(PE)
GE=min(PG)
best=PG.index(GE)
G=comm.bcast(S if comm_rank == best else None, root=best)
if comm_rank==0:
    print G
    print GE

#pso!

for i in range(times):
    V=[omega*V[j]+                                                              \
        phip*random.random()*(P[j]-S[j])+                                       \
        phig*random.random()*(G[j]-S[j])                                        \
        for j in range(l)]
    S=[S[j]+V[j] for j in range(l)]
    S=[S[j] if S[j]<sym_region[j][1] else sym_region[j][1] for j in range(l)]
    S=[S[j] if S[j]>sym_region[j][0] else sym_region[j][0] for j in range(l)]
    temp=get_energy(S,comm_rank,i)
    if(temp<PE):
        P=[S[i] for i in range(l)]
        PE=temp
    PG=comm.allgather(PE)
    g_temp=min(PG);
    if(g_temp<GE):
        GE=g_temp
        best=PG.index(g_temp)
        G=comm.bcast(S if comm_rank == best else None, root=best)
    if comm_rank==0:
        print G
        print GE
