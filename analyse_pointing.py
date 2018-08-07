# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:50:56 2017

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

def main():
#    root = Tk()
#    root.withdraw()
#    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
#    file_names = root.tk.splitlist(file_names)
#    root.destroy()
    plot = 0
    
    app = wx.App(0)
    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/home/lucas/Documents/Manip/",  # defaultPath="C:/Users/users/Desktop/",
                         agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)    
    if dlg.ShowModal() != wx.ID_OK:
        print("You Cancelled The Dialog!")
        dlg.Destroy()    
    paths = dlg.GetPaths()    
    dlg.Destroy()
    app.MainLoop()
    
    DATA = pandas.DataFrame(data={'SUBJ_NB': [], 'SUBJ_NAME1' : [], 'SUBJ_NAME2' : [], 'IS_TRAINING':[] , 'EXP_COND' : [], 'TRIAL_NB' : [], 'ST_TIME' : [], 'END_TIME' : [], 'SUBJ_TARGET1' : [], 'SUBJ_TARGET2' : [], 'FINAL_CHOICE' : [], 'FINAL_POS1': [], 'FINAL_POS2': [], 'FINAL_POSC' : [], 'TARGET_WIDTH1' : [], 'TARGET_WIDTH2' : []})
    DATA_HIST = pandas.DataFrame(data={'SUBJ_NB':[], 'SUBJ_NAME1' : [], 'SUBJ_NAME2' : [], 'EXP_COND':[], 'HIST':[], 'TRIAL_NB' : [], 'IS_TRAINING':[]})
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
            if DataClass.fileName.find('_UI_')!=-1 or DataClass.fileName.find('~')!=-1:
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
            if tempCount < 2:
                isTraining.append(1)
            else:
                isTraining.append(0)
            tempType = f
            tempCount +=1
                
        df['isTraining'] = isTraining
        
        subj_names = [[],[]]
        file_counter = 0
        
        ###### COND #####################################################################################################
        for cond in expCond:
            
            
            figNb = 0
            nb_trial = 0
            n_subplots = len(df[df['fileType'] == cond])
            l=int(np.sqrt(n_subplots))
            if n_subplots-l*l == 0:
                i_subplots = l
                j_subplots = l
            elif n_subplots-l*l <= l:
                i_subplots = l
                j_subplots = l+1
            elif n_subplots-l*l > l:
                i_subplots = l+1
                j_subplots = l+1

            if plot:
                if cond == 'ALONE':            
                    axarr_pos = [[],[]]
                    axarr_vit = [[],[]]
                    f = [0]*4
                    
                    f[0], axarr_pos[0] = plt.subplots(i_subplots, j_subplots)
                    f[1], axarr_pos[1] = plt.subplots(i_subplots, j_subplots)
                    f[2], axarr_vit[0] = plt.subplots(i_subplots, j_subplots)
                    f[3], axarr_vit[1] = plt.subplots(i_subplots, j_subplots)
                     
                    axarr_pos[0] = np.matrix(axarr_pos[0])
                    axarr_pos[1] = np.matrix(axarr_pos[1])
                    axarr_vit[0] = np.matrix(axarr_vit[0])
                    axarr_vit[1] = np.matrix(axarr_vit[1])
                    
                else:
                    f[0], axarr_pos[0] = plt.subplots(i_subplots, j_subplots)
                    f[2], axarr_vit[0] = plt.subplots(i_subplots, j_subplots)
                     
                    axarr_pos[0] = np.matrix(axarr_pos[0])
                    axarr_vit[0] = np.matrix(axarr_vit[0])           
            
            nb_subjects = 2
            
            file_counter = 0
            
            hist_vit = [[],[],[]]
            hist_vit[0] = np.array([0]*101)
            hist_vit[1] = np.array([0]*101)
            hist_vit[2] = np.array([0]*101)
            ###### FILES #####################################################################################################
            for file in df[df['fileType'] == cond]['fileName']:
                print file
                DataClass = FileData(file)
                DataClass.getDataFromFile()
                N = len(DataClass.Time)
                DataClass.getDataFromUIFile()
                
                subj_names[0] = DataClass.SUBJECT_NAMES[0]
                subj_names[1] = DataClass.SUBJECT_NAMES[1]
                nb_subjects = DataClass.UINbSubjects
                
                if plot:
                    if cond == 'ALONE':
                        f[0].suptitle(subj_names[0])
                        f[1].suptitle(subj_names[1])
                        f[2].suptitle(subj_names[0])
                        f[3].suptitle(subj_names[1])
                    else:
                        f[0].suptitle(subj_names[0]+'+'+subj_names[1])
                        f[2].suptitle(subj_names[0]+'+'+subj_names[1])                  
                        
                nyq = 0.5*5000
                low = 10/nyq
            
                b, a =  sig.butter(6, low, btype = 'low')
                b2, a2 = sig.butter(2, 50/nyq, btype = 'low')                
        
                t0 = 0#int(2/DataClass.Time[N-1]*N)
                tf = N#int(25/DataClass.Time[N-1]*N)
        
            #Applying Butterworth filer to force signals        
                for1 = sig.lfilter(b, a, DataClass.Subj_for1)
                for2 = sig.lfilter(b, a, DataClass.Subj_for2)  
                
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
                    if cond == 'HFOP' or cond == 'HFO':
                        vitC[i] = 1./280*posC[i-4] - 4./105*posC[i-3] + 1./5*posC[i-2] - 4./5*posC[i-1] + 4./5*posC[i+1] - 1./5*posC[i+2] + 4./105*posC[i+3] - 1./280*posC[i+4]


                
                indices_trial = [0]
                indices_phase = [[],[]]
                indices_phase[0] = [0]
                indices_phase[1] = [0]
                for i in range(0, N-1):
                    if DataClass.TimeTrial[i] > 0.05 and DataClass.TimeTrial[i+1] < 0.05:
                        indices_trial.append(i+1)
                    if DataClass.TimePhase1[i] > 0.05 and DataClass.TimePhase1[i+1] < 0.05:
                        indices_phase[0].append(i+1)   
                    if DataClass.TimePhase2[i] > 0.05 and DataClass.TimePhase2[i+1] < 0.05:
                        indices_phase[1].append(i+1)       
        #        indices_trial.append(N-1)
                indices_phase[0].append(N-1)
                indices_phase[1].append(N-1)       
                
                
