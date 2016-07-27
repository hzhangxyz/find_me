#!/usr/bin/env python
with open("output","r") as out_file:
    data=out_file.read()
data="[%s]"%data.replace("\n",",")
data=[[i["point"], i["value"]] for i in eval(data)]
to_count=[i[0] for i in data]

l=len(to_count[0])

def which_box(sample,r):
    p=[int(i/r) for i in sample]
    return str(p)

def box_count(e):
    n=2**e
    r=5./n
    d=set([])
    for i in to_count[:10]:
        d.add(which_box(i,r))
    return len(d)

print map(box_count,range(10))
