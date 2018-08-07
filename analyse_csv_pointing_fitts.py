# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:37:48 2018

@author: lucas
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
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm


def main():
    global Y, Ys
#    root = Tk()
#    root.withdraw()
#    file_name = askopenfilename(initialdir = '~/Documents/Manip')
#    root.destroy()    
    #18-57 18-2
    file_name = "~/Documents/Manip/DATA_POINTING_choices_fittstest.csv"
    data = pandas.DataFrame.from_csv(file_name)   
    
    data_temp1 = data[(data['EXP_COND']=='ALONE') & (data['END_TIME']!=data['ST_TIME'])].reset_index(drop=True)
    data_temp1['TARGET_WIDTH1'] = 2*data_temp1['TARGET_WIDTH1']
    df = []
    for subj_name in list(set(data_temp1['SUBJ_NAME1'])):        
        df.append(data_temp1[(data_temp1['SUBJ_NAME1']==subj_name) & (data_temp1['TARGET_WIDTH1']>0) & (data_temp1['FINAL_CHOICE']>0) & (data_temp1['END_TIME']<3)].reset_index(drop=True).loc[:,:].reset_index(drop=True))
    ns = len(df)

    
    colors = [(0, 0, 1) , (0,0,0.5), (0, 1, 0), (0, 0.5, 0), (1, 0, 0), (0.5, 0, 0)]
    markers = [ 'd', 'o', 'h', '*', '^', 'v', 's', '<', '>','p', 'x', ',']
    norm = plt.Normalize()
    colors = cm.jet(norm(range(ns)))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('A')
    ax.set_ylabel('W')
    ax.set_zlabel('MT')
    for k in range(0,ns):
        A = df[k]['FINAL_CHOICE']
        W = df[k]['TARGET_WIDTH1']
        MT = [df[k]['END_TIME'][i]-df[k]['ST_TIME'][i] for i in range(0,len(df[k]))]
        ax.scatter(A,W,MT, color=colors[k], marker=markers[k])

    
    
    #RAW DATA TARGET C
    plt.figure()
    x_min=100
    x_max=-100
    y_min=100
    y_max=-100
    for k in range(ns):
        x = [float(df[k]['FINAL_CHOICE'][i])/df[k]['TARGET_WIDTH1'][i] for i in range(0, len(df[k]))]
        y = [df[k]['END_TIME'][i]-df[k]['ST_TIME'][i] for i in range(0, len(df[k]))]       
        plt.plot(x,y,color=colors[k],marker=markers[k],linestyle='')
        x_min=min(min(x),x_min)
        x_max=max(max(x),x_max)
        y_min=min(min(y),y_min)
        y_max=max(max(y),y_max)
        
        
        #LOG REG, FUNC 1
        popt, pcov = curve_fit(func_log1_C,  x,  y)
        a = popt[0]
        b = popt[1]
        sigma_a = np.sqrt(pcov[0][0])
        sigma_b = np.sqrt(pcov[1][1])
        print a, sigma_a, b, sigma_b
        xf = range(1,160)
        yf = [func_log1_C(w, a, b) for w in xf]
        plt.plot(xf, yf, color=colors[k])
        
        #LOG REG, FUNC 2
        popt, pcov = curve_fit(func_log2_C,  x,  y)
        a = popt[0]
        b = popt[1]
        sigma_a = np.sqrt(pcov[0][0])
        sigma_b = np.sqrt(pcov[1][1])
        print a, sigma_a, b, sigma_b
        xf = range(1,160)
        yf = [func_log2_C(w, a, b) for w in xf]
        plt.plot(xf, yf, color=colors[k])
   
    plt.axis([0.8*x_min,1.2*x_max,0,1.2*y_max]) 
    


#####LINEAR REGRESSION AGAINST LOG(X)    
    fig1 = plt.figure("Fitts")
    ax1 = fig1.add_subplot(111)
    fig2 = plt.figure("Shannon")
    ax2 = fig2.add_subplot(111)
    x_min1=100
    x_min2=100
    x_max1=-100
    x_max2=-100   
    y_min=100
    y_max=-100
