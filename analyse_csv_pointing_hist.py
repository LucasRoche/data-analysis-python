# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 17:03:41 2018

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

def main():
    global Y, Ys
    root = Tk()
    root.withdraw()
    file_name = askopenfilename(initialdir = '~/Documents/Manip')
    root.destroy()    
    
    data = pandas.DataFrame.from_csv(file_name)

    data['HIST'] = data['HIST'].apply(literal_eval) 
   
#    for i in range(0, len(data['HIST'])):
#        plt.figure()
#        if(data['SUBJ_NB'][i]==0):
#            plt.title(data['EXP_COND'][i] + ' : ' + data['SUBJ_NAME1'][i])
#        elif(data['SUBJ_NB'][i]==1):
#            plt.title(data['EXP_COND'][i] + ' : ' + data['SUBJ_NAME2'][i]) 
#        elif(data['SUBJ_NB'][i]==2):
#            plt.title(data['EXP_COND'][i] + ' : ' + data['SUBJ_NAME1'][i]+'+'+data['SUBJ_NAME2'][i])            
#        plt.plot(np.linspace(-0.75, 1.5, 101), data['HIST'][i])
    
    tempName = ''
    k=0
    
    
    
    data_bytrial = pandas.DataFrame(data={'SUBJ_NB':[], 'SUBJ_NAME1' : [], 'SUBJ_NAME2' : [], 'EXP_COND':[], 'HIST':[], 'TRIAL_NB' : [], 'IS_TRAINING':[]} )
    
    #Reconstruct a dataframe with one histogram by trial for plotting
    for subj_name1 in list(set(data['SUBJ_NAME1'])):        
        subj_name2 = data[data['SUBJ_NAME1']==subj_name1]['SUBJ_NAME2'].reset_index()['SUBJ_NAME2'][0]
        for cond in list(set(data[data['SUBJ_NAME1'] == subj_name1]['EXP_COND'])):
            for trial in list(set(data[(data['SUBJ_NAME1'] == subj_name1) & (data['EXP_COND'] == cond)]['TRIAL_NB'])):
                for s in list(set(data[(data['SUBJ_NAME1'] == subj_name1)& (data['EXP_COND'] == cond) & (data['TRIAL_NB']== trial)]['SUBJ_NB'])):
                    df = data[(data['SUBJ_NAME1'] == subj_name1)& (data['EXP_COND'] == cond) & (data['TRIAL_NB']== trial) & (data['SUBJ_NB']== s)].reset_index()
                    temp_hist = [0]*101
                    for i in range(0, len(df )):
                        temp_hist = np.add(temp_hist, df['HIST'][i])
                    if np.sum(temp_hist)!=0:
                        temp_hist = [float(x)/float(np.sum(temp_hist)) for x in temp_hist]
                    else:
                        temp_hist = [float(x) for x in temp_hist]
                    temp_df = pandas.DataFrame(data={'SUBJ_NB':[s], 'SUBJ_NAME1':[subj_name1], 'SUBJ_NAME2': [subj_name2], 'EXP_COND':[cond], 'HIST':[temp_hist], 'TRIAL_NB' : [trial], 'IS_TRAINING':[int(df['IS_TRAINING'][0])]})                   
                    data_bytrial = data_bytrial.append(temp_df,ignore_index=True)
                    
    #Plot HIstograms
    colors = [(0, 0, 1) , (0,0,0.5), (0, 1, 0), (0, 0.5, 0), (1, 0, 0), (0.5, 0, 0)]

    for subj_name1 in list(set(data['SUBJ_NAME1'])):
        plt.figure()
        subj_name2 = data_bytrial[data_bytrial['SUBJ_NAME1']==subj_name1]['SUBJ_NAME2'].reset_index()['SUBJ_NAME2'][0]
        plt.suptitle(subj_name1 + ' + ' + subj_name2)
        y_max = 5*max([max(x) for x in data_bytrial[data_bytrial['SUBJ_NAME1']==subj_name1]['HIST']])
        for cond in list(set(data_bytrial[data_bytrial['SUBJ_NAME1'] == subj_name1]['EXP_COND'])):
            for subj_nb in list(set(data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND'] == cond)]['SUBJ_NB'])):
                df = data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1)& (data_bytrial['EXP_COND'] == cond) & (data_bytrial['SUBJ_NB']== subj_nb)].reset_index()
                
                if(subj_nb==0):
                    sp_title = cond + ' : ' + subj_name1
                    if(cond=='ALONE'):
                        k=1
                    elif(cond=='HFO'):
                        k=5
                elif(subj_nb==1):
                    sp_title = cond + ' : ' + subj_name2
                    if(cond=='ALONE'):
                        k=2
                    elif(cond=='HFO'):
                        k=6            
                elif(subj_nb==2):
                    sp_title = cond + ' : ' + subj_name1+'+'+subj_name2
                    if(cond=='HFOP'):
                        k=3
                    elif(cond=='HFO'):
                        k=7
                        
                ax = plt.subplot(2,4,k)
                ax.set_title(sp_title)
                plt.axis([-0.75, 1.5, 0, y_max])
        #        plt.plot(np.linspace(-0.75, 1.5, 101), data_bytrial['HIST'][i])
                edges = np.linspace(-0.75, 1.5, 101) 
                plt.bar(edges[:-1], df['HIST'][0][:-1], width=np.diff(edges), ec="k", align="edge", color=colors[0]) 
                for i in range(1, len(df['HIST'])):
                    bottom = [0]*100
                    for j in range(0,i):
                        bottom = np.add(bottom, df['HIST'][j][:-1])
                    plt.bar(edges[:-1], df['HIST'][i][:-1], bottom = bottom , width=np.diff(edges), ec="k", align="edge", color=colors[i])
                    
        ax = plt.subplot(2,4,4)
        ax.set_title("ALONE : Mean both")
        plt.axis([-0.75, 1.5, 0, y_max])
