# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:31:02 2017

@author: lucas
"""

from postTrait_Module import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from pylab import *
import scipy.signal
import scipy.io
import numpy as np
from Tkinter import *
from tkFileDialog import *
from spectrum import *
import pylab

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip/TESTS/Tests_freq/')#'/media/NAS/Public/Lucas/OLD_MANIPS/TESTS/tests_freq')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    ij=0
    p1 = [0]*25
    legend_p = []
    legend_n = []
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        N = len(DataClass.Time)
        nyq = 0.5*1000
    
        a = [0]*1501
        b = [0]*1501
        for i in range(1,1501):    
            b[i], a[i] =  sig.butter(2, i/nyq, btype = 'low')

    
    
        int1 = [0]*N
        int2 = [0]*N
        for1 = [0]*N
        for2 = [0]*N
        pos1 = [0]*N
        pos2 = [0]*N
        temp = [0]*N
        diff_pos = [0]*N
        vit1 = [0]*N
        vit2 = [0]*N
        acc1 = [0]*N
        acc2 = [0]*N
        time = [0]*N
        vitp = [0]*N
        vitm = [0]*N
        fcp  = [0]*N
        fcm  = [0]*N
        cm1  = [0]*N
        dt1= 0.0002
        dt = 0.0002
        
        for i in range(0,N):
            time[i] = DataClass.Time[i]
            int1[i] = -(DataClass.Consigne1[i] - 4970)*10/(0.8*10000/2)
            int2[i] = -(DataClass.Consigne2[i] - 4970)*10/(0.8*10000/2)
            cm1[i] = int1[i]*0.123
#            if int1[i]==0:
#                #print DataClass.Consigne1[i], int1[i]
#                int1[i] = 0.001
            for1[i] = DataClass.Subj_for1[i] #- M2
            for2[i] = DataClass.Subj_for2[i] #- M2
            pos1[i] = -(DataClass.Subj_pos1[i])*DataClass.SENSITIVITY/DataClass.WINDOW_WIDTH*10*2*3.14
            pos2[i] = -(DataClass.Subj_pos2[i])*DataClass.SENSITIVITY/DataClass.WINDOW_WIDTH*10*2*3.14
            temp[i] = pos1[i]
            diff_pos[i] = pos1[i]-pos2[i]
#        pos1 = sig.lfilter(b[100], a[100], pos1)

        for i in range(4,N-4):
            dt1 = dt
            dt = (time[i] - time[i-1])
            if dt == 0:
                dt = dt1
            try:
                vit1[i] = (1./280*pos1[i-4] - 4./105* pos1[i-3] + 1./5*pos1[i-2] - 4./5*pos1[i-1] + 4./5*pos1[i+1] - 1./5*pos1[i+2] + 4./105* pos1[i+3] -1./280*pos1[i+4])/dt
#                vit1[i] = (pos1[i] -pos1[i-1])/(time[i] - time[i-1])
                vit2[i] = (1./280*pos2[i-4] - 4./105* pos2[i-3] + 1./5*pos2[i-2] - 4./5*pos2[i-1] + 4./5*pos2[i+1] - 1./5*pos2[i+2] + 4./105* pos2[i+3] -1./280*pos2[i+4])/dt
            except:
                print time[i]
                exit()

#        vit1 = sig.lfilter(b100, a100, vit1)
        vit1 = sig.lfilter(b[10], a[10], vit1)
        
        for i in range(4,N-4):
            dt1 = dt
            dt = (time[i] - time[i-1])
            if dt == 0:
                dt = dt1
            if vit1[i] >= 0:
                vitp[i] = vit1[i]
                vitm[i] = 0
                fcp[i] = 1
                fcm[i] = 0
            else:
                vitm[i] = vit1[i]
                vitp[i] = 0
                fcp[i] = 0
                fcm[i] = -1
            acc1[i] = (1./280*vit1[i-4] - 4./105* vit1[i-3] + 1./5*vit1[i-2] - 4./5*vit1[i-1] + 4./5*vit1[i+1] - 1./5*vit1[i+2] + 4./105* vit1[i+3] -1./280*vit1[i+4])/dt
#            acc1[i] = (vit1[i] -vit1[i-1])/(time[i] - time[i-1])
            acc2[i] = (1./280*vit2[i-4] - 4./105* vit2[i-3] + 1./5*vit2[i-2] - 4./5*vit2[i-1] + 4./5*vit2[i+1] - 1./5*vit2[i+2] + 4./105* vit2[i+3] -1./280*vit2[i+4])/dt
#        vit1 = sig.lfilter(b100, a100, vit1)
        acc1 = sig.lfilter(b[10], a[10], acc1)
#        int1 = sig.lfilter(b[100], a[100], int1) 
        
        indices1 = []
        indices2 =  []
        test = [0]*N

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
        for j in range (2, len(indices2)):
            for k in range(indices2[j-1], indices2[j]+1):
#                print k, indices2[j-1], indices2[j]
                for2[k] = (for2[indices2[j]] - for2[indices2[j-1]])/(time[indices2[j]] - time[indices2[j-1]])*(time[k] - time[indices2[j-1]]) + for2[indices2[j-1]]
#                
#        for1 = sig.lfilter(b[100], a[100], for1)
#        acc1 = sig.lfilter(b[100], a[100], acc1)
#        vitp = sig.lfilter(b[100], a[100], vitp)
#        vitm = sig.lfilter(b[100], a[100], vitm)
    ###############################################################################################################
    #Online impedance estimator
    #####################################################       
        
        deltaT = int(1000*0.050)
        offset = 0


        K= [0]*N
        F = [0]*N
        for i in range(0,N):
            if i<N/3:
                K[i] = 10
            elif (i>N/3 and i < 2*N/3):
                K[i] = 100
            else:
                K[i] = 50
        L = np.random.rand(N,1)
        for i in range(0,N):
            F[i] = L[i]*K[i] + np.random.randn()
    
        sigma = np.var(for1)
        
        a= [1.4, -0.7, 0.04, 0.7, -0.5]
#        N = 50000
           
        test = [0]*N
        test2 = [0]*N
        RMS = 0
        
        for i in range (5,N):
            test[i] = a[0]*test[i-1] + a[1]*test[i-2] + a[2]*test[i-3] + a[3]*test[i-4] + a[4]*test[i-5] + 1*np.random.randn()
            
        X = [0, 0, 0, 0, 0]
        W = [np.matrix([0, 0, 0, 0, 0]).T]*N
        alpha = 0
        G = [0,0,0,0,0]
        P = 1000*np.matrix(np.eye((5)))
        I = np.matrix(np.eye(5))
        lbd = 1
        gamma = 0.5/(3*25)
        l0 = int(0*5000)
        lf = int(N-0*5000)-1
        for i in range(l0, lf):
#            X = np.matrix([test[i-1], test[i-2], test[i-3], test[i-4], test[i-5]]).T
#            Y = test[i]
            X = np.matrix([acc1[i], vitp[i], vitm[i], fcp[i], fcm[i]]).T
            Y = cm1[i]
#            print i, X
            alpha = Y - X.T*W[i-1]
#            print i, alpha
            G = (P*X)/(lbd + X.T * P * X)
#            print i, G
            P = 1/lbd*(P - G*X.T*P) + round(gamma*alpha**2)*I
#            print i, P
            W[i] = W[i-1] + np.asscalar(alpha)*G
#            print i , W[i].T
        
        
#        scipy.io.savemat('/home/lucas/matlab_files_backup/for2.mat', mdict={'for2':for2})
#        scipy.io.savemat('/home/lucas/matlab_files_backup/int2.mat', mdict={'int2':int2})

        plt.figure(1)
        plt.subplot(511)
        plt.plot(time[l0:lf], pos1[l0:lf])        
        plt.subplot(512)
        plt.plot(time[l0:lf], vit1[l0:lf])
#        plt.plot(time[l0:lf], vitp[l0:lf])
#        plt.plot(time[l0:lf], vitm[l0:lf])
        plt.subplot(513)
        plt.plot(time[l0:lf], acc1[l0:lf])        
        plt.subplot(514)
        plt.plot(time[l0:lf], int1[l0:lf])
        test=[0]*N
        for i in range (l0,lf):
            test2[i] = (int1[i] - vitp[i]*np.asscalar(W[lf-1][1])+ vitm[i]*np.asscalar(W[lf-1][2])+ fcp[i]*np.asscalar(W[lf-1][3])+ fcm[i]*np.asscalar(W[lf-1][4]))/np.asscalar(W[lf-1][0])
            test[i] = acc1[i]*np.asscalar(W[lf-1][0])+ vitp[i]*np.asscalar(W[lf-1][1])+ vitm[i]*np.asscalar(W[lf-1][2])+ fcp[i]*np.asscalar(W[lf-1][3])+ fcm[i]*np.asscalar(W[lf-1][4])
        plt.subplot(515)
        plt.plot(time[l0:lf], test2[l0:lf])             
            
            
        print np.asscalar(W[lf-1][0]), '\t', np.asscalar(W[lf-1][1]), '\t', np.asscalar(W[lf-1][2]), '\t', np.asscalar(W[lf-1][3]), '\t', np.asscalar( W[lf-1][4])

        fig2 = plt.figure(2)
        ax1 = plt.subplot(321)
        p1[ij], = ax1.plot(time[l0:lf], [np.asscalar(x[0]) for x in W[l0:lf]])
        ax1.set_ylabel(r"Inertia $(kg.m^2)$")
        ax1.axis([time[l0], time[lf], 0.0001, 0.0004])
        ax1.text(time[l0] + 0.85*(time[lf]-time[l0]), 0.0001 + 0.15*(0.0004 - 0.0001), r"$J_h$", fontsize=20)
        
        ax2 = plt.subplot(323)
        p2, = ax2.plot(time[l0:lf], [np.asscalar(x[1]) for x in W[l0:lf]])
        ax2.set_ylabel(r"Viscous Friction $(N.m.s)$")
        ax2.axis([time[l0], time[lf], -0.005, 0.005])
        ax2.text(time[l0] + 0.85*(time[lf]-time[l0]), -0.005 + 0.15*(0.005 - -0.005), r"$\beta_1$", fontsize=20)
        
        ax3 = plt.subplot(324)
        p3, = ax3.plot(time[l0:lf], [np.asscalar(x[2]) for x in W[l0:lf]])
        ax3.axis([time[l0], time[lf], -0.005, 0.005])
        ax3.text(time[l0] + 0.85*(time[lf]-time[l0]), -0.005 + 0.15*(0.005 - -0.005), r"$\beta_2$", fontsize=20)
        
        ax4 = plt.subplot(325)
        p4, = ax4.plot(time[l0:lf], [np.asscalar(x[3]) for x in W[l0:lf]])
        ax4.set_ylabel(r"Coulomb Friction $(N.m)$")
        ax4.set_xlabel(r"Time $(s)$")
        ax4.axis([time[l0], time[lf], -0.015, 0.015])
        ax4.text(time[l0] + 0.85*(time[lf]-time[l0]), -0.015 + 0.15*(0.015 - -0.015), r"$\beta_3$", fontsize=20)
        
        ax5 = plt.subplot(326)
        p5, = ax5.plot(time[l0:lf], [np.asscalar(x[4]) for x in W[l0:lf]])    
        ax5.set_xlabel(r"Time $(s)$")
        ax5.axis([time[l0], time[lf], -0.015, 0.015])
        ax5.text(time[l0] + 0.85*(time[lf]-time[l0]), -0.015 + 0.15*(0.015 - -0.015), r"$\beta_4$", fontsize=20)
                
#        print np.asscalar(np.array(W[100])[2])
        legend_p.append(p1[ij])
        ij+=1
        legend_n.append("Excitation Session "+ str(ij))        
        
        fig2.legend(legend_p, legend_n, loc=1)
        

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