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
from scipy import stats
from scipy.optimize import curve_fit

def main():
    global Y, Ys
#    root = Tk()
#    root.withdraw()
#    file_name = askopenfilename(initialdir = '~/Documents/Manip')
#    root.destroy()    
    #18-57 18-2
    file_name = "~/Documents/Manip/DATA_POINTING_choices_28-3-15-13.csv"
    data = pandas.DataFrame.from_csv(file_name)   
    


    table_ALONE_n = [[0],[0],[0]] 
    table_ALONE_1 = [[0,0],[0,0],[0,0]]        
    for subj_tar1 in range(0,3):
        data_temp = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (((data['SUBJ_TARGET1']==subj_tar1) & (data['SUBJ_NB']==0)) | ((data['SUBJ_TARGET2']==subj_tar1) & (data['SUBJ_NB']==1)))]
        table_ALONE_n[subj_tar1][0] = len(data_temp)
        table_ALONE_1[subj_tar1][0] = len(data_temp[data_temp['FINAL_CHOICE']==320])/len(data_temp)
        table_ALONE_1[subj_tar1][1] = len(data_temp[data_temp['FINAL_CHOICE']==640])/len(data_temp)
    labels= ['No target', 'Target 1', 'Target 2']
    plt.figure('ALONE')
    ax1 = plt.subplot(211)
    ax1.axis('off')
    ax1.axis('tight')
    plt.table(cellText = table_ALONE_n, rowLabels = labels, colLabels = ["Total"], loc='center')
    ax2 = plt.subplot(212)
    ax2.axis('off')
    ax2.axis('tight')
    plt.table(cellText = table_ALONE_1, rowLabels = labels, colLabels = ["Choice 1 (%)", "Choice 2(%)"], loc='center')       



    table_HFO_n = [[0,0,0],[0,0,0],[0,0,0]] 
    table_HFO_1 = [[0,0,0],[0,0,0],[0,0,0]] 
    table_HFO_2 = [[0,0,0],[0,0,0],[0,0,0]]       
    for subj_tar1 in range(0,3):
        for subj_tar2 in range(0,3):
            if (subj_tar1==subj_tar2==0) or (subj_tar1== 1 and subj_tar2==2) or (subj_tar1== 2 and subj_tar2==1):
                table_HFO_n[subj_tar1][subj_tar2] = table_HFO_1[subj_tar1][subj_tar2] =table_HFO_2[subj_tar1][subj_tar2] ='-'
                continue
            data_temp = data[(data['EXP_COND']=='HFO') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==subj_tar1) & (data['SUBJ_TARGET2']==subj_tar2)]
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, '  ',  len(data_temp)
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, 'final choice : 1  ', len(data_temp[data_temp['FINAL_CHOICE']==320]), '\t', len(data_temp[data_temp['FINAL_CHOICE']==320])/len(data_temp)
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, 'final choice : 2  ', len(data_temp[data_temp['FINAL_CHOICE']==640]), '\t', len(data_temp[data_temp['FINAL_CHOICE']==640])/len(data_temp)
#            print ""
            table_HFO_n[subj_tar1][subj_tar2] = len(data_temp)
            table_HFO_1[subj_tar1][subj_tar2] = len(data_temp[data_temp['FINAL_CHOICE']==320])/len(data_temp)
            table_HFO_2[subj_tar1][subj_tar2] = len(data_temp[data_temp['FINAL_CHOICE']==640])/len(data_temp)
    labels= ['No target', 'Target 1', 'Target 2']
    plt.figure('HFO')
    ax1 = plt.subplot(211)
    ax1.axis('off')
    ax1.axis('tight')
    plt.table(cellText = table_HFO_n, rowLabels = labels, colLabels = labels, loc='center')
    ax2 = plt.subplot(212)
    ax2.axis('off')
    ax2.axis('tight')
    plt.table(cellText = table_HFO_1, rowLabels = labels, colLabels = labels, loc='center')    


    table_HFOP_n = [[0,0,0],[0,0,0],[0,0,0]] 
    table_HFOP_1 = [[0,0,0],[0,0,0],[0,0,0]] 
    table_HFOP_2 = [[0,0,0],[0,0,0],[0,0,0]]         
    for subj_tar1 in range(0,3):
        for subj_tar2 in range(0,3):
            if (subj_tar1==subj_tar2==0) or (subj_tar1== 1 and subj_tar2==2) or (subj_tar1== 2 and subj_tar2==1):
                table_HFOP_n[subj_tar1][subj_tar2] = table_HFOP_1[subj_tar1][subj_tar2] =table_HFOP_2[subj_tar1][subj_tar2] ='-'
                continue
            data_temp = data[(data['EXP_COND']=='HFOP') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==subj_tar1) & (data['SUBJ_TARGET2']==subj_tar2)]
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, '  ',  len(data_temp)
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, 'final choice : 1  ', len(data_temp[data_temp['FINAL_CHOICE']==320]), '\t', len(data_temp[data_temp['FINAL_CHOICE']==320])/len(data_temp)
#            print 'target1 : ', subj_tar1, 'target2 : ', subj_tar2, 'final choice : 2  ', len(data_temp[data_temp['FINAL_CHOICE']==640]), '\t', len(data_temp[data_temp['FINAL_CHOICE']==640])/len(data_temp)
#            print ""
            table_HFOP_n[subj_tar1][subj_tar2] = len(data_temp)
            table_HFOP_1[subj_tar1][subj_tar2] = len(data_temp[data_temp['FINAL_CHOICE']==320])/len(data_temp)
            table_HFOP_2[subj_tar1][subj_tar2] = len(data_temp[data_temp['FINAL_CHOICE']==640])/len(data_temp)
    plt.figure('HFOP')
    ax1 = plt.subplot(211)
    ax1.axis('off')
    ax1.axis('tight')
    plt.table(cellText = table_HFOP_n, rowLabels = labels, colLabels = labels, loc='center')
    ax2 = plt.subplot(212)
    ax2.axis('off')
    ax2.axis('tight')
    plt.table(cellText = table_HFOP_1, rowLabels = labels, colLabels = labels, loc='center')    


    for exp_cond in ['ALONE', 'HFO', 'HFOP']:
        print exp_cond
        data_temp_t1 = data[(data['EXP_COND']==exp_cond) & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==320)].reset_index()
        data_temp_t2 = data[(data['EXP_COND']==exp_cond) & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==640)].reset_index()  
        n1 = len(data_temp_t1)
        n2 = len(data_temp_t2)
        n = n1 + n2
        print "nb trials: ", n, "(", n1, "+", n2, ")"
        traj_times_t1 = [0]*n1
        traj_times_t2 = [0]*n2       
        for i in range(0,n1):
            traj_times_t1[i] = data_temp_t1['END_TIME'][i] - data_temp_t1['ST_TIME'][i]
        for i in range(0,n2):
            traj_times_t2[i] = data_temp_t2['END_TIME'][i] - data_temp_t2['ST_TIME'][i] 
        
        print "mean T1, ste T1, mean T2, ste T2"
        print np.mean(traj_times_t1), np.std(traj_times_t1)/sqrt(n1), np.mean(traj_times_t2), np.std(traj_times_t2)/sqrt(n2)
        print "t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_t1, traj_times_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_t1, traj_times_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_t1, traj_times_t2),5)

    

    print "\nCOMPLETION TIMES ALONE" 
    for subj_tar in range(0,3):    
        dt1 = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['SUBJ_NB']==0) & (data['SUBJ_TARGET1']==subj_tar)]
        dt2 = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['SUBJ_NB']==1) & (data['SUBJ_TARGET2']==subj_tar)]      
        data_temp = pandas.concat([dt1,dt2])
        df1 = data_temp[data_temp['FINAL_CHOICE']==320].reset_index()
        df2 = data_temp[data_temp['FINAL_CHOICE']==640].reset_index()
        n1 = len(df1)
        n2 = len(df2)
        traj_times_t1 = [0]*n1
        traj_times_t2 = [0]*n2       
        for i in range(0,n1):
            traj_times_t1[i] = df1['END_TIME'][i] - df1['ST_TIME'][i]
        for i in range(0,n2):
            traj_times_t2[i] = df2['END_TIME'][i] - df2['ST_TIME'][i] 
        print 'target : ', subj_tar, 'final choice : 1  ', np.mean(traj_times_t1), n1
        print 'target : ', subj_tar, 'final choice : 2  ', np.mean(traj_times_t2), n2            
        print "t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_t1, traj_times_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_t1, traj_times_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_t1, traj_times_t2),5)


    print "\nCOMPLETION TIME HFO"   
    dt_same = data[(data['EXP_COND']=='HFO') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==data['SUBJ_TARGET1'])]
    dt_one = data[(data['EXP_COND']=='HFO') & (data['IS_TRAINING']==0) & ((data['SUBJ_TARGET1']==0) | (data['SUBJ_TARGET2']==0))]      
