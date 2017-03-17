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
    S = [2*(random.random()-0.5)*runner.max for j in range(3*runner.dim)]
    SE = runner.get_energy(S,tag)
    ask(repr((S,SE)))
