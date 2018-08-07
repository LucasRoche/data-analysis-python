# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 13:53:12 2017

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
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip/TESTS/transparence3/')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Time)
        nyq = 0.5*1000
        low = 10/nyq
    
        b, a =  sig.butter(6, low, btype = 'low')
        b2, a2 = sig.butter(6, 100/nyq, btype = 'low')
    
        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
    #        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
    #        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
    #        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)
    
        int1 = [0]*N
        int2 = [0]*N
        for1 = [0]*N
        for2 = [0]*N
        pos1 = [0]*N
        pos2 = [0]*N
        temp = [0]*N
        diff_pos = [0]*N
        diff_for = [0]*N
        vit1 = [0]*N
        vit2 = [0]*N
        time = [0]*N
        cons_pos1 = [0]*N
        cons_for1 = [0]*N
        deltaPos1 = [0]*N
        deltaFor1 = [0]*N
        deltaPos2 = [0]*N
        deltaFor2 = [0]*N
        Ke = [0]*N
        int1opp = [0]*N
        M = numpy.mean(DataClass.Subj_pos1)
        M2 = numpy.mean(DataClass.Subj_for1)
        
        filterCoef = (0.001/(1/(2*3.14*5) + 0.001))
        
        for i in range(0,N):
            time[i] = DataClass.Time[i]
            int1[i] = (DataClass.Consigne1[i]/1000000 - 0.5)*1/0.4*10
            int2[i] = (DataClass.Consigne2[i]/1000000 - 0.5)*1/0.4*10
            if int1[i]==0:
                #print DataClass.Consigne1[i], int1[i]
                int1[i] = 0.001
            for1[i] = DataClass.Subj_for1[i] #- M2
            for2[i] = DataClass.Subj_for2[i] #- M2
            pos1[i] = -(DataClass.Subj_pos1[i])*DataClass.SENSITIVITY/DataClass.WINDOW_WIDTH*10*360
            pos2[i] = -(DataClass.Subj_pos2[i])*DataClass.SENSITIVITY/DataClass.WINDOW_WIDTH*10*360
            diff_pos[i] = pos1[i]-pos2[i]
            diff_for[i] = for1[i] + for2[i]
            temp[i] = filterCoef*pos2[i] + (1-filterCoef)*pos2[i-1]
        for i in range(4,N-4):
            if (time[i] - time[i-1])!=0:
                diff_t = time[i] - time[i-1] 
            vit1[i] = (1./280*pos1[i-4] - 4./105* pos1[i-3] + 1./5*pos1[i-2] - 4./5*pos1[i-1] + 4./5*pos1[i+1] - 1./5*pos1[i+2] + 4./105* pos1[i+3] -1./280*pos1[i+4])/(diff_t)
            vit2[i] = (1./280*pos2[i-4] - 4./105* pos2[i-3] + 1./5*pos2[i-2] - 4./5*pos2[i-1] + 4./5*pos2[i+1] - 1./5*pos2[i+2] + 4./105* pos2[i+3] -1./280*pos2[i+4])/(diff_t)
            vit2[i] = (1./280*temp[i-4] - 4./105* temp[i-3] + 1./5*temp[i-2] - 4./5*temp[i-1] + 4./5*temp[i+1] - 1./5*temp[i+2] + 4./105* temp[i+3] -1./280*temp[i+4])/(diff_t)
#            vit2[i] = (filterCoef)*vit2[i] + (1-filterCoef)*vit2[i-1]
        vit1 = sig.lfilter(b, a, vit1)
        vit2 = sig.lfilter(b, a, vit2)
        
        indices1 = []
        indices2 =  []
        test = [0]*N
        for1_filt = [0]*N
        test1 = [0]*N
        test2 = [0]*N
        test3 = [0]*N
        int_for = [0]*N
        stiffness = [0]*N
        for i in range (0,N):
            if for1[i] != for1[i-1]:
                indices1.append(i)
            if for2[i] != for2[i-1]:
                indices2.append(i)
        for i in range(0,N):
            test[i] = for2[i]
                
        for j in range (2, len(indices1)):
            for k in range(indices1[j-1], indices1[j]+1):
#                print k, indices1[j-1], indices1[j]
                for1[k] = (for1[indices1[j]] - for1[indices1[j-1]])/(time[indices1[j]] - time[indices1[j-1]])*(time[k] - time[indices1[j-1]]) + for1[indices1[j-1]]
#                test2[k] = (for1[indices1[j-1]] - for1[indices1[j-2]])/(time[indices1[j-1]] - time[indices1[j-2]])*(time[k] - time[indices1[j-1]]) + for1[indices1[j-1]]
#                test[k] = (for1[indices1[j-1]] - for1[indices1[j-2]])/(time[indices1[j-1]] - time[indices1[j-2]])/2*(time[k] - time[indices1[j-1]]) + for1[indices1[j-1]]
        for j in range (2, len(indices2)):
            for k in range(indices2[j-1], indices2[j]+1):
