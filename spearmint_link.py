#!/usr/bin/env python

from shared import get_energy

def main(id,param):
    return get_energy([param["a"],param["b"],param["c"]],0,id)
