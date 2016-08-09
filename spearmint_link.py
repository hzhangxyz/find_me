#!/usr/bin/env python

from shared import get_energy,sym_table,dim

def main(id,param):
    print param
    return get_energy([param[sym_table[i]] for i in range(dim)],0,id)
