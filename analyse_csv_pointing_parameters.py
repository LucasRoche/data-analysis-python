# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:39:47 2018

@author: roche
"""

from __future__ import division
from postTrait_Module import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import scipy.signal as sig
import numpy as np
from Tkinter import *
from tkFileDialog import *
import os
import wx
import wx.lib.agw.multidirdialog as MDD
from datetime import datetime
import pandas
import time
from ast import literal_eval
import matplotlib.patches as mpatches
from matplotlib import cm
from scipy import stats
from scipy.optimize import curve_fit

def main():
    global Y, Ys
#    root = Tk()
#    root.withdraw()
#    file_name = askopenfilename(initialdir = '~/Documents/Manip')
#    root.destroy()    
    #18-57 18-2
    file_name = "~/Documents/Manip/DATA_POINTING_choices_11-4-10-29.csv"
    data = pandas.DataFrame.from_csv(file_name)   
    
    
    data_temp1 = data[(data['EXP_COND']=='ALONE')  & (data['FINAL_CHOICE']==320)].reset_index()
    data_temp2 = data[(data['EXP_COND']=='ALONE')  & (data['FINAL_CHOICE']==640)].reset_index()
    plt.figure()
    plt.axis([0,160,0,1])
    colors = [(0, 0, 1) , (0,0,0.5), (0, 1, 0), (0, 0.5, 0), (1, 0, 0), (0.5, 0, 0)]   
    
    
    #RAW DATA TARGET C
    x = data_temp1['TARGET_WIDTH1']
    y = [data_temp1['END_TIME'][i]-data_temp1['ST_TIME'][i] for i in range(0, len(data_temp1))]       
    plt.plot(x,y,color=colors[0],marker='x',linestyle='')
    
    
    
    #LOG REG, FUNC 1
    popt, pcov = curve_fit(func_log1_C,  x,  y)
    a = popt[0]
    b = popt[1]
    sigma_a = np.sqrt(pcov[0][0])
    sigma_b = np.sqrt(pcov[1][1])
    print a, sigma_a, b, sigma_b
    xf = range(1,160)
    yf = [func_log1_C(w, a, b) for w in xf]
    plt.plot(xf, yf, color=colors[0])
    
    #LOG REG, FUNC 2
    popt, pcov = curve_fit(func_log2_C,  x,  y)
    a = popt[0]
    b = popt[1]
    sigma_a = np.sqrt(pcov[0][0])
    sigma_b = np.sqrt(pcov[1][1])
    print a, sigma_a, b, sigma_b
    xf = range(1,160)
    yf = [func_log2_C(w, a, b) for w in xf]
    plt.plot(xf, yf, color=colors[0])
   
   
   
    #RAW DATA TARGET F
    x = data_temp2['TARGET_WIDTH2']
    y = [data_temp2['END_TIME'][i]-data_temp2['ST_TIME'][i] for i in range(0, len(data_temp2))]       
    plt.plot(x,y,color=colors[3],marker='x',linestyle='')
     
    
    #LOG REG, FUNC 1
    popt, pcov = curve_fit(func_log1_F,  x,  y)
    a = popt[0]
    b = popt[1]
    sigma_a = np.sqrt(pcov[0][0])
    sigma_b = np.sqrt(pcov[1][1])
    print a, sigma_a, b, sigma_b
    xf = range(1,160)
    yf = [func_log1_F(w, a, b) for w in xf]
    plt.plot(xf, yf, color=colors[3])
    
    #LOG REG, FUNC 2
    popt, pcov = curve_fit(func_log2_F,  x,  y)
    a = popt[0]
    b = popt[1]
    sigma_a = np.sqrt(pcov[0][0])
    sigma_b = np.sqrt(pcov[1][1])
    print a, sigma_a, b, sigma_b
    xf = range(1,160)
    yf = [func_log2_F(w, a, b) for w in xf]
    plt.plot(xf, yf, color=colors[3])
    


#####LINEAR REGRESSION AGAINST LOG(X)    
    plt.figure()
    plt.axis([3.5,8,0,1])
    #RAW DATA TARGET C

    x = np.log2(1+320/data_temp1['TARGET_WIDTH1'])
    y = [data_temp1['END_TIME'][i]-data_temp1['ST_TIME'][i] for i in range(0, len(data_temp1))]       
    plt.plot(x,y,color=colors[0],marker='x',linestyle='')
    
    
#    LINEAR REG
    slope1, intercept1, r_value, p_value, std_err = stats.linregress(x,y) 
    coefs = np.polyfit(x, y, 1, w=np.sqrt(x))
    print stats.linregress(x,y)  , np.polyfit(x, y, 1, w=np.sqrt(x))
    plt.plot([0,8],[intercept1, intercept1+slope1*8],color=colors[0])
#    plt.plot([0,8],[coefs[1], coefs[1]+coefs[0]*8],color=colors[0])
    
    
    #RAW DATA TARGET F

    x = np.log2(1+640/data_temp2['TARGET_WIDTH2'])
    y = [data_temp2['END_TIME'][i]-data_temp2['ST_TIME'][i] for i in range(0, len(data_temp2))]       
    plt.plot(x,y,color=colors[3],marker='x',linestyle='')
    
    
#    LINEAR REG
    slope2, intercept2, r_value, p_value, std_err = stats.linregress(x,y) 
    coefs = np.polyfit(x, y, 1, w=np.sqrt(x))
    print stats.linregress(x,y) , np.polyfit(x, y, 1)
    plt.plot([0,8],[intercept2, intercept2+slope2*8],color=colors[3])      
#    plt.plot([0,8],[coefs[1], coefs[1]+coefs[0]*8],color=colors[3])    
    
       
       
    plt.figure()
    ax1 = plt.subplot(511)
    data_temp = data[(data['EXP_COND']=='ALONE')  & (data['SUBJ_TARGET1']==0)].reset_index()      
    n = len(data_temp)
    y=data_temp['FINAL_CHOICE']
    x=[data_temp['TARGET_WIDTH2'][i] / data_temp['TARGET_WIDTH1'][i] for i in range(0,n)]
    ax1.plot(x,y,linestyle='',marker='+')
    
    ax2 = plt.subplot(512)
    ax3 = plt.subplot(513)
    nb_bins = 60
    max_range= 10
    hist1 = [x[i] for i in range(0,n) if y[i]==320]
    hist2 = [x[i] for i in range(0,n) if y[i]==640]   
    (n1, bins, patches1) = ax2.hist(hist1, bins = nb_bins, range=(0,max_range))
    (n2, bins, patches2) = ax3.hist(hist2, bins = nb_bins, range=(0,max_range))
    nt1 = [n1[i]/(n1[i]+n2[i]) if (n1[i]+n2[i])!=0 else 0 for i in range(0, len(n1))]
    nt2 = [n2[i]/(n1[i]+n2[i]) if (n1[i]+n2[i])!=0 else 0 for i in range(0, len(n1))]

    ax4 = plt.subplot(514)
    ax4.bar(bins[:-1],nt1,width=max_range/nb_bins)
    ax4.plot([0,max_range],[0.5,0.5], color='red')
    ax5 = plt.subplot(515)
    ax5.bar(bins[:-1],nt2,width=max_range/nb_bins)
    ax5.plot([0,max_range],[0.5,0.5], color='red')

    ax2.axis([0,max_range,0,max(n1)])
    ax3.axis([0,max_range,0,max(n2)])
    ax4.axis([0,max_range,0,1])
    ax5.axis([0,max_range,0,1])

    

    A = np.matrix([[-slope1, 0, 1, 0],
         [0, -slope2, 0, 1],
         [-1, 1, 0, 0],
         [0, 0, -1, 1]])
    B = np.matrix([intercept1, intercept2, np.log2(1.6), 0]).T
    
    X = np.linalg.solve(A,B)
    
    print "Width target 1 : ", np.exp(X[0]*np.log(2))
    print "Width target 2 : ", np.exp(X[1]*np.log(2))
    print "Estimated travel time : ", X[2]
    
    plt.show(block='True')
    
    
    
    
    
    
def func_log1_C(w, a, b):
    return a + b*np.log2(580/w)
def func_log1_F(w, a, b):
    return a + b*np.log2(1220/w)    

def func_log2_C(w, a, b):
    return a + b*np.log2(1+290/w)
def func_log2_F(w, a, b):
    return a + b*np.log2(1+610/w)
            
def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1
        
def cohenns_d(group1, group2):
    return (np.mean(group1)-np.mean(group2))/sqrt(0.5*(np.std(group1)+np.std(group2)))

def cmdscale(D):
    """                                                                                       
    Classical multidimensional scaling (MDS)                                                  
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    D : (n, n) array                                                                          
        Symmetric distance matrix.                                                            
                                                                                               
    Returns                                                                                   
    -------                                                                                   
    Y : (n, p) array                                                                          
        Configuration matrix. Each column represents a dimension. Only the                    
        p dimensions corresponding to positive eigenvalues of B are returned.                 
        Note that each dimension is only determined up to an overall sign,                    
        corresponding to a reflection.                                                        
                                                                                               
    e : (n,) array                                                                            
        Eigenvalues of B.                                                                     
                                                                                               
    """
    # Number of points                                                                        
    n = len(D)
 
    # Centering matrix                                                                        
    H = np.eye(n) - np.ones((n, n))/n
 
    # YY^T                                                                                    
    B = -H.dot(D**2).dot(H)/2
 
    # Diagonalize                                                                             
    evals, evecs = np.linalg.eigh(B)
 
    # Sort by eigenvalue in descending order                                                  
    idx   = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:,idx]
 
    # Compute the coordinates using positive-eigenvalued components only                      
    w, = np.where(evals > 0)
    L  = np.diag(np.sqrt(evals[w]))
    V  = evecs[:,w]
    Y  = V.dot(L)
 
    return Y, evals
                
if __name__ == '__main__':
    main()