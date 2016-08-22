#!/usr/bin/env python

import os
import shutil
try: import simplejson as json
except: import json

def main(s_id,pre_var):
    # Pretreatment
    with open("find_me.json","r") as f:
        opt = json.load(f)

    potpath = opt["potpath"]
    scale = opt["scale"]
    mul = opt["mul"]
    precision = opt["precision"]
    title = opt["title"]
    atoms = opt["atoms"]
    num = opt["num"]
    vasp = opt["vasp"]
    tag = s_id
    var = map(lambda x:pre_var["x%d"%x],range(1,len(pre_var)+1))
    pos = []
    for i in range(len(var)/3+2):
        if i == 0:
            pos.append((0,0,0))
        elif i == 1:
            pos.append((0,0,var[0]))
        elif i == 2:
            pos.append((0,var[1],var[2]))
        else:
            pos.append((var[i*3-6],var[i*3-5],var[i*3-4]))
    def dis(p1,p2):
        s=(p1[0]-p2[0])**2+\
        (p1[1]-p2[1])**2+\
        (p1[2]-p2[2])**2
        import math
        return math.sqrt(s)
    for i in range(len(pos)):
        for j in range(len(pos)):
            if i != j:
                if dis(pos[i],pos[j])<0.2:
                    return 100
    nums=sum(map(int,num.split()))
    # Generate POSCAR
    p=precision
    cys = "%%.%df %%.%df %%.%df\n%%.%df %%.%df %%.%df\n%%.%df %%.%df %%.%df"%(
        p,p,p,p,p,p,p,p,p
    )%(
        scale*mul,0,0,
        0,scale*mul,0,
        0,0,scale*mul
    )
    posi = ""
    for i in range(nums):
        if i == 0:
            posi+="%%.%df %%.%df %%.%df F F F\n"%(p,p,p)%(
                0,0,0)
        elif i == 1:
            posi+="%%.%df %%.%df %%.%df T F F\n"%(p,p,p)%(
                var[0],0,0)
        elif i == 2:
            posi+="%%.%df %%.%df %%.%df T T F\n"%(p,p,p)%(
                var[1],var[2],0)
        else:
            posi+="%%.%df %%.%df %%.%df T T T\n"%(p,p,p)%(
                var[i*3-6],var[i*3-5],var[i*3-4])
    poscar = "%s\n%s\n%s\n%s\n%s\nS\nC\n%s"%(
        title,
        "%%.%df"%precision%1,
        cys,
        atoms,
        num,
        posi
    )
    # Copy Files
    name="try_%d"%tag
    shutil.rmtree(name,ignore_errors=True)
    os.makedirs(name)
    with open("%s/POSCAR"%name,"w") as posc:
        posc.write(poscar)
    with open("%s/KPOINTS"%name,"w") as kpoi:
        kpoi.write("""Gamma-point only
        1
        rec
        0 0 0 1
        """)
    with open("%s/POTCAR"%name,"w") as potc:
        for i in atoms.split():
            with open("%s/%s/POTCAR"%(potpath,i),"r") as to_read:
                to_copy = to_read.read()
            potc.write(to_copy)
    shutil.copy("INCAR","%s/INCAR"%name)
    os.system("cd %s;%s 1>output"%(name,vasp))
    with open("%s/OUTCAR"%name,"r") as outc:
        src=outc.read()
    # Define Get Single Energy
    def get_single_point(src,pos):
        test=src.find("POSITION",pos)
        if test == -1:
            return None
        starter=src.find("\n",src.find("\n",test)+1)
        ender=src.find("\n -",starter)
        pre_position=src[starter:ender].split()
        position=[]
        for i in range(len(pre_position)/6):
            if i==0:
                pass
            elif i==1:
                position.append(pre_position[i*6+0])
            elif i==2:
                position.append(pre_position[i*6+0])
                position.append(pre_position[i*6+1])
            else:
                position.append(pre_position[i*6+0])
                position.append(pre_position[i*6+1])
                position.append(pre_position[i+8+2])
        position=map(float,position)
        position=map(lambda x:x if x<scale*mul/2 else x-scale*mul,position)
        pre_en=src.find("=",ender)
        en=float(src[pre_en+1:src.find("eV",pre_en)].split()[0])
        return position,en,pre_en
    # Get Energy
    pos=0
    ans=[get_single_point(src,pos)]
    while ans[-1]!=None:
        pos=ans[-1][-1]
        ans.append(get_single_point(src,pos))
    pre_ans = [[i[0],i[1]] for i in ans[:-1]]

    length = len(pre_ans)
    to_return = []
    while length != 0:
        to_return.append(pre_ans[-length])
        length = length/2
    return [[dict(map(lambda x:("x%d"%x,i[0][x-1]), range(1,len(pre_var)+1))),i[1]] for i in to_return]
