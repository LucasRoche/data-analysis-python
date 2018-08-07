# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 14:46:51 2018

@author: lucas
"""

from postTrait_Module import *
import matplotlib.pyplot as plt
from matplotlib import cm
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
import scipy.stats as ss
import scipy.optimize as so

def main():
#    root = Tk()
#    root.withdraw()
#    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
#    file_names = root.tk.splitlist(file_names)
#    root.destroy()
    plot = 0
    
#    app = wx.App(0)
#    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/home/lucas/Documents/Manip/",  # defaultPath="C:/Users/users/Desktop/",
#                         agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)    
#    if dlg.ShowModal() != wx.ID_OK:
#        print("You Cancelled The Dialog!")
#        dlg.Destroy()    
#    paths = dlg.GetPaths()    
#    dlg.Destroy()
#    app.MainLoop()
    paths = [u'Home directory/Documents/Manip/Gabor/madani+samiel']
    
    DATA = pandas.DataFrame(data={'SUBJ_NAMES' : [], 'IS_TRAINING':[], 'TRIAL_NB' : [], 'TARGET_STIMULUS' : [], 'CHOICE' : [], 'CHOICE_TIME': [], 'TARGET_CONTRAST' : [], 'TARGET_POS' : []})

    colors = [(0, 0, 1), (1, 1, 0),  (0, 0, 0), (0, 0, 1), (1, 0, 0),  (0, 0, 0)]   
    
    ###### EXPE #####################################################################################################
    for path in enumerate(paths):
        directory= path[1].replace('Home directory','/home/lucas')
        filesToAdd = os.listdir(directory)
        
        fileName  =[]
        fileType = []
        date = []
        isTraining = []
        for file in filesToAdd:
            DataClass = FileData(directory + '/' + file)
            if DataClass.fileName.find('_ROBOT_')!=-1 or DataClass.fileName.find('~')!=-1:
                continue
            fileName.append(str(DataClass.fileName))
            fileType.append(DataClass.fileType)
            date.append(DataClass.fileDate)
        df = pandas.DataFrame(data={'fileName': fileName, 'fileType': fileType, 'date':date}) 
        df = df.sort_values(by=['fileType', 'date'])
        tempType = ''
        tempCount = 0
        expCond=[]
        for f in df['fileType']:
            if f != tempType:
                expCond.append(f)
                tempCount = 0
            if tempCount < 1:
                isTraining.append(1)
            else:
                isTraining.append(0)
            tempType = f
            tempCount +=1
                
        df['isTraining'] = isTraining
#        print df
        k=0
        for f in df['fileName']:
            print f
            DataClass = FileData(f)
            DataClass.getDataFromUIFile()
            n= len(DataClass.UIG_TrialNumber)
            tempdf = pandas.DataFrame(data={'SUBJ_NAMES' : [DataClass.SUBJECT_NAMES]*n, 'IS_TRAINING': [isTraining[k]]*n, 'TRIAL_NB' : DataClass.UIG_TrialNumber, 'TARGET_STIMULUS' : DataClass.UIG_TargetStimulus, 'CHOICE' : reverseDoubleList(DataClass.UIG_ChoiceMade), 'CHOICE_TIME': reverseDoubleList(DataClass.UIG_ChoiceTime), 'TARGET_CONTRAST' : DataClass.UIG_TargetContrast, 'TARGET_POS' : DataClass.UIG_TargetPos})
#            print tempdf            
            DATA = DATA.append(tempdf,ignore_index=True) 
            k+=1
        subj_names = [[],[]]
        file_counter = 0

    print DATA
    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)   

#ADD DYAD NUMBER TO DATAFRAME
    dyads = [list(x) for x in set(tuple(x) for x in DATA['SUBJ_NAMES'])]
    dyad_number = []
    for i in range(len(DATA)):
        for d in dyads:
            if DATA['SUBJ_NAMES'][i]==d:
                dyad_number.append(dyads.index(d))
    DATA['DYAD_NUMBER'] = dyad_number

#ADD CONTRAST DIFFERENCES TO DATAFRAME    
    contrast = []
    for j in range(len(DATA)):
        if DATA['TARGET_CONTRAST'][j]==0:
            temp_c = 0.015
        elif DATA['TARGET_CONTRAST'][j]==1:
            temp_c = 0.035
        elif DATA['TARGET_CONTRAST'][j]==2:
            temp_c = 0.075
        elif DATA['TARGET_CONTRAST'][j]==3:
            temp_c = 0.15
        temp_c = sign(DATA['TARGET_STIMULUS'][j]-0.5)*temp_c
        contrast.append(temp_c)
    DATA['CONTRAST_DIFF'] = contrast   
    for e in list(set(DATA['CONTRAST_DIFF'])):
        print len(DATA[DATA['CONTRAST_DIFF']==e])
    
    s_dyad=[]
    s_min=[]
    s_max=[]
    probas_all=[]
    N=len(dyads)
    for i in range(N):
        print "Dyad num ", i, " : ", dyads[i]
        probas = [[],[],[]]
        bias=[0,0,0]
        variance=[0,0,0]
        slope=[0,0,0]
        lines = [0,0,0]
        contrasts = list(set(DATA['CONTRAST_DIFF']))
        contrasts.sort()       
        for cont in contrasts:
            prop=[0,0,0]
            df = DATA[(DATA['DYAD_NUMBER']==i) & (DATA['CONTRAST_DIFF']==cont)].reset_index(drop=True)
#            print df
            for k in range(3):
                for j in range(len(df)):                
                    prop[k]+=float(df['CHOICE'][j][k])
                prop[k]/=len(df)
                probas[k].append(prop[k])

        plt.figure(i)
        plt.title(dyads[i][0]+" + "+dyads[i][1])  
        plt.axis([-0.2, 0.2, -0.05, 1.05])
        
        x = np.linspace(ss.norm.ppf(0.01), ss.norm.ppf(0.99), 1000)
        for k in range(3):
            fit, coeffs = so.curve_fit(cdf, contrasts, probas[k])
            bias[k]=fit[0]
            variance[k] =fit[1]
    #        plt.plot(x, ss.norm.cdf(x, loc=0, scale=variance),'r')
            slope[k] = 1/sqrt(2*np.pi*variance[k]**2)       
            lines[k],=plt.plot(x, ss.norm.cdf(x, loc=-bias[k], scale=variance[k]), color=colors[k])            
            plt.plot(contrasts, probas[k], 'o', color=colors[k])            
            if(k==2):
                print dyads[i]
            else:
                print dyads[i][k]
            print "bias = ", bias[k] , "\tvariance = ", variance[k], "\tslope = ", slope[k]
    #        print (ss.norm.cdf(contrasts[4], loc=-bias, scale=variance) - ss.norm.cdf(contrasts[3], loc=-bias, scale=variance))/(contrasts[4]-contrasts[3])
        if slope[0]>slope[1]:
            probas_all.append([probas[1],probas[0],probas[2]])
        else:                
            probas_all.append(probas)
        

        plt.legend(lines,[dyads[i][0], dyads[i][1], dyads[i][0]+" + "+dyads[i][1]], loc=4)

        s_min.append(min(slope[0],slope[1]))
        s_max.append(max(slope[0],slope[1]))
        s_dyad.append(slope[2])
        
    plt.figure()
    plt.title("comparisons")
    x= [s_min[i]/s_max[i] for i in range(N)]
    y = [s_dyad[i]/s_max[i] for i in range(N)]
    plt.plot(x,y,'o')
    plt.axis([0,1,0.5,1.5])
        
    print np.array(probas_all)
    print np.sum(probas_all, axis=0)/N
    probas_all = np.sum(probas_all, axis=0)/N
    plt.figure()
    plt.axis([-0.2, 0.2, -0.05, 1.05])
    plt.title("Average, N = " + str(N))    
    x = np.linspace(ss.norm.ppf(0.01), ss.norm.ppf(0.99), 1000)
    for k in range(3):
        fit, coeffs = so.curve_fit(cdf, contrasts, probas_all[k])
        bias[k]=fit[0]
        variance[k] =fit[1]
        lines[k],=plt.plot(x, ss.norm.cdf(x, loc=-bias[k], scale=variance[k]), color=colors[k+3])            
        plt.plot(contrasts, probas_all[k], 'o', color=colors[k+3])   
#        plt.plot(x, ss.norm.cdf(x, loc=0, scale=variance),'r')
        slope[k] = 1/sqrt(2*np.pi*variance[k]**2)        
        
#        print (ss.norm.cdf(contrasts[4], loc=-bias, scale=variance) - ss.norm.cdf(contrasts[3], loc=-bias, scale=variance))/(contrasts[4]-contrasts[3])
    plt.legend(lines,['mins','maxs','dyads'], loc=4)
#        print (ss.norm.cdf(contrasts[4], loc=-bias, scale=variance) - ss.norm.cdf(contrasts[3], loc=-bias, scale=variance))/(contrasts[4]-contrasts[3])
#        test = [0.0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8]
#        plt.plot(contrasts, test, 'x')
#        fit, coeffs = so.curve_fit(cdf, contrasts, test)
#        bias=fit[0]
#        variance =fit[1]
#        plt.plot(x, ss.norm.cdf(x, loc=-bias, scale=variance), 'g')
        
        

            
    plt.show(block='False')
         
def cdf(x, b, s):
    return ss.norm.cdf((x+b)/s)


def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1

def reverseDoubleList(A):
    B=[]
    C=[]
    for j in range(len(A[0])):
        for i in range(len(A)):
            B.append(A[i][j])
        C.append(B)
        B=[]
    return C
                
if __name__ == '__main__':
    main()