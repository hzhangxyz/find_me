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

def check(S):
    s = [(S[i*3+0],S[i*3+1],S[i*3+2]) for i in range(runner.dim)]
    for i in range(runner.dim):
        for j in range(i):
            if sum(map(lambda x:x*x,(s[i][k]-s[j][k] for k in range(3)))) < runner.min*runner.min:
                return True
    return False

while True:
    S = [2*(random.random()-0.5)*runner.max for i in range(3*runner.dim)]
    if check(S):
        continue
    tag = ask("goon")
    SE = runner.get_energy(S,tag)
    for i in SE:
        ask(repr((S,i)))
