#/usr/bin/env python
import math
import random
#import mpi4py.MPI as MPI
from always_used import *
"""
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()
"""

S=[random.random()*(sym_region[j][1]-sym_region[j][0])+                         \
   sym_region[j][0] for j in range(l)]
E=get_energy(S,comm_rank,-1)
print S
print E

T=1
t=0.1
a=0.9
h=0.1

while T>t:
    T*=t
    SS=[S[j]+h*(random.random()-0.5) for j in range(l)]
    SS=[SS[j] if SS[j]<sym_region[j][1] else sym_region[j][1] for j in range(l)]
    SS=[SS[j] if SS[j]>sym_region[j][0] else sym_region[j][0] for j in range(l)]
    EE=get_energy(SS)
    if random.random()<=math.exp((EE-E)/T):
        E=EE
        S=SS
    print S
    print E
