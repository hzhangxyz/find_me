#/usr/bin/env python
# in development
import os
import urllib
import json
import random
import mpi4py.MPI as MPI
from always_used import *

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

DEBUG=os.getenv("DEBUG")=="T"

#bo

if comm_rank==0:
    data=[]
for i in range(times):
    if comm_rank==0:
        to_send={u'domain_info':                                                    \
                 {u'dim': l,                                                        \
                  u'domain_bounds':                                                 \
                  [{u'max': j[1], u'min': j[0]} for j in sym_region]                \
                 },                                                                 \
                 u'gp_historical_info':                                             \
                 {u'points_sampled':data},                                          \
                 u'num_to_sample': core}
        send=urllib.urlopen("http://127.0.0.1:6543/gp/next_points/epi",
                            json.dumps(to_send))
        to_get=json.loads(send.read())
        if DEBUG:
            print to_get
        send.close()
    post_res=comm.bcast(to_get["points_to_sample"] if comm_rank==0 else None, root=0)
    s=map(float,post_res[comm_rank])
    e=get_energy(s,comm_rank,0)
    gatherer=comm.gather({u'value_var': 0.0, u'value': e, u'point': s})
    if comm_rank==0:
        data+=gatherer
if comm_rank==0:
    print data
