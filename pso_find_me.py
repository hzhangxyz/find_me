#/usr/bin/env python
import random
import mpi4py.MPI as MPI
from always_used import *

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

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
