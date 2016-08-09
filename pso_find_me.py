#/usr/bin/env python

import os
import random
import mpi4py.MPI as MPI
from shared import get_energy,dim,sym_region,times,omega,phip,phig

os.system("rm try* -rf")

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

# pso init

S=[random.random()*(sym_region[j][1]-sym_region[j][0])+                         \
   sym_region[j][0] for j in range(dim)]
V=[(2*random.random()-1)*(sym_region[j][1]-sym_region[j][0])                    \
   for j in range(dim)]
PE=get_energy(S,comm_rank,-1)
P=[S[i] for i in range(dim)]
PG=comm.allgather(PE)
GE=min(PG)
best=PG.index(GE)
G=comm.bcast(S if comm_rank == best else None, root=best)
DEBUG=os.getenv("DEBUG")=="T"

if DEBUG:
    combine_S=comm.gather(S,root=0)
    combine_E=comm.gather(PE,root=0)
    if comm_rank==0:
        for j in range(comm_size):
            print combine_S[j]
            print combine_E[j]
else:
    if comm_rank==0:
        print G
        print GE

# pso

for i in range(times):
    V=[omega*V[j]+                                                              \
        phip*random.random()*(P[j]-S[j])+                                       \
        phig*random.random()*(G[j]-S[j])                                        \
        for j in range(dim)]
    S=[S[j]+V[j] for j in range(dim)]
    S=[S[j] if S[j]<sym_region[j][1] else sym_region[j][1] for j in range(dim)]
    S=[S[j] if S[j]>sym_region[j][0] else sym_region[j][0] for j in range(dim)]
    temp=get_energy(S,comm_rank,i)
    # p
    if(temp<PE):
        P=[S[i] for i in range(dim)]
        PE=temp
    # g
    PG=comm.allgather(PE)
    g_temp=min(PG);
    if(g_temp<GE):
        GE=g_temp
        best=PG.index(g_temp)
        G=comm.bcast(S if comm_rank == best else None, root=best)
    # output
    if DEBUG:
        combine_S=comm.gather(S,root=0)
        combine_E=comm.gather(temp,root=0)
        if comm_rank==0:
            for j in range(comm_size):
                print combine_S[j]
                print combine_E[j]
    else:
        if comm_rank==0:
            print G
            print GE