#    plt.axis([0,5,0,1])
    for k in range(ns):
        #RAW DATA TARGET C
        x1 = np.log2([2*float(df[k]['FINAL_CHOICE'][i])/df[k]['TARGET_WIDTH1'][i] for i in range(0, len(df[k]))])
        x2 = np.log2([1+float(df[k]['FINAL_CHOICE'][i])/df[k]['TARGET_WIDTH1'][i] for i in range(0, len(df[k]))])
        y = [df[k]['END_TIME'][i]-df[k]['ST_TIME'][i] for i in range(0, len(df[k]))]       
        x_min1=min(min(x1),x_min1)
        x_max1=max(max(x1),x_max1)
        x_min2=min(min(x2),x_min2)
        x_max2=max(max(x2),x_max2)        
        y_min=min(min(y),y_min)
        y_max=max(max(y),y_max)
        
        ax1.plot(x1,y,color=colors[k],marker=markers[k],linestyle='')
        ax2.plot(x2,y,color=colors[k],marker=markers[k],linestyle='')
        
        
    #    LINEAR REG
        slope1, intercept1, r_value, p_value, std_err = stats.linregress(x1,y) 
        print df[k]['SUBJ_NAME1'][0], '\t- Slope : ', slope1, '\tIntercept : ', intercept1, '\tR : ', r_value, '\tp : ', p_value
        ax1.plot([0,2*x_max1],[intercept1, intercept1+slope1*2*x_max1],color=colors[k], label=df[k]['SUBJ_NAME1'][0])

        slope2, intercept2, r_value, p_value, std_err = stats.linregress(x2,y) 
        print df[k]['SUBJ_NAME1'][0], '\t- Slope : ', slope2, '\tIntercept : ', intercept2, '\tR : ', r_value, '\tp : ', p_value
        ax2.plot([0,2*x_max2],[intercept2, intercept2+slope2*2*x_max2],color=colors[k], label=df[k]['SUBJ_NAME1'][0])
        
    ax1.axis([0.8*x_min1,1.2*x_max1,0,1.2*y_max])
    ax1.legend()
    ax2.axis([0.8*x_min2,1.2*x_max2,0,1.2*y_max])
    ax2.legend()   

    data_temp2 = pandas.concat(df,ignore_index='True')
    x1 = np.log2([2*float(data_temp2['FINAL_CHOICE'][i])/data_temp2['TARGET_WIDTH1'][i] for i in range(0, len(data_temp2))])
    x2 = np.log2([1+float(data_temp2['FINAL_CHOICE'][i])/data_temp2['TARGET_WIDTH1'][i] for i in range(0, len(data_temp2))])
    y = [data_temp2['END_TIME'][i]-data_temp2['ST_TIME'][i] for i in range(0, len(data_temp2))]       
    
#    LINEAR REG
    slope1, intercept1, r_value, p_value, std_err = stats.linregress(x1,y) 
    print 'TOTAL\t- Slope : ', slope1, '\tIntercept : ', intercept1, '\tR : ', r_value, '\tp : ', p_value
    ax1.plot([0,2*x_max1],[intercept1, intercept1+slope1*2*x_max1],color='black',linestyle='--')
    model = sm.OLS(y, x1)
    results = model.fit()
    print results.summary()
    ax1.plot([0,2*x_max1],[0, results.params[0]*2*x_max1],color='black',linestyle='--')
    
    slope2, intercept2, r_value, p_value, std_err = stats.linregress(x2,y)     
    print 'TOTAL\t- Slope : ', slope2, '\tIntercept : ', intercept2, '\tR : ', r_value, '\tp : ', p_value
    ax2.plot([0,2*x_max2],[intercept2, intercept2+slope2*2*x_max2],color='black',linestyle='--') 
    model = sm.OLS(y, x1)
    results = model.fit()
    print results.summary()
    ax2.plot([0,2*x_max1],[0, results.params[0]*2*x_max1],color='black',linestyle='--')  
    
    
 ###################################""
    fig3 = plt.figure("speed accuracy tradeoff")
    ax3 = fig3.add_subplot(111)
    y = [data_temp2['TARGET_WIDTH1'][i] for i in range(0, len(data_temp2))]
    x1 = [float(data_temp2['FINAL_CHOICE'][i])/(data_temp2['END_TIME'][i]-data_temp2['ST_TIME'][i]) for i in range(0, len(data_temp2))]       

    mask = np.isfinite(x1) & np.isfinite(y)
    x1 = [x1[i] for i in range(len(x1)) if mask[i]==True ]
    y = [y[i] for i in range(len(y)) if mask[i]==True]
    x_min1=min(min(x1),x_min1)
    x_max1=max(max(x1),x_max1)
    y_min=min(min(y),y_min)
    y_max=max(max(y),y_max)
    ax3.axis([0.8*x_min1,1.2*x_max1,0,1.2*y_max])
    slope1, intercept1, r_value, p_value, std_err = stats.linregress(x1, y)
    print 'TOTAL\t- Slope : ', slope1, '\tIntercept : ', intercept1, '\tR : ', r_value, '\tp : ', p_value
    ax3.plot(x1,y,color=colors[k],marker=markers[k],linestyle='')
    ax3.plot([0,2*x_max1],[intercept1, intercept1+slope1*2*x_max1],color='black',linestyle='--')    

    dft = pandas.DataFrame(data={'W': y, 'AMT' : x1, 'Ones' : np.ones((len(y),)) })
    model = sm.OLS(dft.W, dft.AMT)
    results = model.fit()
    print results.summary()
    
    dft = pandas.DataFrame(data={'W': y, 'AMT' : x1, 'Ones' : np.ones((len(y),)) })
    model = sm.OLS(dft.W, dft[['AMT','Ones']])
    results = model.fit()
    print results.summary()    
    
    
    ax3.plot([0,2*x_max1],[0, results.params[0]*2*x_max1],color='black',linestyle='--')    
    
    plt.show(block='True')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def func_log1_C(r, a, b):
    return a + b*np.log2(2*r)
def func_log2_C(r, a, b):
    return a + b*np.log2(1+r)    
     
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