#        plt.plot(np.linspace(-0.75, 1.5, 101), data_bytrial['HIST'][i])
        edges = np.linspace(-0.75, 1.5, 101)         

        df_mix1=[0]*6
        df_mix2=[0]*6
        df_mix=[0]*6
        n = len(data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='ALONE') & (data_bytrial['SUBJ_NB']==0)].reset_index()['HIST'])
        for i in range(0, n):
            df_mix1[i] = data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='ALONE') & (data_bytrial['SUBJ_NB']==0)].reset_index()['HIST'][i]
            df_mix2[i] = data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='ALONE') & (data_bytrial['SUBJ_NB']==1)].reset_index()['HIST'][i]
            df_mix[i] = [float(x)/2.0 for x in np.add(df_mix1[i],df_mix2[i])]
#            print df_mix1[i]
#            print df_mix2[i]
#            print df_mix[i]
        for i in range(0, n):
            bottom = [0]*100
            if i!=0:
                for j in range(0,i):
                    bottom = np.add(bottom, df_mix[j][:-1])
            plt.bar(edges[:-1], df_mix[i][:-1], bottom = bottom , width=np.diff(edges), ec="k", align="edge", color=colors[i])
                
        ax = plt.subplot(2,4,8)
        ax.set_title("HFO : Mean both")
        plt.axis([-0.75, 1.5, 0, y_max])
#        plt.plot(np.linspace(-0.75, 1.5, 101), data_bytrial['HIST'][i])
        edges = np.linspace(-0.75, 1.5, 101)         

        df_mix1=[0]*6
        df_mix2=[0]*6
        df_mix=[0]*6
        n = len(data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='HFO') & (data_bytrial['SUBJ_NB']==0)].reset_index()['HIST'])
        for i in range(0, n):
            df_mix1[i] = data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='HFO') & (data_bytrial['SUBJ_NB']==0)].reset_index()['HIST'][i]
            df_mix2[i] = data_bytrial[(data_bytrial['SUBJ_NAME1'] == subj_name1) & (data_bytrial['EXP_COND']=='HFO') & (data_bytrial['SUBJ_NB']==1)].reset_index()['HIST'][i]
            df_mix[i] = [float(x)/2.0 for x in np.add(df_mix1[i],df_mix2[i])]
