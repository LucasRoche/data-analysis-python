#!/usr/bin/env python

#Code written by Lucas Roche
#March 2016

import random
import socket
import threading
import time
import math

UDP_PORT1 = 5005
UDP_PORT2 = 5006
UDP_PORT3 = 5007
UDP_PORT4 = 5008
UDP_IP = "192.168.7.2"





sock1 = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP


                  
#sock1.bind((UDP_IP, UDP_PORT1))
#sock2.bind((UDP_IP, UDP_PORT2))

#sock3 = socket.socket(socket.AF_INET, # Internet
#                  socket.SOCK_DGRAM) # UDP
#sock3.bind((UDP_IP, UDP_PORT3))
#
#sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock4.bind((UDP_IP, UDP_PORT4))




mess1 = "testestesteste\n"

sock1.sendto(mess1, (UDP_IP, UDP_PORT3))
    
print "lalala"

    

    


#while True:
#    #Read socket to get info about cursor
#    data1, addr = sock1.recvfrom(1024)
#    #data1 = float(data1[0:data1.find("\n")])
#
#    data2, addr = sock2.recvfrom(1024)
#    #data2 = float(data2[0:data2.find("\n")])
#
#    data3, addr = sock3.recvfrom(1024)
#    #data3 = float(data3[0:data1.find("\n")])
#
#    data4, addr = sock4.recvfrom(1024)
#    #data4 = float(data4[0:data2.find("\n")])
#    
#    print data1, data2, data3, data4
    



