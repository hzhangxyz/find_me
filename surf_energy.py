#!/usr/bin/env python
#

import random
import sys
import mpi4py.MPI as MPI
from shared import find_me_parser

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

runner = find_me_parser(sys.argv[1])

for i in range(runner.times):
    S=[random.random()*(runner.sym_region[j][1]-runner.sym_region[j][0])+                         \
       runner.sym_region[j][0] for j in range(runner.dim)]
    SE=runner.get_energy(S,comm_rank,i)
    combine_S=comm.gather(S,root=0)
    combine_E=comm.gather(SE,root=0)
    if comm_rank==0:
        for j in range(comm_size):
            print combine_S[j]
            print combine_E[j]
