# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:45:45 2016

@author: lucas
"""

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
#    root = Tk()
#    root.withdraw()
#    file_names = askopenfilenames(initialdir = '../results')
#    file_names = root.tk.splitlist(file_names)
#    root.destroy()
    file_names = ["/home/lucas/phri/MANIP/results/TESTS/tests_moteurs/RESULTS_scenario_1_trial_1_Alone_02-12-11-40.txt"]

    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Time)
        nyq = 0.5*1000
        low = 10/nyq

        b, a =  sig.butter(2, low, btype = 'low')

#        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
#        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
#        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
#        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
#        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)
        lp = 0.07
        dp = 0.1
        de = 0.008
        pos_ang = [0]*N
        vit_ang = [0]*N
        acc_ang = [0]*N
        acc_ang_test = [0]*N
        couple_mot = [0]*N
        time = [0]*N
        M = numpy.mean(DataClass.Subj_pos2)
        M2 = numpy.mean(DataClass.Subj_for2)
        
        for i in range(0,N):
            couple_mot[i] = -DataClass.Subj_for2[i]*9.81*lp*de/dp*1100
            pos_ang[i] = DataClass.Paddle_pos2[i]
            time[i] = DataClass.Time[i]
        
        for i in range(4,N-4):
            vit_ang[i] = (1./280*pos_ang[i-4] - 4./105* pos_ang[i-3] + 1./5*pos_ang[i-2] - 4./5*pos_ang[i-1] + 4./5*pos_ang[i+1] - 1./5*pos_ang[i+2] + 4./105* pos_ang[i+3] -1./280*pos_ang[i+4])/(time[i] - time[i-1])
        vit_ang = sig.lfilter(b, a, vit_ang)    
        for i in range(4,N-4):   
            acc_ang[i] = (1./280*vit_ang[i-4] - 4./105* vit_ang[i-3] + 1./5*vit_ang[i-2] - 4./5*vit_ang[i-1] + 4./5*vit_ang[i+1] - 1./5*vit_ang[i+2] + 4./105* vit_ang[i+3] -1./280*vit_ang[i+4])/(time[i] - time[i-1])
            acc_ang_test[i] = (-1./560*pos_ang[i-4] + 8./315* pos_ang[i-3] - 1./5*pos_ang[i-2] + 8./5*pos_ang[i-1] - 205./72*pos_ang[i] + 8./5*pos_ang[i+1] - 1./5*pos_ang[i+2] + 8./315* pos_ang[i+3] -1./560*pos_ang[i+4])/((time[i] - time[i-1])**2)
        acc_ang = sig.lfilter(b, a, acc_ang)   
        acc_ang_test = sig.lfilter(b, a, acc_ang_test)   
          
        ax1 = host_subplot(111)
#        ax1.set_ylim(-2, 2)
        ax1.set_xlim(0, DataClass.Time[N-1])

#        ax1.plot(time, DataClass.Subj_for2)
#        ax1.plot(time, DataClass.Subj_pos2)
        ax1.plot(time, pos_ang, 'b')
#        ax1.plot(time, vit_ang, 'c')
        ax1.plot(time, acc_ang, 'g')
        ax1.plot(time, acc_ang_test, 'm')
        ax1.plot(time, couple_mot, 'r')
        ax1.plot(time, [0]*N, 'k')
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