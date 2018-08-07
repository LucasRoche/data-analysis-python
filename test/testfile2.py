# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:12:29 2015

@author: Lucas
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
import scipy.signal as sig

N=50000
#A = np.random.rand(N)*2 -1
#B = np.random.randn(N)
#
#IA = [0]*N
#IB = [0]*N
nyq = 0.5*5000
b2, a2 = sig.butter(6, 10/nyq, btype = 'low')
#for i in range (1,N):
#    IA[i] = IA[i-1] + A[i]
#    IB[i] = IB[i-1] + B[i]
#    
#IA = sig.lfilter(b2, a2, IA)
#IB = sig.lfilter(b2, a2, IB)
#    

A = [(np.random.rand(1)*2-1 + i*0) for i in range(0,N)]
B = [(np.random.randn(1) + i*0) for i in range(0,N)]
t = [i/5000.0 for i in range(0,N)]
fc = 1
T = 1./5000
alpha = T/(1/(2*3.14*fc)+T)

IA = sig.lfilter(b2, a2, A)
IB = sig.lfilter(b2, a2, B)
for i in range(1,N):
    A[i] = alpha*A[i] + (1-alpha)*A[i-1]
    B[i] = alpha*B[i] + (1-alpha)*B[i-1]
    



plt.plot(t, A, 'b')
plt.plot(t, B, 'g')
#plt.plot(sig.lfilter(b2, a2, A), 'c')
#plt.plot(sig.lfilter(b2, a2, B), 'm')
plt.plot(t, IA, 'c')
plt.plot(t, IB, 'm')
plt.show()