################## EXTRACT START AND END TIMES + VELOCITIES HISTOGRAMS
#######################"
                if cond=='ALONE':
                    for k in range(0,nb_subjects):
                        st_timesC = []
                        end_timesC = []
                        st_timesF = []
                        end_timesF = []                    
                        for i in range(0, len(DataClass.UITrialNumber)):
                            t0 = indices_trial[2*i+1]
                            tf = indices_phase[k][4*i+3]- DataClass.time2line(1)
                            tempST = 0
                            tempEND = 0
                            
                            if DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosC[i]:
                                final_target = DataClass.UITargetPosC[i]
                                target_width = DataClass.UITargetWidth[0]
                                for j in range(t0, tf):              
                                   if abs(pos[k][j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(pos[k][j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                       tempST = DataClass.Time[j-t0]
                                       tempEND = DataClass.Time[tf-t0]
                                       st_timesC.append(tempST)
                                       end_timesC.append(tempEND)
                                                
                            elif DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosF[i]:
                                final_target = DataClass.UITargetPosF[i]
                                target_width = DataClass.UITargetWidth[1]
                                for j in range(t0, tf):              
                                   if abs(pos[k][j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(pos[k][j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                       tempST = DataClass.Time[j-t0]
                                       tempEND = DataClass.Time[tf-t0]
                                       st_timesF.append(tempST)
                                       end_timesF.append(tempEND) 
                            else:
                                final_target = 0
                                target_width = 0
        
                            tempdf = pandas.DataFrame(data={'SUBJ_NB': [k], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])] , 'EXP_COND' : [DataClass.fileType], 'TRIAL_NB' : [file_counter], 'ST_TIME' : [tempST], 'END_TIME' : [tempEND],  'SUBJ_TARGET1' : [DataClass.UITargetSubj[0][i]], 'SUBJ_TARGET2' : [DataClass.UITargetSubj[1][i]], 'FINAL_CHOICE' : [DataClass.UIFinalChoice[k][i]], 'FINAL_POS1': [pos[0][tf+DataClass.time2line(1)]], 'FINAL_POS2': [pos[1][tf+DataClass.time2line(1)]], 'FINAL_POSC' : ['-'], 'TARGET_WIDTH1' : [DataClass.UITargetWidth[0][i]], 'TARGET_WIDTH2' : [DataClass.UITargetWidth[1][i]] })
                            DATA = DATA.append(tempdf, ignore_index=True)
                            
#                            if(not(int(df[df['fileName']==file]['isTraining']))):
#                                temp_hist, temp_bins = np.histogram([x for x in vit[k][t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
#                                hist_vit[k] = np.add(hist_vit[k], temp_hist)    
                            temp_hist, temp_bins = np.histogram([x for x in vit[k][t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
                            if np.sum(temp_hist)!=0:
                                temp_hist = [float(x)/float(np.sum(temp_hist)) for x in temp_hist]
                            else:
                                temp_hist = [float(x) for x in temp_hist]
                            tempdf = pandas.DataFrame(data={'SUBJ_NB':[k], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[temp_hist], 'TRIAL_NB' : [file_counter], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])]})
                            DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)   
                                
                elif cond=='HFOP':
                    st_timesC = []
                    end_timesC = []
                    st_timesF = []
                    end_timesF = []                    
                    for i in range(0, len(DataClass.UITrialNumber)):
                        t0 = indices_trial[2*i+1]
                        tf = indices_phase[0][4*i+3]- DataClass.time2line(1)
                        tempST = 0
                        tempEND = 0
                        
                        if DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosC[i]:
                            final_target = DataClass.UITargetPosC[i]
                            target_width = DataClass.UITargetWidth[0]
                            for j in range(t0, tf):              
                               if abs(posC[j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(posC[j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                   tempST = DataClass.Time[j-t0]
                                   tempEND = DataClass.Time[tf-t0]
                                   st_timesC.append(tempST)
                                   end_timesC.append(tempEND)
                                            
                        elif DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosF[i]:
                            final_target = DataClass.UITargetPosF[i]
                            target_width = DataClass.UITargetWidth[1]
                            for j in range(t0, tf):              
                               if abs(posC[j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(posC[j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                   tempST = DataClass.Time[j-t0]
                                   tempEND = DataClass.Time[tf-t0]
                                   st_timesF.append(tempST)
                                   end_timesF.append(tempEND) 
                        else:
                            final_target = 0
                            target_width = 0
                            
                        tempdf = pandas.DataFrame(data={'SUBJ_NB': [2], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])] , 'EXP_COND' : [DataClass.fileType], 'TRIAL_NB' : [file_counter], 'ST_TIME' : [tempST], 'END_TIME' : [tempEND], 'SUBJ_TARGET1' : [DataClass.UITargetSubj[0][i]], 'SUBJ_TARGET2' : [DataClass.UITargetSubj[1][i]], 'FINAL_CHOICE' : [DataClass.UIFinalChoice[0][i]], 'FINAL_POS1': [pos[0][tf+DataClass.time2line(1)]], 'FINAL_POS2': [pos[1][tf+DataClass.time2line(1)]], 'FINAL_POSC' : [posC[tf+DataClass.time2line(1)]], 'TARGET_WIDTH1' : [DataClass.UITargetWidth[0][i]], 'TARGET_WIDTH2' : [DataClass.UITargetWidth[1][i]]})
                        DATA = DATA.append(tempdf, ignore_index=True)
                        
#                        if(not(int(df[df['fileName']==file]['isTraining']))):
#                            temp_hist, temp_bins = np.histogram([x for x in vitC[t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
#                            hist_vit[2] = np.add(hist_vit[2], temp_hist)
                        temp_hist, temp_bins = np.histogram([x for x in vitC[t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
                        if np.sum(temp_hist)!=0:
                            temp_hist = [float(x)/float(np.sum(temp_hist)) for x in temp_hist]
                        else:
                            temp_hist = [float(x) for x in temp_hist]
                        tempdf = pandas.DataFrame(data={'SUBJ_NB':[2], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[temp_hist], 'TRIAL_NB' : [file_counter], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])]})
                        DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)  


                elif cond=='HFO':
                    st_timesC = []
                    end_timesC = []
                    st_timesF = []
                    end_timesF = []                    
                    for i in range(0, len(DataClass.UITrialNumber)):
                        t0 = indices_trial[2*i+1]
                        tf = indices_phase[0][4*i+3]- DataClass.time2line(1)
                        tempST = 0
                        tempEND = 0
                        
                        if DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosC[i]:
                            final_target = DataClass.UITargetPosC[i]
                            target_width = DataClass.UITargetWidth[0]
                            for j in range(t0, tf):              
                               if abs(posC[j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(posC[j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                   tempST = DataClass.Time[j-t0]
                                   tempEND = DataClass.Time[tf-t0]
                                   st_timesC.append(tempST)
                                   end_timesC.append(tempEND)
                                            
                        elif DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosF[i]:
                            final_target = DataClass.UITargetPosF[i]
                            target_width = DataClass.UITargetWidth[1]
                            for j in range(t0, tf):              
                               if abs(posC[j-1] - DataClass.UIStartPos[i]) < DataClass.UIStartWidth and abs(posC[j] - DataClass.UIStartPos[i]) > DataClass.UIStartWidth:
                                   tempST = DataClass.Time[j-t0]
                                   tempEND = DataClass.Time[tf-t0]
                                   st_timesF.append(tempST)
                                   end_timesF.append(tempEND) 
                        else:
                            final_target = 0
                            target_width = 0
                            
                        tempdf = pandas.DataFrame(data={'SUBJ_NB': [2], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])] , 'EXP_COND' : [DataClass.fileType], 'TRIAL_NB' : [file_counter], 'ST_TIME' : [tempST], 'END_TIME' : [tempEND], 'SUBJ_TARGET1' : [DataClass.UITargetSubj[0][i]], 'SUBJ_TARGET2' : [DataClass.UITargetSubj[1][i]], 'FINAL_CHOICE' : [DataClass.UIFinalChoice[0][i]], 'FINAL_POS1': [pos[0][tf+DataClass.time2line(1)]], 'FINAL_POS2': [pos[1][tf+DataClass.time2line(1)]], 'FINAL_POSC' : [posC[tf+DataClass.time2line(1)]], 'TARGET_WIDTH1' : [DataClass.UITargetWidth[0][i]], 'TARGET_WIDTH2' : [DataClass.UITargetWidth[1][i]]})
                        DATA = DATA.append(tempdf, ignore_index=True)
                        
#                        if(not(int(df[df['fileName']==file]['isTraining']))):
#                            temp_hist, temp_bins = np.histogram([x for x in vit[0][t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
#                            hist_vit[0] = np.add(hist_vit[0], temp_hist)
#                            temp_hist, temp_bins = np.histogram([x for x in vit[1][t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
#                            hist_vit[1] = np.add(hist_vit[1], temp_hist)  
#                            temp_hist, temp_bins = np.histogram([x for x in vitC[t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
#                            hist_vit[2] = np.add(hist_vit[2], temp_hist)
                        
                        for k in range(0, nb_subjects):
                            temp_hist, temp_bins = np.histogram([x for x in vit[k][t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
                            if np.sum(temp_hist)!=0:
                                temp_hist = [float(x)/float(np.sum(temp_hist)) for x in temp_hist]
                            else:
                                temp_hist = [float(x) for x in temp_hist]
                            tempdf = pandas.DataFrame(data={'SUBJ_NB':[k], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[temp_hist], 'TRIAL_NB' : [file_counter], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])]})
                            DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)
                            
                        temp_hist, temp_bins = np.histogram([x for x in vitC[t0:tf] if abs(x)>0.01], bins=101, range=(-0.75,1.5))
                        temp_hist = [float(x)/float(np.sum(temp_hist)) for x in temp_hist]
                        tempdf = pandas.DataFrame(data={'SUBJ_NB':[2], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[temp_hist], 'TRIAL_NB' : [file_counter], 'IS_TRAINING':[int(df[df['fileName']==file]['isTraining'])]})
                        DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)                                                      
#                print "Subject : ", k
#                print "Mean Start Time Target C : ", np.mean(st_timesC)
#                print "Mean End Time Target C : ", np.mean(end_timesC)
#                print "Mean Start Time Target F : ", np.mean(st_timesF)
#                print "Mean End Time Target F : ", np.mean(end_timesF)
#                print "Mean Traj Time Target C : ", np.mean([end_timesC[i] - st_timesC[i] for i in range(0, len(st_timesC))])
#                print "Mean Traj Time Target F : ", np.mean([end_timesF[i] - st_timesF[i] for i in range(0, len(st_timesF))])
#                print ("\n")                
 
########################PLOTS
#########################

                if plot:            
                    if cond == 'ALONE':
                        ## PLOT POSITIONS
                        pos_targetC = [DataClass.UITargetPosC[0]]*(tf-t0)       
                        pos_targetF = [DataClass.UITargetPosF[0]]*(tf-t0)
                        pos_start = [DataClass.UIStartPos[0]]*(tf-t0)
                        width_tC = DataClass.UITargetWidthC
                        width_tF = DataClass.UITargetWidthF
                        for k in range(0,nb_subjects):
                            plt.figure(f[k].number)
                            figNb+=1
                #            axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots] = plt.subplot(111)
                            axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].axis([0,  DataClass.WINDOW_WIDTH, 0, 2])
                            temp1 = []
                            temp2 = []        
                            for i in range(0, len(DataClass.UITrialNumber)):
                                t0 = indices_trial[2*i+1]
                                tf = indices_phase[k][4*i+3]- DataClass.time2line(1)
                                
                                time_local = [ x - DataClass.Time[t0]  for x in DataClass.Time[t0:tf]]
                    
                                pos_targetC = [DataClass.UITargetPosC[0]]*(tf-t0)       
                                pos_targetF = [DataClass.UITargetPosF[0]]*(tf-t0)
                                pos_start = [DataClass.UIStartPos[0]]*(tf-t0)            
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_targetC, time_local,'k')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-width_tC for x in pos_targetC], time_local,'k--')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+width_tC for x in pos_targetC], time_local,'k--')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_targetF, time_local,'k')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-width_tF for x in pos_targetF], time_local,'k--')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+width_tF for x in pos_targetF], time_local,'k--')     
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_start, time_local,'k')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-10 for x in pos_start], time_local,'k--')
                                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+10 for x in pos_start], time_local,'k--')  
                    
                                
                                if DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosC[i]:
                    #                axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0], DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0]], 'r--') 
                                    axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[tf]-DataClass.Time[t0], DataClass.Time[tf]-DataClass.Time[t0]], 'g--') 
                                    axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos[k][t0:tf], time_local,'g')
                                    temp1.append(tf-t0)
                                elif DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosF[i]:
                                    axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[tf]-DataClass.Time[t0], DataClass.Time[tf]-DataClass.Time[t0]], 'b--') 
                                    axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos[k][t0:tf], time_local,'b')
                                    temp2.append(tf-t0)
                                    
                            axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[int(np.mean(temp1))], DataClass.Time[int(np.mean(temp1))]], 'g-', linewidth=3)
                            axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[int(np.mean(temp2))], DataClass.Time[int(np.mean(temp2))]], 'b-', linewidth=3)
                            
                            
                        ## PLOT VITESSES
                        for k in range(0,nb_subjects):
                            plt.figure(f[k+2].number)
                            figNb+=1
                            for i in range(0, len(DataClass.UITrialNumber)):
                                t0 = indices_trial[2*i+1]
                                tf = indices_phase[k][4*i+3]- DataClass.time2line(1)
                                
                                time_local = [ x - DataClass.Time[t0]  for x in DataClass.Time[t0:tf]]
                                  
                                if DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosC[i]:
                                    axarr_vit[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(vit[k][t0:tf], time_local,'g')
                                    temp1.append(tf-t0)
                                elif DataClass.UIFinalChoice[k][i] == DataClass.UITargetPosF[i]:
                                    axarr_vit[k][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(vit[k][t0:tf], time_local,'b')
                                    temp2.append(tf-t0)
                                    
                    elif cond == 'HFOP':
                        ## PLOT POSITIONS
                        pos_targetC = [DataClass.UITargetPosC[0]]*(tf-t0)       
                        pos_targetF = [DataClass.UITargetPosF[0]]*(tf-t0)
                        pos_start = [DataClass.UIStartPos[0]]*(tf-t0)
                        width_tC = DataClass.UITargetWidthC
                        width_tF = DataClass.UITargetWidthF
    
                        plt.figure(f[0].number)
                        figNb+=1
            #            axarr_pos[k][int(nb_trial/j_subplots), nb_trial%j_subplots] = plt.subplot(111)
                        axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].axis([0,  DataClass.WINDOW_WIDTH, 0, 2])
                        temp1 = []
                        temp2 = []        
                        for i in range(0, len(DataClass.UITrialNumber)):
                            t0 = indices_trial[2*i+1]
                            tf = indices_phase[0][4*i+3]- DataClass.time2line(1)
                            
                            time_local = [ x - DataClass.Time[t0]  for x in DataClass.Time[t0:tf]]
                
                            pos_targetC = [DataClass.UITargetPosC[0]]*(tf-t0)       
                            pos_targetF = [DataClass.UITargetPosF[0]]*(tf-t0)
                            pos_start = [DataClass.UIStartPos[0]]*(tf-t0)            
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_targetC, time_local,'k')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-width_tC for x in pos_targetC], time_local,'k--')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+width_tC for x in pos_targetC], time_local,'k--')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_targetF, time_local,'k')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-width_tF for x in pos_targetF], time_local,'k--')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+width_tF for x in pos_targetF], time_local,'k--')     
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(pos_start, time_local,'k')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x-10 for x in pos_start], time_local,'k--')
                            axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([x+10 for x in pos_start], time_local,'k--')  
                
                            
                            if DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosC[i]:
                #                axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0], DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0]], 'r--') 
                                axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[tf]-DataClass.Time[t0], DataClass.Time[tf]-DataClass.Time[t0]], 'g--') 
                                axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(posC[t0:tf], time_local,'g')
                                temp1.append(tf-t0)
                            elif DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosF[i]:
                                axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[tf]-DataClass.Time[t0], DataClass.Time[tf]-DataClass.Time[t0]], 'b--') 
                                axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(posC[t0:tf], time_local,'b')
                                temp2.append(tf-t0)
                                
                        axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[int(np.mean(temp1))], DataClass.Time[int(np.mean(temp1))]], 'g-', linewidth=3)
                        axarr_pos[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot([0,  DataClass.WINDOW_WIDTH],[DataClass.Time[int(np.mean(temp2))], DataClass.Time[int(np.mean(temp2))]], 'b-', linewidth=3)
                            
                            
                        ## PLOT VITESSES
                        plt.figure(f[2].number)
                        figNb+=1
                        for i in range(0, len(DataClass.UITrialNumber)):
                            t0 = indices_trial[2*i+1]
                            tf = indices_phase[0][4*i+3]- DataClass.time2line(1)
                            
                            time_local = [ x - DataClass.Time[t0]  for x in DataClass.Time[t0:tf]]
                              
                            if DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosC[i]:
                                axarr_vit[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(vitC[t0:tf], time_local,'g')
                                temp1.append(tf-t0)
                            elif DataClass.UIFinalChoice[0][i] == DataClass.UITargetPosF[i]:
                                axarr_vit[0][int(nb_trial/j_subplots), nb_trial%j_subplots].plot(vitC[t0:tf], time_local,'b')
                                temp2.append(tf-t0)
                                
        
                file_counter+=1
                nb_trial+=1
                               
            ###### FILES     #####################################################################################################
#            if cond=='ALONE':
#                for k in range(0, nb_subjects):
#                    hist_vit[k] = [float(x)/float(np.sum(hist_vit[k])) for x in hist_vit[k]]
#                    tempdf = pandas.DataFrame(data={'SUBJ_NB':[k], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[hist_vit[k]]})
#                    DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)    
#            elif cond=='HFOP':
#                hist_vit[2] = [float(x)/float(np.sum(hist_vit[2])) for x in hist_vit[2]]
#                tempdf = pandas.DataFrame(data={'SUBJ_NB':[2], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[hist_vit[2]]})
#                DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)              
#            elif cond=='HFO':
#                for k in range(0, nb_subjects+1):
#                    hist_vit[k] = [float(x)/float(np.sum(hist_vit[k])) for x in hist_vit[k]]
#                    tempdf = pandas.DataFrame(data={'SUBJ_NB':[k], 'SUBJ_NAME1':[subj_names[0]], 'SUBJ_NAME2': [subj_names[1]], 'EXP_COND':[cond], 'HIST':[hist_vit[k]]})
#                    DATA_HIST = DATA_HIST.append(tempdf,ignore_index=True)                 
        ###### COND #####################################################################################################
        
        
    ###### EXPE  #####################################################################################################
    print DATA
    
    print DATA_HIST  
#    for i in range(0, len(DATA_HIST['HIST'])):
#        plt.figure()
#        if(DATA_HIST['SUBJ_NB'][i]==0):
#            plt.title(DATA_HIST['EXP_COND'][i] + ' : ' + DATA_HIST['SUBJ_NAME1'][i])
#        elif(DATA_HIST['SUBJ_NB'][i]==1):
#            plt.title(DATA_HIST['EXP_COND'][i] + ' : ' + DATA_HIST['SUBJ_NAME2'][i]) 
#        elif(DATA_HIST['SUBJ_NB'][i]==2):
#            plt.title(DATA_HIST['EXP_COND'][i] + ' : ' + DATA_HIST['SUBJ_NAME1'][i]+'+'+DATA_HIST['SUBJ_NAME2'][i])            
#        plt.plot(np.linspace(-0.75, 1.5, 101), DATA_HIST['HIST'][i])

    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)   
    DATA.to_csv('~/Documents/Manip/DATA_POINTING_choices_'+date+'.csv')
    DATA_HIST.to_csv('~/Documents/Manip/DATA_POINTING_histograms_'+date+'.csv')
            
    plt.show(block='False')
    
    

        

        
        #Create parameters for Butterworth filter (Low-pass, 6th Order)

    
    #        DataClass.Subj_for1 = sig.lfilter(b, a, DataClass.Subj_for1)
    #        DataClass.Subj_for2 = sig.lfilter(b, a, DataClass.Subj_for2)
    #        DataClass.Curs_pos = sig.lfilter(b, a, DataClass.Curs_pos)
    #        DataClass.Subj_pos1 = sig.lfilter(b, a, DataClass.Subj_pos1)
    #        DataClass.Subj_pos2 = sig.lfilter(b, a, DataClass.Subj_pos2)
    

        
        
#        print len(indices_trial), indices_trial
#        print len(indices_phase[0]), indices_phase[0]
#        print len(indices_phase[1]), indices_phase[1]
        
        
        
    #Plotting results
#        fig = plt.figure(figNb)
#        figNb+=1
#        ax1 = plt.subplot(111)
##        ax2 = ax1.twiny()
##        ax3 = ax1.twiny()
#        ax1.set_ylabel('Time (s)')
#        ax1.set_xlabel('Position (deg)')
##        ax2.set_xlabel('Force (N)')
#        ax1.axis([0, DataClass.WINDOW_WIDTH, DataClass.Time[t0], DataClass.Time[tf-1]])
##        ax2.axis([ -2.5, 2.5, DataClass.Time[t0], DataClass.Time[tf-1]])
##        ax3.axis([ -0.5, 1.5, DataClass.Time[t0], DataClass.Time[tf-1]])
#        
#        ax1.plot(pos_targetC, DataClass.Time[t0:tf],'k')
#        ax1.plot([x-width_tC for x in pos_targetC], DataClass.Time[t0:tf],'k--')
#        ax1.plot([x+width_tC for x in pos_targetC], DataClass.Time[t0:tf],'k--')
#        ax1.plot(pos_targetF, DataClass.Time[t0:tf],'k')
#        ax1.plot([x-width_tF for x in pos_targetF], DataClass.Time[t0:tf],'k--')
#        ax1.plot([x+width_tF for x in pos_targetF], DataClass.Time[t0:tf],'k--')     
#        ax1.plot(pos_start, DataClass.Time[t0:tf],'k')
#        ax1.plot([x-10 for x in pos_start], DataClass.Time[t0:tf],'k--')
#        ax1.plot([x+10 for x in pos_start], DataClass.Time[t0:tf],'k--')         
#        
#
#        for i in range(0, len(indices_phase[0])):
#            ax1.plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_phase[0][i]], DataClass.Time[indices_phase[0][i]]], 'b--')
#        for i in range(0, len(indices_phase[0])):
#            ax1.plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_phase[1][i]], DataClass.Time[indices_phase[1][i]]], 'g--') 
#        for i in range(0, len(indices_trial)):
#            ax1.plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_trial[i]], DataClass.Time[indices_trial[i]]], 'r--')    
#            
#        try:
#            ax1.plot(DataClass.Curs_pos1[t0:tf], DataClass.Time[t0:tf],'b')
#            ax1.plot(DataClass.Curs_pos2[t0:tf], DataClass.Time[t0:tf],'g')
#        except:
#            ax1.plot(DataClass.Curs_pos[t0:tf], DataClass.Time[t0:tf],'r')
#
#
#        fig2 = plt.figure(figNb)
#        figNb+=1
#        ax2 = plt.subplot(111)
#        
#        for i in range(0, len(indices_trial)-1):
#            t0 = indices_trial[i]
#            tf = indices_trial[i+1]
#            
#            time_local = [ x - DataClass.Time[t0]  for x in DataClass.Time[t0:tf]]
#
#            pos_targetC = [DataClass.UITargetPosC[0]-DataClass.WINDOW_WIDTH/2]*(tf-t0)       
#            pos_targetF = [DataClass.UITargetPosF[0]-DataClass.WINDOW_WIDTH/2]*(tf-t0)
#            pos_start = [DataClass.UIStartPos[0]-DataClass.WINDOW_WIDTH/2]*(tf-t0)            
#            ax2.plot(pos_targetC, time_local,'k')
#            ax2.plot([x-width_tC for x in pos_targetC], time_local,'k--')
#            ax2.plot([x+width_tC for x in pos_targetC], time_local,'k--')
#            ax2.plot(pos_targetF, time_local,'k')
#            ax2.plot([x-width_tF for x in pos_targetF], time_local,'k--')
#            ax2.plot([x+width_tF for x in pos_targetF], time_local,'k--')     
#            ax2.plot(pos_start, time_local,'k')
#            ax2.plot([x-10 for x in pos_start], time_local,'k--')
#            ax2.plot([x+10 for x in pos_start], time_local,'k--')  
#        
#            ax2.plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_trial[i+1]]-DataClass.Time[t0], DataClass.Time[indices_trial[i+1]]-DataClass.Time[t0]], 'r--') 
#            ax2.plot([0, DataClass.WINDOW_WIDTH],[DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0], DataClass.Time[indices_phase[0][2*i+1]]-DataClass.Time[t0]], 'g--') 
#            
#            try:
#                ax2.plot(DataClass.Curs_pos1[t0:tf], time_local,'b')
#                ax2.plot(DataClass.Curs_pos2[t0:tf], time_local,'g')
#            except:
#                ax2.plot(DataClass.Curs_pos[t0:tf], time_local,'r')
#        plt.show()

      

#        print len(indices_phase[0]), len(indices_trial)
#        indices_trial = [indices_trial[i] for i in range(0, len(indices_trial)) if (indices_phase[0][2*i+1] < np.mean(indices_phase[0])+2*np.std(indices_phase[0]) and indices_phase[0][2*i+1] > np.mean(indices_phase[0])-2*np.std(indices_phase[0]))]
#        indices_phase[0] = [indices_phase[0][2*i+1] for i in range(0, int(len(indices_phase[0])/2)) if (indices_phase[0][2*i+1] < np.mean(indices_phase[0])+2*np.std(indices_phase[0]) and indices_phase[0][2*i+1] > np.mean(indices_phase[0])-2*np.std(indices_phase[0])) ]




        


        

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