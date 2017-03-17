#!/usr/bin/env pyhton

import sys
import random
import socket
import mpi4py.MPI as MPI
from shared import find_me_parser

addr = sys.argv[1]
port = int(sys.argv[2])

def ask(name):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr,port))
        s.send(name)
        d = s.recv(1024)
        s.close()
        return d
    except:
        exit()

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

runner = find_me_parser(ask("prefix"))

while True:
    tag = ask("goon")
    S = [random.random()*(runner.sym_region[j][1]-runner.sym_region[j][0])+
        runner.sym_region[j][0] for j in range(runner.dim)]
    SE = runner.get_energy(S,tag)
    ask(repr((S,SE)))
