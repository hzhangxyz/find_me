#/usr/bin/env python
# in development
import os
import urllib
import json
import random
from always_used import *

DEBUG=os.getenv("DEBUG")=="T"

#bo

try:
    of=open("output","r")
    data=eval(of.read())
    of.close()
except:
    data=[]
for i in range(times):
    to_send={u'domain_info':                                                    \
             {u'dim': l,                                                        \
              u'domain_bounds':                                                 \
              [{u'max': j[1], u'min': j[0]} for j in sym_region]                \
             },                                                                 \
             u'gp_historical_info':                                             \
             {u'points_sampled':data},                                          \
             u'num_to_sample': core}
    send=urllib.urlopen("http://%s/gp/next_points/epi"%moe_url,
                        json.dumps(to_send))
    if send.code==200:
        to_get=send.read()
        send.close()
        to_bcast=json.loads(to_get)["points_to_sample"]
    else:
        send.close()
        to_bcast=[[random.random()*(sym_region[j][1]-sym_region[j][0])+         \
                   sym_region[j][0] for j in range(l)] for k in range(core)]
    if DEBUG:
        print "################"
    post_res=to_bcast[0]
    s=map(float,post_res)
    e=get_energy(s,0,i)
    gatherer={u'value_var': 0.0, u'value': e, u'point': s}
    #print gatherer
    data.append(gatherer)

print data