#                print k, indices2[j-1], indices2[j]
                for2[k] = (for2[indices2[j]] - for2[indices2[j-1]])/(time[indices2[j]] - time[indices2[j-1]])*(time[k] - time[indices2[j-1]]) + for2[indices2[j-1]]
#                

        for i in range(0,N):
            int_for[i] = for1[i] - for2[i]
            if abs(diff_pos[i]) < 0.001:
                stiffness[i] = 0
            else:
                stiffness[i] = abs(int_for[i])/(abs(diff_pos[i])/360*2*3.14*0.08 )
   
    ###############################################################################################################
    #Online impedance estimator
    #####################################################       
        
        K= [0]*N
        F = [0]*N
        for i in range(0,N):
            if i<N/3:
                K[i] = 10
            elif (i>N/3 and i < 2*N/3):
                K[i] = 100
            else:
                K[i] = 50
        L = numpy.random.rand(N,1)
        for i in range(0,N):
            F[i] = L[i]*K[i] + numpy.random.randn()


    
        X = 0
        W = [0]*N
        alpha = 0
        G = 0
        P = 1
        lbd = 0.99
        gamma = 0.5/(3*25)
        for i in range(150, N):
            X = abs(diff_pos[i])/360*2*3.14*0.08
            alpha = abs(diff_for[i]) - X*W[i-1]
            G = P*X/(lbd + X*P*X)
            P = 1/lbd*(P - G*X*P) + round(gamma*alpha**2)
            W[i] = W[i-1] + alpha*G
            
        plt.figure(0)
        plt.plot(W)
         
#        ax1 = host_subplot(111)
    #    ax1.set_ylim(-10, 10)
    #    ax1.set_xlim(0, DataClass.Time[N-1])
        
    #    ax1.plot(time, pos1,'c-')
    #    ax1.plot(time, pos2,'m-')
    #    ax1.plot(time, for1, 'b--')
    #    ax1.plot(time, for2, 'g--')
    #    #ax1.plot(time, int1, 'b-')
    #    #ax1.plot(time, int2, 'g-')
    #    ax1.plot(time, diff_pos, 'r-')
    #    #ax1.plot(time, cons_pos1, 'c-')
    #    #ax1.plot(time, cons_for1, 'm-')
    #    ax1.plot(time, [0]*N, 'k-')
        #ax1.plot(time, Ke, 'm-')
#        plt.figure(1)
#        plt.subplot(311)
#        plt.plot([0]*N, 'k')
#        plt.plot(Ke[150:N])
#        plt.plot(W[150:N])
#        
#        plt.subplot(312)
#        plt.plot([0]*N, 'k')
#        plt.plot(deltaPos2[150:N])
#        plt.plot([-i for i in deltaFor2[150:N]])
#        
#        plt.subplot(313)
#        plt.plot([0]*N, 'k')
#        plt.plot(pos2[150:N])
#        plt.plot(for2[150:N])
#        plt.plot(vit2[150:N])
        #plt.plot(diff_pos[150:N])
        t0 = int(9.2/time[N-1]*N)
        tf = int(11.8/time[N-1]*N)   
        
        print "Mean position error : ", numpy.mean([abs(x) for x in diff_pos[t0:tf]]), numpy.mean([abs(x) for x in diff_pos[t0:tf]])*3.1415/180*0.08
        print "Mean force error : ", numpy.mean([abs(x) for x in diff_for[t0:tf]])
        print "Mean relative force error : ", numpy.mean([abs(diff_for[i])/max(abs(for1[i]), abs(for2[i])) if min(abs(for1[i]), abs(for2[i])) > 0.5 else 0  for i in range(t0,tf)])
        

        fig = plt.figure(1)
        ax1 = plt.subplot(111)
        ax2 = ax1.twinx()
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Position (deg)')
        ax2.set_ylabel('Force (N)')
#        ax3 = ax1.twinx()
        ax1.axis([time[t0], time[tf-1], -2, 14])
        ax2.axis([time[t0], time[tf-1], -2, 14])
#        ax3.axis([time[t0], time[tf-1], 0, 100000])
        ax1.plot(time[t0:tf], [0]*(tf-t0), 'k')
#        p_pos1, = ax1.plot(time[t0:tf], pos1[t0:tf],'b-')
#        p_pos2, = ax1.plot(time[t0:tf], pos2[t0:tf],'g-')
        p_for1, = ax2.plot(time[t0:tf], for1[t0:tf], 'c-')
        p_for2, = ax2.plot(time[t0:tf], [-x for x in for2[t0:tf]], 'm-')
        p_diff_pos, = ax1.plot(time[t0:tf], diff_pos[t0:tf], 'r')
        
#        p_stiff = ax3.plot(time[t0:tf], stiffness[t0:tf], 'orange')
        
#        plt.plot(time, int1, 'b-')
#        plt.plot(time, int2, 'g-')
        legendHandles = [p_for1, p_for2, p_diff_pos]
        legendLabels = ["Force 1", "-Force 2", "Position error"]
        
        fig.legend(legendHandles, legendLabels, loc='upper left') 
        
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