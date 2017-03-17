#!/usr/bin/env python

import sys
import socket

prefix = sys.argv[1]
port   = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', port))
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
        with open("output","a") as f:
            f.write("%s\n"%t)
    sock.close()


