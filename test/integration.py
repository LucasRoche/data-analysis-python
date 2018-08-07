# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:48:05 2017

@author: lucas
"""

import matplotlib.pyplot as plt
import numpy as np

total_time = 100
F = 0
M = 1
C = 1
K = 10
x = 10
X0r = -5
d2x=0
dx=0
T=0.01
N = int(total_time/T)
X = [x]*N
time = [0]*N
Q0 = T**2/(4*M + 2*C*T + K*T**2)
Q1 = -2*K + 8*M/T**2
Q2 = (2*C/T - 4*M/T**2 - K)
Q3 = 1
for i in range(2,N):
#    d2x = F
#    dx += d2x*T
#    x += dx*T
    x = Q0*(Q1*X[i-1] + Q2*X[i-2] + Q3*(4*F + 4*K*X0r))
    X[i] = x
    time[i] = T*i

    #print d2x, dx, x, 10+0.5*F*total_time**2

plt.plot(time, X)