#%!/usr/bin/env python
#

import os
import shutil

class find_me_parser():
    def get_poscar(self):
        with open(os.path.join(self.prefix,"POSCAR"),"r") as pos_file:
            self.pos=pos_file.read()
        start=self.pos.find("{{")
        end=self.pos.find("}}")
        self.control=self.pos[start+2:end].split()
        self.to_replace=self.pos[:start]
    def set_param(self):
        temp = ""
        for i in self.control:
            if i!="vars":
                if temp == "":
                    temp = i
                else:
                    if "." in i:
                        var = float(i)
                    else:
                        var = int(i)
                    setattr(self,temp,var)
                    temp = ""
            else:
                break
    def count_dim(self):
        self.dim = sum(map(int,self.to_replace.split("\n")[-3].split()))
    def __init__(self,prefix):
        self.prefix = prefix
        self.get_poscar()
        self.set_param()
        self.count_dim()
    def get_energy_vasp(self,var,tag):
        this_name=os.path.join(self.prefix,"try_%s"%tag)
        self.copy_data(this_name,var)
        os.system("cd %s;vasp_without_mpi 1>output"%this_name)
        ans = self.analyze(os.path.join(this_name,"OUTCAR"))
        return ans
    def copy_data(self,this_name,var):
        shutil.rmtree(this_name,ignore_errors=True)
        os.makedirs(this_name)
        shutil.copy(os.path.join(self.prefix,"INCAR"),os.path.join(this_name,"INCAR"))
        shutil.copy(os.path.join(self.prefix,"POTCAR"),os.path.join(this_name,"POTCAR"))
        shutil.copy(os.path.join(self.prefix,"KPOINTS"),os.path.join(this_name,"KPOINT"))
        with open(os.path.join(this_name,"POSCAR"),"w") as this_pos_file:
            this_pos_file.write(self.get_this_pos(var))
    def get_this_pos(self,var):
        this_pos=self.to_replace
        for i in range(self.dim):
            this_pos += "%%.%(p)df %%.%(p)df %%.%(p)df\n"%{"p":self.precision}%(
                    var[i*self.dim+0],
                    var[i*self.dim+1],
                    var[i*self.dim+2])
        return this_pos
    def analyze(self,file_name):
        with open(file_name,"r") as to_ana_file:
            to_ana=to_ana_file.read()
            temp=to_ana.find("TOTEN",0)
            offset=0
            while(temp!=-1):
                 offset=temp+1
                 temp=to_ana.find("TOTEN",offset)
            if offset!=0:
                data=float(to_ana[to_ana.find("=",offset)+1:                        \
                    to_ana.find("eV",offset)].strip())
            else:
                data="2147483647"
        return float(data)
    get_energy=get_energy_vasp
