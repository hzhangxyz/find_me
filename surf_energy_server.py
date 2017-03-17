#!/usr/bin/env python

import os
import sys
import socket

prefix = os.curdir if len(sys.argv)==1 else sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(1024)

i = 0
while True:
    sock, addr = s.accept()
    t = sock.recv(1024)
    if "prefix" in t:
        sock.send(prefix)
    elif "goon" in t:
        sock.send(repr(i))
        i += 1
    else:
        sock.send("T")
        print t
    sock.close()


