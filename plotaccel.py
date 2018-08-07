# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:28:48 2015

@author: Lucas
"""

from postTrait_Module import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import scipy.signal as sig
import numpy
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '../results')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    

    for file in file_names:
        if file.find('_a_') == -1:
            continue
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Curs_pos)
        nyq = 0.5*2000
        low = 10/nyq
#        low1 = 5/nyq
#        low2 = 1/nyq
        b, a =  sig.butter(3, low, btype = 'low')
#        c, d =  sig.butter(3, low1, btype = 'low')
#        e, f =  sig.butter(3, low2, btype = 'low')

#        curs_pos_filtered1 = [0]*len(DataClass.Curs_pos)
#        curs_pos_filtered2 = [0]*len(DataClass.Curs_pos)
#        curs_pos_filtered1 = sig.lfilter(c, d, DataClass.Curs_pos)
#        curs_pos_filtered2 = sig.lfilter(e, f, DataClass.Curs_pos)

        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)
        
        for i in range(0,N):
            if DataClass.Path_pos1[i] >= 5000:
                DataClass.Path_pos1[i] = 0.
            if DataClass.Path_pos2[i] >= 5000:
                DataClass.Path_pos2[i] = 0.


        d_curs_pos = [0]*N
        d2_curs_pos = [0]*N
        sign_for = [0]*N
        sign_d_curs =[0]*N
        sign_d2_curs = [0]*N
        executorship = [0]*N
        conductorship = [0]*N
        
        for i in range(1, N-1):
            d_curs_pos[i] = (-0.5*DataClass.Curs_pos[i-1]+0.5*DataClass.Curs_pos[i+1])/(DataClass.Time[i+1] - DataClass.Time[i-1])
        d_curs_pos = sig.lfilter(b,a, d_curs_pos)  
        
        for i in range(1, N-1):
            d2_curs_pos[i] = (-0.5*d_curs_pos[i-1]+0.5*d_curs_pos[i+1])/(DataClass.Time[i+1] - DataClass.Time[i-1])
        d2_curs_pos = sig.lfilter(b,a, d2_curs_pos)              

        for i in range(0, N):
            sign_for[i] = sign((DataClass.Subj_for1[i] - DataClass.Subj_for2[i])/2)
        for i in range(0, N):
            sign_d_curs[i] = sign(d_curs_pos[i])
        for i in range(0, N):
            sign_d2_curs[i] = sign(d2_curs_pos[i])
            
        for i in range(0, N):
            executorship[i], conductorship[i] = Stefanov(sign_for[i], sign_d_curs[i], sign_d2_curs[i])

        for i in range(0,N):
            executorship[i] *= 100
            conductorship[i] *= 100            

        ax1 = host_subplot(111)
        ax1.set_xlim(-200, 200)
        ax1.set_ylim(0, DataClass.Time[N-1])

#        ax1.plot(d_curs_pos, DataClass.Time, 'm')
#        ax1.plot(DataClass.Subj_for1 , DataClass.Time, 'c')
#        ax1.plot(DataClass.Subj_for2 , DataClass.Time, 'm')
#        ax1.plot((DataClass.Subj_for1 - DataClass.Subj_for2)/2, DataClass.Time, 'y')
#        plt.plot(d2_curs_pos, DataClass.Time, 'c')

#        ax1.plot(sign_for, DataClass.Time)
#        ax1.plot(sign_d_curs, DataClass.Time)
#        ax1.plot(sign_d2_curs, DataClass.Time)


        lowStef = 0.5/nyq
        c, d =  sig.butter(3, lowStef, btype = 'low')
        executorship = sig.lfilter(c,d,executorship)
        conductorship = sig.lfilter(c,d,conductorship)
#        executorship = filtreBourrin(executorship)
#        conductorship = filtreBourrin(conductorship)

        ax1.plot(DataClass.Path_pos1, DataClass.Time, 'b')
        ax1.plot(DataClass.Path_pos2, DataClass.Time, 'g')
        ax1.plot(DataClass.Curs_pos, DataClass.Time, 'r')
        ax1.plot(executorship, DataClass.Time, 'c')
        ax1.plot(conductorship, DataClass.Time, 'm')
        plt.show(block='False')
        
        print numpy.mean(DataClass.Path_pos1[10000:N-10000]), numpy.mean(DataClass.Path_pos2[10000:N-10000]), numpy.mean(DataClass.Curs_pos[10000:N-10000])
        print numpy.mean(executorship), numpy.mean(conductorship)


def filtreBourrin(Array):
    M=100
    Array_filtered = [0]*len(Array)
    for i in range(0,len(Array)):
        if i<M:
            for j in range (0,i):
                Array_filtered[i] += Array[j]
        else:
            for j in range (i-M,i):
                Array_filtered[i] += Array[j]         
        Array_filtered[i] /= min(i+1, M)
    return Array_filtered


def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1

def Stefanov(fi, dx, d2x):
    if fi<0:
        if dx<0:
            if d2x<0:
                return -1,-1
            elif d2x==0:
                return -1, 0
            else:
                return -1, 1
        elif dx == 0:
            if d2x<0:
                return 0,-1
            elif d2x==0:
                return 0, 0
            else:
                return 0, 1            
        else:
            if d2x<0:
                return 1,-1
            elif d2x==0:
                return 1, 0
            else:
                return 1, 1
    elif fi>0:
        if dx<0:
            if d2x<0:
                return 1, 1
            elif d2x==0:
                return 1, 0
            else:
                return 1, -1
        elif dx == 0:
            if d2x<0:
                return 0, 1
            elif d2x==0:
                return 0, 0
            else:
                return 0, -1          
        else:
            if d2x<0:
                return -1, 1
            elif d2x==0:
                return -1, 0
            else:
                return -1, -1
    else:
        return 0, 0
                
                
if __name__ == '__main__':
    main()