#        dt_oppo = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==data['SUBJ_TARGET1']) & (data['SUBJ_TARGET1']*data['SUBJ_TARGET2']!=0)]
    df_s_1 = dt_same[dt_same['FINAL_CHOICE']==320].reset_index()
    df_s_2 = dt_same[dt_same['FINAL_CHOICE']==640].reset_index()
    df_o_1 = dt_one[dt_one['FINAL_CHOICE']==320].reset_index()
    df_o_2 = dt_one[dt_one['FINAL_CHOICE']==640].reset_index()        
    ns1 = len(df_s_1)
    ns2 = len(df_s_2)
    no1 = len(df_o_1)
    no2 = len(df_o_2)
    traj_times_s_t1 = [0]*ns1
    traj_times_s_t2 = [0]*ns2 
    traj_times_o_t1 = [0]*no1 
    traj_times_o_t2 = [0]*no2     
    for i in range(0,ns1):
        traj_times_s_t1[i] = df_s_1['END_TIME'][i] - df_s_1['ST_TIME'][i]
    for i in range(0,ns2):
        traj_times_s_t2[i] = df_s_2['END_TIME'][i] - df_s_2['ST_TIME'][i] 
    for i in range(0,no1):
        traj_times_o_t1[i] = df_o_1['END_TIME'][i] - df_o_1['ST_TIME'][i]
    for i in range(0,no2):
        traj_times_o_t2[i] = df_o_2['END_TIME'][i] - df_o_2['ST_TIME'][i] 
    print 'target : SAME, final choice : 1  ', np.mean(traj_times_s_t1), ns1
    print 'target : SAME, final choice : 2  ', np.mean(traj_times_s_t2), ns2 
    print 'target : ONE, final choice : 1  ', np.mean(traj_times_o_t1), no1
    print 'target : ONE, final choice : 2  ', np.mean(traj_times_o_t2), no2           
    print "SAME, t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_s_t1, traj_times_s_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t1, traj_times_s_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t1, traj_times_s_t2),5)
    print "ONE, t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_o_t1, traj_times_o_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_o_t1, traj_times_o_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_o_t1, traj_times_o_t2),5)
    print "t1, SAME vs ONE\tt-value: " , round(stats.ttest_ind(traj_times_s_t1, traj_times_o_t1)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t1, traj_times_o_t1)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t1, traj_times_o_t1),5)
    print "t2, SAME vs ONE\tt-value: " , round(stats.ttest_ind(traj_times_s_t2, traj_times_o_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t2, traj_times_o_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t2, traj_times_o_t2),5)


    print "\nCOMPLETION TIME HFOP"   
    dt_same = data[(data['EXP_COND']=='HFOP') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==data['SUBJ_TARGET1'])]
    dt_one = data[(data['EXP_COND']=='HFOP') & (data['IS_TRAINING']==0) & ((data['SUBJ_TARGET1']==0) | (data['SUBJ_TARGET2']==0))]      