#            print df_mix1[i]
#            print df_mix2[i]
#            print df_mix[i]
        for i in range(0, n):
            bottom = [0]*100
            if i!=0:
                for j in range(0,i):
                    bottom = np.add(bottom, df_mix[j][:-1])
            plt.bar(edges[:-1], df_mix[i][:-1], bottom = bottom , width=np.diff(edges), ec="k", align="edge", color=colors[i])            

    
    df_al = data_bytrial[data_bytrial['EXP_COND']=='ALONE']
    n = len(df_al[(df_al['SUBJ_NAME1']==df_al['SUBJ_NAME1'][0]) & (df_al['SUBJ_NB']==0)])
    
    data_D = pandas.DataFrame(data={'TRIAL_NB':[], 'SUBJ_NAME':[], 'HIST':[]})
    for i in range(0, n):
        print i
        for subj_name1 in list(set(df_al['SUBJ_NAME1'])):
            print subj_name1
            subj_name2 = df_al[df_al['SUBJ_NAME1']==subj_name1]['SUBJ_NAME2'].reset_index()['SUBJ_NAME2'][0]
            for k in range(0,2):
                if k==0:
                    try:
                        tempdf = pandas.DataFrame(data={'TRIAL_NB':[i], 'SUBJ_NAME':[subj_name1], 'HIST':[df_al[(df_al['SUBJ_NAME1']==subj_name1) & (df_al['SUBJ_NB']==k) ].reset_index()['HIST'][i]]})
                    except:
                        tempdf = pandas.DataFrame(data={'TRIAL_NB':[i], 'SUBJ_NAME':[subj_name1], 'HIST':[[0.0]*101]})                        
                    data_D = data_D.append(tempdf,ignore_index=True)
                elif k==1:
                    try:
                        tempdf = pandas.DataFrame(data={'TRIAL_NB':[i], 'SUBJ_NAME':[subj_name2], 'HIST':[df_al[(df_al['SUBJ_NAME2']==subj_name2) & (df_al['SUBJ_NB']==k) ].reset_index()['HIST'][i]]})
                    except:
                        tempdf = pandas.DataFrame(data={'TRIAL_NB':[i], 'SUBJ_NAME':[subj_name2], 'HIST':[[0.0]*101]})                        
                    data_D = data_D.append(tempdf,ignore_index=True)  
                
    print data_D
    
    ns = len(list(set(data_D['SUBJ_NAME'])))
    subj_names = list(set(data_D['SUBJ_NAME']))
    D = np.zeros((ns,ns))
    Y = [0]*n
    bins = np.linspace(-0.75, 1.5, 101)
    bin_width = bins[1]-bins[0]
    max_emd = 2.25
    plt.figure()
    a = plt.subplot(111)
    plt.axis('equal')
    colors = [(0, 0, 1) , (0,0,0.5), (0, 1, 0), (0, 0.5, 0), (1, 0, 0), (0.5, 0, 0), (1, 0, 1), (0.5, 0, 0.5), (0, 1, 1), (0, 0.5, 0.5), (1, 1, 0), (0.5, 0.5, 0), (1,1,1), (0.5,0.5,0.5)]
    norm = plt.Normalize()
    colors = cm.jet(norm(range(ns)))
    for i in range(0,n):
        tempdf = data_D[data_D['TRIAL_NB']==i].reset_index()
        for j in range(0, ns):
            for k in range(0, ns):
                h1 = tempdf['HIST'][j]
                h2 = tempdf['HIST'][k]
                if j==k:
                   D[j][k] = 0
                else:
                   D[j][k] = sum(abs(np.cumsum(h1)-np.cumsum(h2)))*bin_width/max_emd
    
        tempY, e = cmdscale(D)
        Y[i] = tempY[:,0:2]
        
        
