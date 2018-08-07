#!/usr/bin/env python

#Code written by Lucas Roche
#March 2016

import random
import socket
import threading
import time

UDP_PORT1 = 5005
UDP_PORT2 = 5006
UDP_PORT3 = 5007
UDP_PORT4 = 5008
UDP_IP = "192.168.7.1"



sock1 = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP

sock2 = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP

sock3 = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP

sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock1.bind((UDP_IP, UDP_PORT1))
sock1.close()

sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.bind((UDP_IP, UDP_PORT2))
sock2.close()

sock3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock3.bind((UDP_IP, UDP_PORT3))
sock3.close()

sock4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock4.bind((UDP_IP, UDP_PORT4))
sock4.close()