#        dt_oppo = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['SUBJ_TARGET1']==data['SUBJ_TARGET1']) & (data['SUBJ_TARGET1']*data['SUBJ_TARGET2']!=0)]
    df_s_1 = dt_same[dt_same['FINAL_CHOICE']==320].reset_index()
    df_s_2 = dt_same[dt_same['FINAL_CHOICE']==640].reset_index()
    df_o_1 = dt_one[dt_one['FINAL_CHOICE']==320].reset_index()
    df_o_2 = dt_one[dt_one['FINAL_CHOICE']==640].reset_index()        
    ns1 = len(df_s_1)
    ns2 = len(df_s_2)
    no1 = len(df_o_1)
    no2 = len(df_o_2)
    traj_times_s_t1 = [0]*ns1
    traj_times_s_t2 = [0]*ns2 
    traj_times_o_t1 = [0]*no1 
    traj_times_o_t2 = [0]*no2     
    for i in range(0,ns1):
        traj_times_s_t1[i] = df_s_1['END_TIME'][i] - df_s_1['ST_TIME'][i]
    for i in range(0,ns2):
        traj_times_s_t2[i] = df_s_2['END_TIME'][i] - df_s_2['ST_TIME'][i] 
    for i in range(0,no1):
        traj_times_o_t1[i] = df_o_1['END_TIME'][i] - df_o_1['ST_TIME'][i]
    for i in range(0,no2):
        traj_times_o_t2[i] = df_o_2['END_TIME'][i] - df_o_2['ST_TIME'][i] 
    print 'target : SAME, final choice : 1  ', np.mean(traj_times_s_t1), ns1
    print 'target : SAME, final choice : 2  ', np.mean(traj_times_s_t2), ns2 
    print 'target : ONE, final choice : 1  ', np.mean(traj_times_o_t1), no1
    print 'target : ONE, final choice : 2  ', np.mean(traj_times_o_t2), no2           
    print "SAME, t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_s_t1, traj_times_s_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t1, traj_times_s_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t1, traj_times_s_t2),5)
    print "ONE, t1 vs t2\tt-value: " , round(stats.ttest_ind(traj_times_o_t1, traj_times_o_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_o_t1, traj_times_o_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_o_t1, traj_times_o_t2),5)
    print "t1, SAME vs ONE\tt-value: " , round(stats.ttest_ind(traj_times_s_t1, traj_times_o_t1)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t1, traj_times_o_t1)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t1, traj_times_o_t1),5)
    print "t2, SAME vs ONE\tt-value: " , round(stats.ttest_ind(traj_times_s_t2, traj_times_o_t2)[0], 5), "\tp-value :", round(stats.ttest_ind(traj_times_s_t2, traj_times_o_t2)[1],5), "\td-value :", round(cohenns_d(traj_times_s_t2, traj_times_o_t2),5)