#        for l in range(0, len(Y)):
#            plt.plot(Y[i][l][0], Y[i][l][1], '+', markersize=8, mew=2, color=colors[i])

    Ys = []
    for i in range(0,ns):
        Ys.append(np.zeros((n,2)))
            
    for i in range(0,n):
        for j in range(0, ns):
#            print Ys[j][i,:]
            Ys[j][i,:] = Y[i][j,:]

        
    for i in range(0, ns):
        COV = np.cov(Ys[i], rowvar=0)
        
        CX = np.mean(Ys[i], axis = 0)[0]
        CY = np.mean(Ys[i], axis = 0)[1]
#        print Ys[i]       
        for j in range(0, n):
#            print Ys[i][j,0], Ys[i][j,1]
            plt.plot(Ys[i][j,0], Ys[i][j,1], '+', markersize=8, mew=2, color=colors[i])
        plt.plot(CX, CY, 'o', markersize=8, mew=2, color=colors[i])
        plt.text(CX, CY, subj_names[i], color = colors[i])
        
        
        eigval, eigvec = np.linalg.eigh(COV)
        
#        print ""
#        print eigval
#        print eigvec
#        print "\n"
        
        V1 = eigvec[:][1]
        V2 = eigvec[:][0]
        lmb1 = eigval[1]
        lmb2 = eigval[0]
        s = 4.605#5.991
        l1 = 2*np.sqrt(5.991*lmb1)
        l2 = 2*np.sqrt(5.991*lmb2)
        alpha = 180/pi*np.arctan(V1[1]/V1[0])
        
        e = mpatches.Ellipse((CX,CY), l1, l2, alpha, color = colors[i])
        e.set_clip_box(a.bbox)
        e.set_alpha(0.1)
        a.add_artist(e)    
    
    plt.show()        
    quit()

#    for i in range(0, len(data_bytrial['HIST'])):
#        if tempName != data_bytrial['SUBJ_NAME1'][i]:
#            tempName = data_bytrial['SUBJ_NAME1'][i]
#            plt.figure()
#            plt.suptitle(data_bytrial['SUBJ_NAME1'][i] + ' + ' + data_bytrial['SUBJ_NAME2'][i])
#            y_max = 1.05*max([max(x) for x in data_bytrial[data_bytrial['SUBJ_NAME1']==tempName]['HIST']])
#        
#        if(data_bytrial['SUBJ_NB'][i]==0):
#            sp_title = data_bytrial['EXP_COND'][i] + ' : ' + data_bytrial['SUBJ_NAME1'][i]
#            if(data_bytrial['EXP_COND'][i]=='ALONE'):
#                k=1
#            elif(data_bytrial['EXP_COND'][i]=='HFO'):
#                k=4
#        elif(data_bytrial['SUBJ_NB'][i]==1):
#            sp_title = data_bytrial['EXP_COND'][i] + ' : ' + data_bytrial['SUBJ_NAME2'][i]
#            if(data_bytrial['EXP_COND'][i]=='ALONE'):
#                k=2
#            elif(data_bytrial['EXP_COND'][i]=='HFO'):
#                k=5            
#        elif(data_bytrial['SUBJ_NB'][i]==2):
#            sp_title = data_bytrial['EXP_COND'][i] + ' : ' + data_bytrial['SUBJ_NAME1'][i]+'+'+data_bytrial['SUBJ_NAME2'][i]
#            if(data_bytrial['EXP_COND'][i]=='HFOP'):
#                k=3
#            elif(data_bytrial['EXP_COND'][i]=='HFO'):
#                k=6
#                
#        ax = plt.subplot(2,3,k)
#        ax.set_title(sp_title)
#        plt.axis([-0.75, 1.5, 0, y_max])
##        plt.plot(np.linspace(-0.75, 1.5, 101), data_bytrial['HIST'][i])
#        edges = np.linspace(-0.75, 1.5, 101)
#        plt.bar(edges[:-1], data_bytrial['HIST'][i][:-1], width=np.diff(edges), ec="k", align="edge")
#        
#       
#       
#    
#        
#    plt.show()
    
def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1

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