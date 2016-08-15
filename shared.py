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
    position=tuple(map(float,position))
    pre_en=src.find("=",ender)
    en=float(src[pre_en+1:src.find("eV",pre_en)].split()[0])
    return position,en,pre_en

def get_all_points(src):
    pos=0
    ans=[get_single_point(src,pos)]
    while ans[-1]!=None:
        pos=ans[-1][-1]
        ans.append(get_single_point(src,pos))
    return [(i[0],i[1]) for i in ans[:-1]]
