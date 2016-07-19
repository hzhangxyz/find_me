#/usr/bin/env python
import os
import random
import shutil
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
h=float(control[0])
pp=int(control[1])
sym_table=control[2:]
l=len(sym_table)
to_replace=pos[:start]

#define evironment
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

omega=0.1
phip=0.1
phig=0.2
times=10

S=[random.random()*2*h-h for i in range(l)]
V=[random.random()*2*h-h for i in range(l)]
PE=get_energy(S)
P=[S[i] for i in range(l)]
PG=comm.allgather(PE)
GE=min(PG)
best=PG.index(GE)
G=comm.bcast(S if comm_rank == best else None, root=best)

for i in range(times):
    if comm_rank==0:
        print "#"
        print G
        print GE
    V=[omega*V[j]+                        \
        phip*random.random()*(P[j]-S[j])+ \
        phig*random.random()*(G[j]-S[j])  \
        for j in range(l)]
    S=[S[j]+V[j] for j in range(l)]
    temp=get_energy(S)
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
    print "#"
    print G
    print GE
