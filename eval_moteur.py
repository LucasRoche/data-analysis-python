# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:48:16 2016

@author: lucas
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
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Time)
        nyq = 0.5*2000
        low = 10/nyq

        b, a =  sig.butter(3, low, btype = 'low')

#        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
#        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
#        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
#        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
#        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)

        int1 = [0]*N
        test = [0]*N
        test2 = [0]*N
        test3 = [0]*N
        int1opp = [0]*N
        M = numpy.mean(DataClass.Subj_pos1)
        M2 = numpy.mean(DataClass.Subj_for1)
        
        for i in range(0,N):
            int1[i] = (DataClass.Consigne1[i]/1000000 - 0.5)*1/0.4
            if int1[i]==0:
                print DataClass.Consigne1[i], int1[i]
                int1[i] = 0.001
            test3[i] = DataClass.Subj_for1[i] #- M2
            #test[i] = DataClass.Subj_for1[i]/int1[i]
            test[i] = test3[i]/int1[i]
            test2[i] = -(DataClass.Subj_pos1[i] - M )*DataClass.SENSITIVITY/DataClass.WINDOW_WIDTH*10*5
            int1opp[i] = -int1[i]
            
          
        print numpy.mean(test), numpy.std(test), numpy.std(test)/sqrt(N), numpy.mean(DataClass.Subj_for1)
          
        ax1 = host_subplot(111)
        ax1.set_ylim(-2, 2)
        ax1.set_xlim(0, DataClass.Time[N-1])


        ax1.plot( DataClass.Time, test3,'b')
        ax1.plot( DataClass.Time, int1opp,'c')
        ax1.plot(DataClass.Time,test,  'r')
        ax1.plot(DataClass.Time, [0]*N, 'k')
        ax1.plot(DataClass.Time, test2, 'm')
        plt.show(block='False')
        




def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1


                
if __name__ == '__main__':
    main()