#    n=0
#    axs = [0]*6
#    colors = [(0, 0, 1) , (0,0,0.5), (0, 1, 0), (0, 0.5, 0), (1, 0, 0), (0.5, 0, 0)] 
#    for subj_nb in range(0,2):
#        fig = plt.figure()
#        axs[n] = fig.add_subplot(111)
#        data_temp1 = data[(data['EXP_COND']=='ALONE') & (data['SUBJ_NB']==subj_nb) & (data['FINAL_CHOICE']==320)].reset_index()  
#        for i in range(0, len(data_temp1)):            
#            axs[n].plot(i,data_temp1['END_TIME'][i]-data_temp1['ST_TIME'][i],color=colors[n],marker='x')
#        data_temp2 = data[(data['EXP_COND']=='ALONE') & (data['SUBJ_NB']==subj_nb) & (data['FINAL_CHOICE']==640)].reset_index()  
#        for i in range(0, len(data_temp2)):            
#            axs[n].plot(i,data_temp2['END_TIME'][i]-data_temp2['ST_TIME'][i],color=colors[n+1],marker='+')            
#        n+=1
    


       
    print "\nACCURACY : mean T1, std T1, mean T2, std T2"    
    data_temp_t1 = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==320)].reset_index()
    acc_t1 = []
    for i in range (0, len(data_temp_t1)):
        if data_temp_t1['SUBJ_NB'][i]==0:
            acc_t1.append(abs(data_temp_t1['FINAL_POS1'][i] - data_temp_t1['FINAL_CHOICE'][i]))
        else:
            acc_t1.append(abs(data_temp_t1['FINAL_POS2'][i] - data_temp_t1['FINAL_CHOICE'][i]))
            
    data_temp_t2 = data[(data['EXP_COND']=='ALONE') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==640)].reset_index()
    acc_t2 = []
    for i in range (0, len(data_temp_t2)):
        if data_temp_t1['SUBJ_NB'][i]==0:
            acc_t2.append(abs(data_temp_t2['FINAL_POS1'][i] - data_temp_t2['FINAL_CHOICE'][i]))
        else:
            acc_t2.append(abs(data_temp_t2['FINAL_POS2'][i] - data_temp_t2['FINAL_CHOICE'][i]))    
    
    print "ALONE", np.mean(acc_t1), np.std(acc_t1), np.mean(acc_t2) , np.std(acc_t2)   
 
   
    data_temp_t1 = data[(data['EXP_COND']=='HFO') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==320)].reset_index()
    acc_t1 = []
    for i in range (0, len(data_temp_t1)):
        acc_t1.append(abs(float(data_temp_t1['FINAL_POSC'][i]) - data_temp_t1['FINAL_CHOICE'][i]))
            
    data_temp_t2 = data[(data['EXP_COND']=='HFO') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==640)].reset_index()
    acc_t2 = []
    for i in range (0, len(data_temp_t2)):
            acc_t2.append(abs(float(data_temp_t2['FINAL_POSC'][i]) - data_temp_t2['FINAL_CHOICE'][i]))
    
    print"HFO",  np.mean(acc_t1), np.std(acc_t1), np.mean(acc_t2) , np.std(acc_t2)     
 


    data_temp_t1 = data[(data['EXP_COND']=='HFOP') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==320)].reset_index()
    acc_t1 = []
    for i in range (0, len(data_temp_t1)):
        acc_t1.append(abs(float(data_temp_t1['FINAL_POSC'][i]) - data_temp_t1['FINAL_CHOICE'][i]))
            
    data_temp_t2 = data[(data['EXP_COND']=='HFOP') & (data['IS_TRAINING']==0) & (data['FINAL_CHOICE']==640)].reset_index()
    acc_t2 = []
    for i in range (0, len(data_temp_t2)):
            acc_t2.append(abs(float(data_temp_t2['FINAL_POSC'][i]) - data_temp_t2['FINAL_CHOICE'][i]))
    
    print "HFOP", np.mean(acc_t1), np.std(acc_t1), np.mean(acc_t2) , np.std(acc_t2)         
    
    
    
    plt.show()
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