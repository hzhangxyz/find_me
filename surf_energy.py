#/usr/bin/env python
import random
import mpi4py.MPI as MPI
from shared import *

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

for i in range(times):
    S=[random.random()*(sym_region[j][1]-sym_region[j][0])+                         \
       sym_region[j][0] for j in range(l)]
    SE=get_energy(S,comm_rank,i)
    combine_S=comm.gather(S,root=0)
    combine_E=comm.gather(SE,root=0)
    if comm_rank==0:
        for j in range(comm_size):
            print combine_S[j]
            print combine_E[j]
