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
sock1.bind((UDP_IP, UDP_PORT3))




while True:
    #Read socket to get info about cursor
    data1, addr = sock1.recvfrom(1024)
    #data1 = float(data1[0:data1.find("\n")])


    #data2 = float(data2[0:data2.find("\n")])
    
    print data1
    



