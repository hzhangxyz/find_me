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
    def parse_sym(self):
        raw_sym_table = self.control[self.control.index("vars")+1:]
        self.dim = len(raw_sym_table)/3
        self.sym_table=[raw_sym_table[3*i] for i in range(self.dim)]
        self.sym_region=[[float(raw_sym_table[3*i+1]),
            float(raw_sym_table[3*i+2])] for i in range(self.dim)]
    def __init__(self,prefix):
        self.prefix = prefix
        self.get_poscar()
        self.set_param()
        self.parse_sym()
    def get_energy_vasp(self,var,tag1,tag2):
        this_name="try_%d_%d"%(tag1,tag2)
        this_pos=self.to_replace
        while this_pos.find("{")!=-1:
            starter=this_pos.find("{")
            ender=this_pos.find("}")
            to_calc=this_pos[starter+1:ender]
            for i in range(self.dim):
                to_calc=to_calc.replace("(%s)"%self.sym_table[i],
                    "(%%.%df)"%self.precision%var[i])
            calc_res="%%.%df"%self.precision%eval(to_calc)
            this_pos="%s%s%s"%(this_pos[:starter],calc_res,this_pos[ender+1:])
        shutil.rmtree(this_name,ignore_errors=True)
        os.makedirs(this_name)
        shutil.copy(os.path.join(self.prefix,"INCAR"),os.path.join(self.prefix,this_name,"INCAR"))
        shutil.copy(os.path.join(self.prefix,"POTCAR"),os.path.join(self.prefix,this_name,"POTCAR"))
        shutil.copy(os.path.join(self.prefox,"KPOINTS"),os.path.join(self.prefix,this_name,"KPOINT"))
        with open(os.path.join(self.prefix,this_name,"POSCAR"),"w") as this_pos_file:
            this_pos_file.write(this_pos)
        os.system("cd %s;vasp_without_mpi 1>output"%os.path.join(self.prefix,this_name))
        with open(os.path.join(self.prefix,this_name,"OUTCAR"),"r") as to_ana_file:
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
