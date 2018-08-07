
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 27 17:50:56 2017

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
    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Time)

        #Create parameters for Butterworth filter (Low-pass, 6th Order)
        nyq = 0.5*5000
        low = 10/nyq
   
        b, a =  sig.butter(6, low, btype = 'low')
        b2, a2 = sig.butter(6, 100/nyq, btype = 'low')

    
    #        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
    #        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
    #        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
    #        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
    #        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)
  
        t0 = 0#int(2/DataClass.Time[N-1]*N)
        tf = N-2#int(25/DataClass.Time[N-1]*N)
    #Applying Butterworth filer to force signals        
        for1 = sig.lfilter(b, a, DataClass.Subj_for1)
        for2 = sig.lfilter(b, a, DataClass.Subj_for2)  
    

        dom1 = [0]*N        
        for i in range(0,N):
            if(sign(for1[i])==sign(for2[i])):
                f1_i = 0
            elif(abs(for1[i]) <= abs(for2[i])):
                f1_i = for1[i]
            else:
                f1_i = -for2[i]
            f1_e = for1[i] - f1_i
            dom1[i]=f1_e/(for1[i]+for2[i])
        
        pos = [[],[]]
        pos[0] = sig.lfilter(b2, a2, DataClass.Subj_pos1)
        pos[1] = sig.lfilter(b2, a2, DataClass.Subj_pos2)
        posC = sig.lfilter(b2, a2, DataClass.Curs_pos)
        vit = [[],[]]
        vit[0] = [0]*N
        vit[1] = [0]*N
        vitC = [0]*N
        for i in range(4,N-4):
            vit[0][i] = 1./280*pos[0][i-4] - 4./105*pos[0][i-3] + 1./5*pos[0][i-2] - 4./5*pos[0][i-1] + 4./5*pos[0][i+1] - 1./5*pos[0][i+2] + 4./105*pos[0][i+3] - 1./280*pos[0][i+4]
            vit[1][i] = 1./280*pos[1][i-4] - 4./105*pos[1][i-3] + 1./5*pos[1][i-2] - 4./5*pos[1][i-1] + 4./5*pos[1][i+1] - 1./5*pos[1][i+2] + 4./105*pos[1][i+3] - 1./280*pos[1][i+4]
#            if cond == 'HFOP' or cond == 'HFO':
#                vitC[i] = 1./280*posC[i-4] - 4./105*posC[i-3] + 1./5*posC[i-2] - 4./5*posC[i-1] + 4./5*posC[i+1] - 1./5*posC[i+2] + 4./105*posC[i+3] - 1./280*posC[i+4]

            
#        c_dom1 = [0]*N
#        for i in range(0, N):
#            if DataClass.Path_pos1[i] == DataClass.Path_pos2[i]:
#                c_dom1[i] = 0.5
#            else:
#                c_dom1[i] = min(1, max(0, (DataClass.Curs_pos[i] - DataClass.Path_pos2[i])/(DataClass.Path_pos1[i] - DataClass.Path_pos2[i])))

    #Plotting results
        fig = plt.figure(1)
        ax1 = plt.subplot(111)
#        ax2 = ax1.twiny()
#        ax3 = ax1.twiny()
        ax1.set_ylabel('Time (s)')
        ax1.set_xlabel('Position (deg)')
#        ax2.set_xlabel('Force (N)')
        ax1.axis([ -100, 800, DataClass.Time[t0], DataClass.Time[tf-1]])
#        ax2.axis([ -2.5, 2.5, DataClass.Time[t0], DataClass.Time[tf-1]])
#        ax3.axis([ -0.5, 1.5, DataClass.Time[t0], DataClass.Time[tf-1]])
    

#        ax1.plot(DataClass.Path_pos1[t0:tf], DataClass.Time[t0:tf], 'k')
#        ax1.plot(DataClass.Path_pos2[t0:tf], DataClass.Time[t0:tf], 'k--')

       
        try:
            ax1.plot(DataClass.Curs_pos1[t0:tf], DataClass.Time[t0:tf],'b')
            ax1.plot(DataClass.Curs_pos2[t0:tf], DataClass.Time[t0:tf],'g')
        except:
            ax1.plot(DataClass.Curs_pos[t0:tf], DataClass.Time[t0:tf],'r')

#        p_pos1, = ax1.plot(DataClass.Subj_pos1[t0:tf], DataClass.Time[t0:tf],'b')
#        p_pos2, = ax1.plot(DataClass.Subj_pos2[t0:tf], DataClass.Time[t0:tf],'g')
#        p_for1, = ax2.plot([-x for x in for1], DataClass.Time[t0:tf],'c')
#        p_for2, = ax2.plot([-x for x in for2], DataClass.Time[t0:tf],'m')
#        p_dom1, = ax3.plot(dom1[t0:tf], DataClass.Time[t0:tf],'green')
#        p_cdom1, = ax3.plot(c_dom1[t0:tf], DataClass.Time[t0:tf],'blue')

#        p_vit1 = ax2.plot(vit[0][t0:tf], DataClass.Time[t0:tf],'c') 
#        p_vit2 = ax2.plot(vit[1][t0:tf], DataClass.Time[t0:tf],'m')

#        print len(DataClass.Consigne1), len(DataClass.Subj_for1), len(DataClass.Time)
#        fig = plt.figure(2)
#        ax1 = plt.subplot(111)
##        ax2 = ax1.twiny()
#        ax1.set_ylabel('Time (s)')
#        ax1.set_xlabel('Position (mm)')
##        ax2.set_xlabel('Force (N)')
##        p_posd, = ax1.plot([(DataClass.Subj_pos1[i] - DataClass.Subj_pos2[i])*0.08 for i in range(0,N)], DataClass.Time[t0:tf],'b')
##        p_ifor, = ax2.plot([-for1[i]/((DataClass.Subj_pos1[i] - DataClass.Subj_pos2[i])*0.08) for i in range(0,N)], DataClass.Time[t0:tf],'r')

#
#        p_cons, = ax1.plot([-(x - 4970)*10/(0.8*10000/2)*0.123/0.082 for x in DataClass.Consigne1[t0:tf]], DataClass.Time[t0:tf],'r')
#        p_for1, = ax1.plot([-x for x in DataClass.Subj_for1[t0:tf]], DataClass.Time[t0:tf],'b')        

        
#        test, = ax2.plot([abs(x) + abs(y) for x, y in zip(for1,for2)], DataClass.Time[t0:tf],'g')
#        test1, = ax2.plot([abs(x) for x in for1], DataClass.Time[t0:tf],'b')
#        test2, = ax2.plot([-abs(x) for x in for2], DataClass.Time[t0:tf],'r')

        
        #p_diff_pos, = ax1.plot(DataClass.Time[t0:tf], diff_pos[t0:tf], 'r')
#        plt.plot(DataClass.Time, int1, 'b-')
#        plt.plot(DataClass.Time, int2, 'g-')
        
        

#        legendHandles = [p_pos1, p_pos2, p_for1, p_for2, p_diff_pos]
#        legendLabels = ["Position 1", "-Position 2", "Force 1", "Force 2", "Position error"]
        
#        fig.legend(legendHandles, legendLabels, loc='upper left') 
        
        plt.show(block='False')

#            

        

def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1
           

if __name__ == '__main__':
    main()