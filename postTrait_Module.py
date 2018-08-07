# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:34:49 2015

@author: roche
"""

import sys
import random
import os

#from params import *
import numpy as np
#from scipy import *
#from pylab import *
from math import *
import matplotlib.pyplot as plt
import scipy.signal as sig
import pandas
from datetime import datetime

class FileData:
    
    def __init__(self, file_name):
        
        self.fileName = file_name
        if (self.fileName.find('_mou') != -1):
            self.fileType = 'HFOP_mou'         
        elif (self.fileName.find('_HFOP_') != -1 or self.fileName.find('_a_') != -1):
            self.fileType = 'HFOP'
        elif (self.fileName.find('_HFO_') != -1 or self.fileName.find('_s_') != -1):
            self.fileType = 'HFO' 
        elif (self.fileName.find('_Alone_') != -1 or self.fileName.find('_w_') != -1):
            self.fileType = 'ALONE'
        elif (self.fileName.find('_HRP_') != -1 or self.fileName.find('_HVP_') != -1 or self.fileName.find('_u_') != -1):
            self.fileType = 'HVP'
        elif (self.fileName.find('_KRP_') != -1 or self.fileName.find('_KVP_') != -1):
            self.fileType = 'KVP'
        elif (self.fileName.find('_r_') != -1 or self.fileName.find('_ROBOT_') != -1):
            self.fileType = 'ROBOT'
        elif (self.fileName.find('_NOISY_') != -1):
            self.fileType = 'NOISY'        
        elif (self.fileName.find('_DELAYED_') != -1):
            self.fileType = 'DELAYED'  
        elif (self.fileName.find('_PPHARD_') != -1):
            self.fileType = 'PPHARD'  
        elif (self.fileName.find('_PPSOFT_') != -1):
            self.fileType = 'PPSOFT'  
        else:
            self.fileType = 'UNKNOWN'
        
        if self.fileName.find('_TRANSPARENCE')!=-1:
            self.experienceType = 'TRAJ'
        elif self.fileName.find('_POINTING_')!=-1:
            self.experienceType = 'POINTING'
            self.fileNameUI = self.fileName[0: self.fileName.find('_ROBOT_')]+ '_UI_' + self.fileName[self.fileName.find('_ROBOT_')+7:]
        elif self.fileName.find('_GABOR_')!=-1:
            self.experienceType = 'GABOR'
            self.fileNameUI = self.fileName
        else:
            self.experienceType = 'INT'            
        self.fileTrialNb = self.fileName[self.fileName.find('_trial_')+7]
        self.fileScenarioNb = self.fileName[self.fileName.find('_scenario_')+10]

        try:        
            n = len(file_name)
            day = int(file_name[n-15:n-13])
            month = int(file_name[n-12:n-10])
            hour = int(file_name[n-9:n-7])
            minute = int(file_name[n-6:n-4])
            self.fileDate = datetime(2018, month, day, hour, minute)
        except:
            self.fileDate = 0
       

#getParamsFromFile()    
        self.finalTime = 0.0
        self.timeOffset = 0.0
        self.facteurDilatation = 0.0
        self.SUBJECT_NAME1 = ''
        self.SUBJECT_NAME2 = ''
        self.PATH_DURATION = 0.0
        self.VITESSE =0.0
        self.Y_POS_CURSOR =0.0
        self.PART_DURATION_BODY =0.0
        self.PART_DURATION_CHOICE =0.0
        self.PART_DURATION_FORK =0.0
        self.PART_DURATION_REGRP =0.0
        self.PART_DURATION_START =0.0
        self.POSITION_OFFSET =0.0
        self.SENSITIVITY =0.0
        self.WINDOW_WIDTH =0.0 
        self.WINDOW_LENGTH =0.0
        self.SCORE1 = 0
        self.SCORE2 = 0
        
#getDataFromFile()     
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Curs_pos  = []
        self.Subj_pos1 = []
        self.Subj_pos2 = []
        self.Subj_for1 = []
        self.Subj_for2 = []
        self.Part_mark1 = []
        self.Part_mark2 = []
        self.Consigne1 = []
        self.Consigne2 = []
        self.Paddle_pos1 = []
        self.Paddle_pos2 = []
        
#calculateRMSandMAP()       
        self.TIME_WINDOW_BEFORE = 1
        self.TIME_WINDOW_AFTER = 1
        self.dataKept = 'INTER'
        self.forceLimit = 1.5
        self.partAnalyzed = 'CHOICES'        
        self.RMS_trial_withpoints = [["."]*100, ["."]*100, ["."]*100] #[SAME, ONE, OPPO]
        self.MAP_trial_withpoints = [["."]*100, ["."]*100, ["."]*100]
        self.FOM_trial_withpoints = [["."]*100, ["."]*100, ["."]*100]
        self.ERR_trial_withpoints = [["."]*100, ["."]*100, ["."]*100]
        self.RMS_trial = [[]]*3
        self.MAP_trial = [[]]*3
        self.FOM_trial = [[]]*3
        self.ERR_trial = [[]]*3
        self.RMS_mean = [0.0]*3
        self.MAP_mean = [0.0]*3
        self.FOM_mean = [0.0]*3
        self.ERR_mean = [0.0]*3
        if self.fileType == 'ALONE' or self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            self.Curs_pos1 = []
            self.Curs_pos2 = []
            self.Robot_pos1 = []
            self.Robot_pos2 = []
            self.RMS_trial_withpoints_1 = [["."]*100, ["."]*100, ["."]*100] 
            self.RMS_trial_withpoints_2 = [["."]*100, ["."]*100, ["."]*100]
            self.RMS_trial_1 = [[]]*3
            self.RMS_trial_2 = [[]]*3
            self.RMS_mean_1 = [0.0]*3
            self.RMS_mean_2 = [0.0]*3
            self.MAP_trial_withpoints_1 = [["."]*100, ["."]*100, ["."]*100] 
            self.MAP_trial_withpoints_2 = [["."]*100, ["."]*100, ["."]*100]
            self.MAP_trial_1 = [[]]*3
            self.MAP_trial_2 = [[]]*3
            self.MAP_mean_1 = [0.0]*3
            self.MAP_mean_2 = [0.0]*3
            self.FOM_trial_withpoints_1 = [["."]*100, ["."]*100, ["."]*100] 
            self.FOM_trial_withpoints_2 = [["."]*100, ["."]*100, ["."]*100]
            self.FOM_trial_1 = [[]]*3
            self.FOM_trial_2 = [[]]*3
            self.FOM_mean_1 = [0.0]*3
            self.FOM_mean_2 = [0.0]*3
            self.ERR_trial_withpoints_1 = [["."]*100, ["."]*100, ["."]*100] 
            self.ERR_trial_withpoints_2 = [["."]*100, ["."]*100, ["."]*100]
            self.ERR_trial_1 = [[]]*3
            self.ERR_trial_2 = [[]]*3
            self.ERR_mean_1 = [0.0]*3
            self.ERR_mean_2 = [0.0]*3            
            
#analyzeDominance()       
        self.nbConflicts = 0
        self.nbChoices1 = 0
        self.nbChoices2 = 0
        self.distParcourue1 = 0
        self.distParcourue2 = 0
        if self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            self.nbConflicts1 = 0
            self.nbConflicts2 = 0
            self.nbChoicesH1 = 0
            self.nbChoicesR1 = 0
            self.nbChoicesH2 = 0
            self.nbChoicesR2 = 0
            
#extractStartingTimes()     
        self.startTimeLeader = []
        self.startTimeFollower = []
        self.analysisStartTime = 0.2
        self.threshold = 15
        if self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            self.startTimeLeader1 = []
            self.startTimeLeader2 = []
            self.startTimeFollower1 = []
            self.startTimeFollower2 = []
            
#extractForces()
        self.forceIntLeader = []
        self.forceIntFollower = []     


#intentionDetection()
        self.analysisStopTime = 0.5
        self.analysisTime = 0
        self.timerMax = 0.1

#analyzeTrajectory()       
        self.threshold_ext = 15
        
#MelendezCalderon()
        self.D_global = []
        self.low_pass = 10
        
        self.RMS_traj = 0
        self.MAP_traj = 0
        self.FOM_traj = 0
        self.RMS_traj1 = 0
        self.RMS_traj2 = 0
        self.MAP_traj1 = 0
        self.MAP_traj2 = 0
        self.FOM_traj1 = 0
        self.FOM_traj2 = 0
        self.ERR_traj = 0
        self.ERR_traj1 = 0
        self.ERR_traj2 = 0
        
#Fichiers POINTING
        self.TimeTrial = []
        self.TimePhase1 = []
        self.TimePhase2 = []
        self.UITrialNumber = []
        self.UIStartPos = []
        self.UITargetPosC = []
        self.UITargetPosF = []
        self.UITargetSubj = [[],[]]
        self.UIFinalChoice = [[],[]]
        self.UITargetWidth = [[],[]]
        self.UIStartWidth = 10
        self.UINbSubjects = 2

#Fichiers POINTING
        self.UIG_TrialNumber = []
        self.UIG_TargetStimulus = []
        self.UIG_ChoiceMade = [[],[], []]
        self.UIG_ChoiceTime = [[],[], []]
        self.UIG_TargetContrast = []
        self.UIG_TargetPos = []
        self.SUBJECT_NAMES = ['','']      
        
#####################################################################################################
    def getParamsFromFile(self):
        f = open(self.fileName,'r')
        self.SUBJECT_NAMES = ['','']
        for line in f:
            if line.find('SUBJECT NAME1')!=-1:
                self.SUBJECT_NAME1 = line[line.find(' : ')+3 : line.find("\n")]
                self.SUBJECT_NAMES[0] = self.SUBJECT_NAME1
            elif line.find('SUBJECT NAME2')!=-1:
                self.SUBJECT_NAME2 = line[line.find(' : ')+3 : line.find("\n")]
                self.SUBJECT_NAMES[1] = self.SUBJECT_NAME2
            elif line.find('PATH_DURATION')!=-1:
                self.PATH_DURATION = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('VITESSE')!=-1:
                self.VITESSE = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('Y_POS_CURSOR')!=-1:
                self.Y_POS_CURSOR = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('PART_DURATION_BODY')!=-1:
                self.PART_DURATION_BODY = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('PART_DURATION_CHOICE')!=-1:
                self.PART_DURATION_CHOICE = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('PART_DURATION_FORK')!=-1:
                self.PART_DURATION_FORK = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('PART_DURATION_REGRP')!=-1:
                self.PART_DURATION_REGRP = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('PART_DURATION_START')!=-1:
                self.PART_DURATION_START = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('POSITION_OFFSET')!=-1:
                self.POSITION_OFFSET = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('SENSITIVITY')!=-1 or line.find('SENSIBILITY')!=-1:
                self.SENSITIVITY = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('WINDOW_WIDTH')!=-1:
                self.WINDOW_WIDTH = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('WINDOW_LENGTH')!=-1:
                self.WINDOW_LENGTH = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('SCORE 1')!=-1:
                self.SCORE1 = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find('SCORE 2')!=-1:
                self.SCORE2 = float(line[line.find(' : ')+3 : line.find("\n")])
            elif line.find("RESULTS") != -1:
                break
        f.close()
        
#####################################################################################################     
    def getDataFromFile(self):
        
        self.getParamsFromFile()
        
        f = open(self.fileName, 'r')
        for line in f:
            lineReadData = line[ 0 : line.find("\n")]
            self.finalTime = lineReadData.split('\t')[0]
        f.close()
    
        if self.experienceType == 'POINTING':
            self.timeOffset = 0
            self.facteurDilatation = 1
        else:                
            self.timeOffset = float(self.Y_POS_CURSOR)/float(self.VITESSE)
            self.facteurDilatation = float(self.finalTime)/(self.PATH_DURATION + float(self.WINDOW_LENGTH)/self.VITESSE)
            
        f = open(self.fileName, 'r')
        i=0
        k = 0
        fl = 0
        for line in f:
            lineRead= line[0:line.find("\n")]
            if lineRead.find("ROBOT TIME") != -1:
                k =1
                continue
            if k==1 and line == "\n":
                k=2
                continue
            if k ==2:
                dataList = lineRead.split("\t")
                if fl == 0:
                    fl = len(dataList)
                else:
                    if len(dataList) < fl:
                        continue
                if self.experienceType == 'POINTING':
                    self.Time.append(float(dataList[0]))
                    self.TimeTrial.append(float(dataList[1]))
                    self.TimePhase1.append(float(dataList[2]))
                    self.TimePhase2.append(float(dataList[3]))
                    self.Subj_pos1.append(-(float(dataList[4]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                    self.Subj_pos2.append(-(float(dataList[5]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                    self.Paddle_pos1.append(float(dataList[4]))
                    self.Paddle_pos2.append(float(dataList[5]))
                    self.Subj_for1.append(float(dataList[6]))
                    self.Subj_for2.append(float(dataList[7]))
                    self.Consigne1.append(float(dataList[8]))
                    self.Consigne2.append(float(dataList[9]))
                    if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
                        self.Curs_pos.append(-((float(dataList[4]) + float(dataList[5]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                    elif self.fileType == 'ALONE':
                        self.Curs_pos1.append(-(float(dataList[4]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                        self.Curs_pos2.append(-(float(dataList[5]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                    elif self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
                        self.Curs_pos1.append(-((float(dataList[4]) + float(dataList[10]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                        self.Curs_pos2.append(-((float(dataList[5]) + float(dataList[11]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH / self.SENSITIVITY +self.WINDOW_WIDTH/2)
                        self.Robot_pos1.append(-(float(dataList[10]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                        self.Robot_pos2.append(-(float(dataList[11]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/ self.SENSITIVITY +self.WINDOW_WIDTH/2)
                 
                else:
                    if len(dataList) <= 9: #anciens fichiers
                        self.Time.append(float(dataList[0]))
                        self.Path_pos1.append(float(dataList[1]) - self.WINDOW_WIDTH/2)
                        self.Path_pos2.append(float(dataList[2]) - self.WINDOW_WIDTH/2)
                        self.Subj_pos1.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[3]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                        self.Subj_pos2.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[4]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                        self.Subj_for1.append(float(dataList[5]))
                        self.Subj_for2.append(float(dataList[6]))
                        if self.fileType == 'HFOP' or self.fileType == 'HFO' or self.fileType == 'HFOP_mou':
                            self.Curs_pos.append(self.WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                        elif self.fileType == 'ALONE':
                            self.Curs_pos1.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[3]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                            self.Curs_pos2.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[4]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                        elif self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
                            self.Curs_pos1.append(self.WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[7]))/2 - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                            self.Curs_pos2.append(self.WINDOW_WIDTH/2*(1 - ((float(dataList[4])+float(dataList[8]))/2 - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                            self.Robot_pos1.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[7]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
                            self.Robot_pos2.append(self.WINDOW_WIDTH/2*(1 - (float(dataList[8]) - self.POSITION_OFFSET) / self.POSITION_OFFSET * self.SENSITIVITY) - self.WINDOW_WIDTH/2)
    
                    else: #nouveaux fichiers
                        self.Time.append(float(dataList[0]))
                        self.Path_pos1.append(float(dataList[1]) - self.WINDOW_WIDTH/2)
                        self.Path_pos2.append(float(dataList[2]) - self.WINDOW_WIDTH/2)
                        self.Subj_pos1.append(-(float(dataList[3]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                        self.Subj_pos2.append(-(float(dataList[4]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                        self.Paddle_pos1.append(float(dataList[3]))
                        self.Paddle_pos2.append(float(dataList[4]))
                        self.Subj_for1.append(float(dataList[5]))
                        self.Subj_for2.append(float(dataList[6]))
                        self.Consigne1.append(float(dataList[7]))
                        self.Consigne2.append(float(dataList[8]))
                        if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
                            self.Curs_pos.append(-((float(dataList[3]) + float(dataList[4]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                        elif self.fileType == 'ALONE':
                            self.Curs_pos1.append(-(float(dataList[3]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                            self.Curs_pos2.append(-(float(dataList[4]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                        elif self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
                            self.Curs_pos1.append(-((float(dataList[3]) + float(dataList[9]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                            self.Curs_pos2.append(-((float(dataList[4]) + float(dataList[10]))/2 - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                            self.Robot_pos1.append(-(float(dataList[9]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                            self.Robot_pos2.append(-(float(dataList[10]) - self.POSITION_OFFSET) * self.WINDOW_WIDTH/10 / self.SENSITIVITY)
                            
                    if len(dataList) > 11:
                        self.Part_mark1.append(dataList[11])
                        self.Part_mark2.append(dataList[12])
                    else:
                        self.Part_mark1.append("0")
                        self.Part_mark2.append("0")
            i+=1
        
        f.close()
   
     
#####################################################################################################     
    def getDataFromUIFile(self):
        
        f = open(self.fileNameUI, 'r')           
        i=0
        k = 0
        if(self.experienceType == 'POINTING'):
            for line in f:
                lineRead= line[0:line.find("\n")]
                if line.find('TARGET WIDTH 1')!=-1:
                    UITargetWidthC = float(line[line.find(' :')+2 : line.find("\n")])
                elif line.find('TARGET WIDTH 2')!=-1:
                    UITargetWidthF = float(line[line.find(' :')+2 : line.find("\n")] )                
                elif line.find('NB_SUBJECTS')!=-1:
                    self.UINbSubjects = int(line[line.find(' :')+2 : line.find("\n")] )                
                if lineRead.find("TRIAL NUMBER") != -1:
                    k =1
                    continue
                if k==1 and line == "\n":
                    k=2
                    continue
                if k ==2:
                    dataList = lineRead.split("\t")
                    self.UITrialNumber.append(float(dataList[0]))
                    self.UIStartPos.append(float(dataList[1]))
                    self.UITargetPosC.append(float(dataList[2]))
                    self.UITargetPosF.append(float(dataList[3]))
                    self.UITargetSubj[0].append(float(dataList[4]))
                    self.UITargetSubj[1].append(float(dataList[5]))
                    self.UIFinalChoice[0].append(float(dataList[6]))
                    self.UIFinalChoice[1].append(float(dataList[7]))
                    if len(dataList)>9:
                        self.UITargetWidth[0].append(float(dataList[8]))
                        self.UITargetWidth[1].append(float(dataList[9]))
                    else:
                        self.UITargetWidth[0].append(UITargetWidthC)
                        self.UITargetWidth[1].append(UITargetWidthF)                    

        elif(self.experienceType == 'GABOR'):
                    
            for line in f:
                lineRead= line[0:line.find("\n")]   
                if line.find('SUBJECT NAME1')!=-1:
                    self.SUBJECT_NAME1 = line[line.find(' : ')+3 : line.find("\n")]
                    self.SUBJECT_NAMES[0] = self.SUBJECT_NAME1
                elif line.find('SUBJECT NAME2')!=-1:
                    self.SUBJECT_NAME2 = line[line.find(' : ')+3 : line.find("\n")]
                    self.SUBJECT_NAMES[1] = self.SUBJECT_NAME2
                          
                if lineRead.find("TRIAL NUMBER") != -1:
                    k =1
                    continue
                if k==1 and (line == "\n" or line == "\t\n"):
                    k=2
                    continue
                if k ==2:
                    dataList = lineRead.split("\t")
                    self.UIG_TrialNumber.append(int(dataList[0]))
                    self.UIG_TargetStimulus.append(int(dataList[1]))
                    self.UIG_ChoiceMade[0].append(int(dataList[2])-1)
                    self.UIG_ChoiceMade[1].append(int(dataList[3])-1)
                    self.UIG_ChoiceMade[2].append(int(dataList[4])-1)
                    self.UIG_ChoiceTime[0].append(float(dataList[5]))
                    self.UIG_ChoiceTime[1].append(float(dataList[6]))
                    self.UIG_ChoiceTime[2].append(float(dataList[7]))
                    self.UIG_TargetContrast.append(float(dataList[8]))
                    self.UIG_TargetPos.append(float(dataList[9]))
                
        f.close()
        
##################################################################################################### 
    def toCSV(self):   
        data = pandas.DataFrame({'Time' : self.Time, 'Path_pos1' : self.Path_pos1, 'Path_pos2' : self.Path_pos2, 'Subj_pos1' : self.Subj_pos1, 'Subj_pos2' : self.Subj_pos2, 'Subj_for1' : self.Subj_for1, 'Subj_for2' : self.Subj_for2, 'Consigne1' : self.Consigne1, 'Consigne2' : self.Consigne2})            
        data.to_csv(self.fileName[0:len(self.fileName)-3]+'csv')
        
##################################################################################################### 
    def calculateRMSandMAP(self):
        #Les matrices sont dans un premier temps remplies de points, on vient ensuite remplacer dans chaque ligne la valeur pour le trial etudie (SAME, ONE, OPPO)
        #Cette fonctionnalite permet d'acceder a l'ordre des trials (n'est plus utilise dans cette version)
        self.RMS_trial_withpoints = [['.']*30, ['.']*30, ['.']*30]
        self.MAP_trial_withpoints = [['.']*30, ['.']*30, ['.']*30]
    
        l=0
    
        start_time = self.Y_POS_CURSOR/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation
        
                #Check for damaged file
        for i in range(0, len(self.Time)-1):
            if self.Time[i+1] - self.Time[i] > 0.5:
                end_time = self.Time[i]
                print "broken" 
                break

        if self.partAnalyzed == 'CHOICES':
            loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY + self.PART_DURATION_CHOICE  - int(self.TIME_WINDOW_BEFORE)
            loop_stop_time  = loop_start_time  + int(self.TIME_WINDOW_BEFORE + self.TIME_WINDOW_AFTER) #PART_DURATION_CHOICE + PART_DURATION_FORK
        elif self.partAnalyzed == 'BODY' :
            loop_start_time = start_time + self.PART_DURATION_START
            loop_stop_time  = loop_start_time  + 2*self.PART_DURATION_BODY
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
            
        while (loop_start_time <= end_time and loop_stop_time<= end_time):
            if self.dataKept == 'INTER':
                if abs(np.mean(self.Subj_for1[loop_start_line:loop_stop_line])) >= self.forceLimit or abs(np.mean(self.Subj_for2[loop_start_line:loop_stop_line])) >= self.forceLimit:
                    l+=1
                    loop_start_time += cycle_time
                    loop_start_line = self.time2line(loop_start_time)
                    loop_stop_time  += cycle_time
                    loop_stop_line  = self.time2line(loop_stop_time)
                    continue
            elif self.dataKept == 'EXTER' and self.fileType == 'HFOP':
                if abs(np.mean(self.Subj_for1[loop_start_line:loop_stop_line])) <= self.forceLimit or abs(np.mean(self.Subj_for2[loop_start_line:loop_stop_line])) <= self.forceLimit:
                    l+=1
                    loop_start_time += cycle_time
                    loop_start_line = self.time2line(loop_start_time)
                    loop_stop_time  += cycle_time
                    loop_stop_line  = self.time2line(loop_stop_time)
                    continue            
            
            if self.Path_pos1[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] == self.Path_pos2[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] : #SAME case
                for j in range (loop_start_line, loop_stop_line):
                    if self.RMS_trial_withpoints[0][l] == ".":
                        self.RMS_trial_withpoints[0][l] = 0
                    if self.MAP_trial_withpoints[0][l] == ".":
                        self.MAP_trial_withpoints[0][l] = 0
                        
                    if self.fileType == 'HFO' or self.fileType == 'HFOP':
                        self.RMS_trial_withpoints[0][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j])))**2
                        self.MAP_trial_withpoints[0][l] += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j]))

                    elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                        if self.RMS_trial_withpoints_1[0][l] == '.':
                            self.RMS_trial_withpoints_1[0][l] = 0
                        if self.RMS_trial_withpoints_2[0][l] == '.':
                            self.RMS_trial_withpoints_2[0][l] = 0
                        if self.MAP_trial_withpoints_1[0][l] == '.':
                            self.MAP_trial_withpoints_1[0][l] = 0
                        if self.MAP_trial_withpoints_2[0][l] == '.':
                            self.MAP_trial_withpoints_2[0][l] = 0   
                        self.RMS_trial_withpoints_1[0][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j])))**2                                               
                        self.RMS_trial_withpoints_2[0][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j])))**2
                        self.MAP_trial_withpoints_1[0][l] += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j])
                        self.MAP_trial_withpoints_2[0][l] += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j])

                              
                if self.fileType == 'HFO' or self.fileType == 'HFOP':
                    self.MAP_trial_withpoints[0][l] /= (loop_stop_line - loop_start_line)
                    self.RMS_trial_withpoints[0][l] = sqrt(self.RMS_trial_withpoints[0][l]/(loop_stop_line - loop_start_line))
                elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                    self.RMS_trial_withpoints_1[0][l] = sqrt(self.RMS_trial_withpoints_1[0][l]/(loop_stop_line - loop_start_line))
                    self.RMS_trial_withpoints_2[0][l] = sqrt(self.RMS_trial_withpoints_2[0][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_1[0][l] = sqrt(self.MAP_trial_withpoints_1[0][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_2[0][l] = sqrt(self.MAP_trial_withpoints_2[0][l]/(loop_stop_line - loop_start_line))
                    
                    
            elif(self.Path_pos1[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] >= 5000 or self.Path_pos2[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] >= 5000): #ONE case      
                for j in range (loop_start_line, loop_stop_line):
                    if self.RMS_trial_withpoints[1][l] == ".":
                        self.RMS_trial_withpoints[1][l] = 0
                    if self.MAP_trial_withpoints[1][l] == ".":
                        self.MAP_trial_withpoints[1][l] = 0
                        
                    if self.fileType == 'HFO' or self.fileType == 'HFOP':
                        self.RMS_trial_withpoints[1][l] += ( min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j]), abs(-self.Path_pos1[j] - self.Curs_pos[j]), abs(-self.Path_pos2[j] - self.Curs_pos[j])) )**2
                        self.MAP_trial_withpoints[1][l] += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j]))

                    elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                        if self.RMS_trial_withpoints_1[1][l] == '.':
                            self.RMS_trial_withpoints_1[1][l] = 0
                        if self.RMS_trial_withpoints_2[1][l] == '.':
                            self.RMS_trial_withpoints_2[1][l] = 0
                        if self.MAP_trial_withpoints_1[1][l] == '.':
                            self.MAP_trial_withpoints_1[1][l] = 0
                        if self.MAP_trial_withpoints_2[1][l] == '.':
                            self.MAP_trial_withpoints_2[1][l] = 0 
                        self.RMS_trial_withpoints_1[1][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j]), abs(-self.Path_pos1[j] - self.Curs_pos1[j]), abs(-self.Path_pos2[j] - self.Curs_pos1[j])))**2                                               
                        self.RMS_trial_withpoints_2[1][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j]), abs(-self.Path_pos1[j] - self.Curs_pos1[j]), abs(-self.Path_pos2[j] - self.Curs_pos1[j])))**2 
                        self.MAP_trial_withpoints_1[1][l] += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j])
                        self.MAP_trial_withpoints_2[1][l] += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j])
                                               
                if self.fileType == 'HFO' or self.fileType == 'HFOP':
                    self.RMS_trial_withpoints[1][l] = sqrt(self.RMS_trial_withpoints[1][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints[1][l] /= (loop_stop_line - loop_start_line)
                elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                    self.RMS_trial_withpoints_1[1][l] = sqrt(self.RMS_trial_withpoints_1[1][l]/(loop_stop_line - loop_start_line))
                    self.RMS_trial_withpoints_2[1][l] = sqrt(self.RMS_trial_withpoints_2[1][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_1[1][l] = sqrt(self.MAP_trial_withpoints_1[1][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_2[1][l] = sqrt(self.MAP_trial_withpoints_2[1][l]/(loop_stop_line - loop_start_line))

                
            else: # OPPO case
                for j in range (loop_start_line, loop_stop_line):
                    if self.RMS_trial_withpoints[2][l] == ".":
                        self.RMS_trial_withpoints[2][l] = 0
                    if self.MAP_trial_withpoints[2][l] == ".":
                        self.MAP_trial_withpoints[2][l] = 0
                        
                    if self.fileType == 'HFO' or self.fileType == 'HFOP':
                        self.RMS_trial_withpoints[2][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j])))**2
                        self.MAP_trial_withpoints[2][l] += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j]))

                    elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                        if self.RMS_trial_withpoints_1[2][l] == '.':
                            self.RMS_trial_withpoints_1[2][l] = 0
                        if self.RMS_trial_withpoints_2[2][l] == '.':
                            self.RMS_trial_withpoints_2[2][l] = 0
                        if self.MAP_trial_withpoints_1[2][l] == '.':
                            self.MAP_trial_withpoints_1[2][l] = 0
                        if self.MAP_trial_withpoints_2[2][l] == '.':
                            self.MAP_trial_withpoints_2[2][l] = 0 
                        self.RMS_trial_withpoints_1[2][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j])))**2                                               
                        self.RMS_trial_withpoints_2[2][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j])))**2                                      
                        self.MAP_trial_withpoints_1[2][l] += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for1[j])
                        self.MAP_trial_withpoints_2[2][l] += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(self.Time[j+1]-self.Time[j-1])*self.Subj_for2[j])
                        
                if self.fileType == 'HFO' or self.fileType == 'HFOP':
                    self.MAP_trial_withpoints[2][l] /= (loop_stop_line - loop_start_line)
                    self.RMS_trial_withpoints[2][l] = sqrt(self.RMS_trial_withpoints[2][l]/(loop_stop_line - loop_start_line))
                elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                    self.RMS_trial_withpoints_1[2][l] = sqrt(self.RMS_trial_withpoints_1[2][l]/(loop_stop_line - loop_start_line))
                    self.RMS_trial_withpoints_2[2][l] = sqrt(self.RMS_trial_withpoints_2[2][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_1[2][l] = sqrt(self.MAP_trial_withpoints_1[2][l]/(loop_stop_line - loop_start_line))
                    self.MAP_trial_withpoints_2[2][l] = sqrt(self.MAP_trial_withpoints_2[2][l]/(loop_stop_line - loop_start_line))
                    
            l+=1
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
            
        self.RMS_trial = removePoints(self.RMS_trial_withpoints)
        self.MAP_trial = removePoints(self.MAP_trial_withpoints)
            
        for i in range(0, len(self.RMS_mean)):
            nbSamples = len(self.RMS_trial[i])
            if nbSamples == 0:
                nbSamples =1
            self.RMS_mean[i] = sum(self.RMS_trial[i])/nbSamples
            self.MAP_mean[i] = sum(self.MAP_trial[i])/nbSamples
            
        if self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
            self.RMS_trial_1 = removePoints(self.RMS_trial_withpoints_1)
            self.RMS_trial_2 = removePoints(self.RMS_trial_withpoints_2)
            self.MAP_trial_1 = removePoints(self.MAP_trial_withpoints_1)
            self.MAP_trial_2 = removePoints(self.MAP_trial_withpoints_2)
            for i in range(0, len(self.RMS_mean)):
                nbSamples = len(self.RMS_trial_1[i])
                if nbSamples == 0:
                    nbSamples =1
                self.RMS_mean_1[i] = sum(self.RMS_trial_1[i])/nbSamples
                self.RMS_mean_2[i] = sum(self.RMS_trial_2[i])/nbSamples
            M=0         
            for i in range(0, len(self.RMS_trial_1)):
                M = customMax(self.RMS_trial_1[i])
                while  M > self.RMS_mean_1[i] + 3*np.std(self.RMS_mean_1[i]):
                    self.RMS_trial_1[i].remove(M)
                    M = customMax(self.RMS_trial_1[i])
            for i in range(0, len(self.RMS_trial_2)):
                M = customMax(self.RMS_trial_2[i])
                while  M > self.RMS_mean_2[i] + 3*np.std(self.RMS_mean_2[i]):
                    self.RMS_trial_2[i].remove(M)
                    M = customMax(self.RMS_trial_2[i])                    


##################################################################################################### 
    def calculateRMSandMAP_markers(self):
        #Les matrices sont dans un premier temps remplies de points, on vient ensuite remplacer dans chaque ligne la valeur pour le trial etudie (SAME, ONE, OPPO)
        #Cette fonctionnalite permet d'acceder a l'ordre des trials (n'est plus utilise dans cette version)
#        self.RMS_trial_withpoints = [[], [], []]
#        self.MAP_trial_withpoints = [[], [], []]

    
        l=0
        deltaT = 0
    
        start_time = self.Time[self.Part_mark1.index('START')]
        start_line = self.Part_mark1.index('START')
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation
        
                #Check for damaged file
        for i in range(0, len(self.Time)-1):
            if self.Time[i+1] - self.Time[i] > 0.5:
                #end_time = self.Time[i]
                print "broken" 
                break
            
        loop_start_line = start_line
        loop_stop_line = start_line
        
        fork_time = (self.PART_DURATION_REGRP + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK)*self.facteurDilatation
        fork_lines = self.time2line(fork_time)
        
        body_lines = self.time2line((self.PART_DURATION_BODY)*self.facteurDilatation)
           
        while (loop_start_line <= len(self.Time) and loop_stop_line<= len(self.Time)):
            if self.partAnalyzed == 'CHOICES':
                n = loop_stop_line + 200
                temp = [i + n for i, s in enumerate(self.Part_mark1[n:]) if 'FORK' in s]
                if len(temp)>=1:
                    loop_start_line = min(temp) + self.time2line((self.PART_DURATION_CHOICE - self.TIME_WINDOW_BEFORE)*self.facteurDilatation)
                    loop_stop_line = loop_start_line + self.time2line((self.TIME_WINDOW_BEFORE+self.TIME_WINDOW_AFTER)*self.facteurDilatation)
                else:
                    break
                        
            elif self.partAnalyzed == 'BODY' :
                n = loop_stop_line + 200
                temp = [i + n for i, s in enumerate(self.Part_mark1[n:]) if 'BODY' in s]
                if len(temp)>=1:
                    loop_start_line = min(temp) 
                    loop_stop_line = loop_start_line + self.time2line((2*self.PART_DURATION_BODY)*self.facteurDilatation)
                else:
                    break
         
            if self.dataKept == 'INTER':
                if abs(np.mean(self.Subj_for1[loop_start_line:loop_stop_line])) >= self.forceLimit or abs(np.mean(self.Subj_for2[loop_start_line:loop_stop_line])) >= self.forceLimit:
                    continue
            elif self.dataKept == 'EXTER' and self.fileType == 'HFOP':
                if abs(np.mean(self.Subj_for1[loop_start_line:loop_stop_line])) <= self.forceLimit or abs(np.mean(self.Subj_for2[loop_start_line:loop_stop_line])) <= self.forceLimit:
                    continue            

#################################"SAME           
            if self.Path_pos1[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] == self.Path_pos2[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] : #SAME case
                trial_case = 0
#################################"ONE                   
            elif(self.Path_pos1[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] >= 5000 or self.Path_pos2[loop_start_line + self.time2line(self.TIME_WINDOW_BEFORE * self.facteurDilatation) + 5000] >= 5000): #ONE case      
                trial_case = 1
#################################"OPPO   
            else:
                trial_case = 2

            for j in range (loop_start_line, loop_stop_line):
                if(self.Time[j+1]-self.Time[j-1] != 0):
                    deltaT = self.Time[j+1]-self.Time[j-1]                       
                    
                if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
                    if self.RMS_trial_withpoints[trial_case][l] == ".":
                        self.RMS_trial_withpoints[trial_case][l] = 0
                    if self.MAP_trial_withpoints[trial_case][l] == ".":
                        self.MAP_trial_withpoints[trial_case][l] = 0
                    if self.FOM_trial_withpoints[trial_case][l] == ".":
                        self.FOM_trial_withpoints[trial_case][l] = 0  
                    if self.ERR_trial_withpoints[trial_case][l] == ".":
                        self.ERR_trial_withpoints[trial_case][l] = 0   
                    self.RMS_trial_withpoints[trial_case][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j]), abs(-self.Path_pos1[j] - self.Curs_pos[j]), abs(-self.Path_pos2[j] - self.Curs_pos[j])) )**2
                    self.MAP_trial_withpoints[trial_case][l] += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for2[j]))
                    self.FOM_trial_withpoints[trial_case][l] += abs(self.Subj_for1[j]) + abs( self.Subj_for2[j])
                    self.ERR_trial_withpoints[trial_case][l] += min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j]), abs(-self.Path_pos1[j] - self.Curs_pos[j]), abs(-self.Path_pos2[j] - self.Curs_pos[j])) 
                            
                elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                    if self.RMS_trial_withpoints_1[trial_case][l] == '.':
                        self.RMS_trial_withpoints_1[trial_case][l] = 0
                    if self.RMS_trial_withpoints_2[trial_case][l] == '.':
                        self.RMS_trial_withpoints_2[trial_case][l] = 0
                    if self.MAP_trial_withpoints_1[trial_case][l] == '.':
                        self.MAP_trial_withpoints_1[trial_case][l] = 0
                    if self.MAP_trial_withpoints_2[trial_case][l] == '.':
                        self.MAP_trial_withpoints_2[trial_case][l] = 0
                    if self.FOM_trial_withpoints_1[trial_case][l] == '.':
                        self.FOM_trial_withpoints_1[trial_case][l] = 0
                    if self.FOM_trial_withpoints_2[trial_case][l] == '.':
                        self.FOM_trial_withpoints_2[trial_case][l] = 0  
                    if self.ERR_trial_withpoints_1[trial_case][l] == '.':
                        self.ERR_trial_withpoints_1[trial_case][l] = 0
                    if self.ERR_trial_withpoints_2[trial_case][l] == '.':
                        self.ERR_trial_withpoints_2[trial_case][l] = 0
                    self.RMS_trial_withpoints_1[trial_case][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j]), abs(-self.Path_pos1[j] - self.Curs_pos1[j]), abs(-self.Path_pos2[j] - self.Curs_pos1[j])) )**2
                    self.RMS_trial_withpoints_2[trial_case][l] += (min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j]), abs(-self.Path_pos1[j] - self.Curs_pos2[j]), abs(-self.Path_pos2[j] - self.Curs_pos2[j])) )**2
                    self.MAP_trial_withpoints_1[trial_case][l] += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(deltaT)*self.Subj_for1[j])
                    self.MAP_trial_withpoints_2[trial_case][l] += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(deltaT)*self.Subj_for2[j])
                    self.FOM_trial_withpoints_1[trial_case][l] += abs(self.Subj_for1[j])
                    self.FOM_trial_withpoints_2[trial_case][l] += abs(self.Subj_for2[j])
                    self.ERR_trial_withpoints_1[trial_case][l] += min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j]), abs(-self.Path_pos1[j] - self.Curs_pos1[j]), abs(-self.Path_pos2[j] - self.Curs_pos1[j]))                                             
                    self.ERR_trial_withpoints_2[trial_case][l] += min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j]), abs(-self.Path_pos1[j] - self.Curs_pos2[j]), abs(-self.Path_pos2[j] - self.Curs_pos2[j]))
                    
            if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
                self.RMS_trial_withpoints[trial_case][l] = sqrt(self.RMS_trial_withpoints[trial_case][l]/(loop_stop_line - loop_start_line))
                self.MAP_trial_withpoints[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.FOM_trial_withpoints[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.ERR_trial_withpoints[trial_case][l] /= (loop_stop_line - loop_start_line)
            elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                self.RMS_trial_withpoints_1[trial_case][l] = sqrt(self.RMS_trial_withpoints_1[trial_case][l]/(loop_stop_line - loop_start_line))
                self.RMS_trial_withpoints_2[trial_case][l] = sqrt(self.RMS_trial_withpoints_2[trial_case][l]/(loop_stop_line - loop_start_line))
                self.MAP_trial_withpoints_1[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.MAP_trial_withpoints_2[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.FOM_trial_withpoints_1[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.FOM_trial_withpoints_2[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.ERR_trial_withpoints_1[trial_case][l] /= (loop_stop_line - loop_start_line)
                self.ERR_trial_withpoints_2[trial_case][l] /= (loop_stop_line - loop_start_line)

            l+=1       
#        print self.RMS_trial_withpoints_1    
        self.RMS_trial = removePoints(self.RMS_trial_withpoints)
        self.MAP_trial = removePoints(self.MAP_trial_withpoints)
        self.FOM_trial = removePoints(self.FOM_trial_withpoints)  
        self.ERR_trial = removePoints(self.ERR_trial_withpoints)  
        for i in range(0, len(self.RMS_mean)):
            nbSamples = len(self.RMS_trial[i])
            if nbSamples == 0:
                nbSamples =1
            self.RMS_mean[i] = sum(self.RMS_trial[i])/nbSamples
            self.MAP_mean[i] = sum(self.MAP_trial[i])/nbSamples
            self.FOM_mean[i] = sum(self.FOM_trial[i])/nbSamples
            self.ERR_mean[i] = sum(self.ERR_trial[i])/nbSamples
            
        if self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
            self.RMS_trial_1 = removePoints(self.RMS_trial_withpoints_1)
            self.RMS_trial_2 = removePoints(self.RMS_trial_withpoints_2)
            self.MAP_trial_1 = removePoints(self.MAP_trial_withpoints_1)
            self.MAP_trial_2 = removePoints(self.MAP_trial_withpoints_2)            
            self.FOM_trial_1 = removePoints(self.FOM_trial_withpoints_1)
            self.FOM_trial_2 = removePoints(self.FOM_trial_withpoints_2)
            self.ERR_trial_1 = removePoints(self.ERR_trial_withpoints_1)
            self.ERR_trial_2 = removePoints(self.ERR_trial_withpoints_2)            
            for i in range(0, len(self.RMS_mean)):
                nbSamples = len(self.RMS_trial_1[i])
                if nbSamples == 0:
                    nbSamples =1
                self.RMS_mean_1[i] = sum(self.RMS_trial_1[i])/nbSamples
                self.RMS_mean_2[i] = sum(self.RMS_trial_2[i])/nbSamples
                self.MAP_mean_1[i] = sum(self.MAP_trial_1[i])/nbSamples
                self.MAP_mean_2[i] = sum(self.MAP_trial_2[i])/nbSamples
                self.FOM_mean_1[i] = sum(self.FOM_trial_1[i])/nbSamples
                self.FOM_mean_2[i] = sum(self.FOM_trial_2[i])/nbSamples
                self.ERR_mean_1[i] = sum(self.ERR_trial_1[i])/nbSamples
                self.ERR_mean_2[i] = sum(self.ERR_trial_2[i])/nbSamples                
            M=0  
#            print self.RMS_trial_1
#            for i in range(0, len(self.RMS_trial_1)):
#                M = customMax(self.RMS_trial_1[i])
##                print self.RMS_trial_1[i]
##                print M, self.RMS_mean_1[i], np.std(self.RMS_trial_1[i])
#                while  M > self.RMS_mean_1[i] + 6*np.std(self.RMS_trial_1[i]):
#                    self.RMS_trial_1[i].remove(M)
#                    M = customMax(self.RMS_trial_1[i])
#            for i in range(0, len(self.RMS_trial_2)):
#                M = customMax(self.RMS_trial_2[i])
#                while  M > self.RMS_mean_2[i] + 3*np.std(self.RMS_mean_2[i]):
#                    self.RMS_trial_2[i].remove(M)
#                    M = customMax(self.RMS_trial_2[i])                    
##            print self.RMS_trial_1 
#
####################################################################################################
    def calculateRMSandMAP_traj(self):
                #Check for damaged file
        for i in range(0, len(self.Time)-1):
            if self.Time[i+1] - self.Time[i] > 0.5:
                #end_time = self.Time[i]
                print "broken" 
                break

        part_posStart = []
        part_posStop = []
        part_start = []
        part_stop = []
        part_type = []
        scenario_file = open('../../lucas/scenarios/obstacle/SCENARIO_OBST_' + str(self.fileScenarioNb))
        for line in scenario_file:
            line[ 0 : line.find("\n")]
            line = line.split('\t')
            part_posStart.append(float(line[0]))
            part_posStop.append(float(line[1]))
            part_start.append(float(line[2]))
            part_stop.append(float(line[3]))
            part_type.append(int(line[4]))

        while(max(part_stop)> self.PATH_DURATION):
            if (part_stop[len(part_stop)-1] > self.PATH_DURATION):
                part_posStart.pop(len(part_stop)-1)
                part_posStop.pop(len(part_stop)-1)
                part_start.pop(len(part_stop)-1)
                part_stop.pop(len(part_stop)-1)
                part_type.pop(len(part_stop)-1)                
        
        if max(part_stop)<60:
            part_start.append(part_stop[len(part_stop)-1])
            part_stop.append(60.0)
            part_type.append(3)
#        for i in range(0, len(part_stop)):
#            if (part_stop[i] > self.PATH_DURATION):
#                part_start.pop(i)
#                part_stop.pop(i)
#                part_type.pop(i)
        for i in range(0, len(part_posStart )):
            if part_posStart[i] == part_posStop[i]:
                part_type[i] = 3
#        print part_start
#        print part_stop
#        print part_type
#        print self.facteurDilatation


        deltaT = 0
        self.RMS_traj = [[], [], [], []]
        self.MAP_traj = [[], [], [], []]
        self.FOM_traj = [[], [], [], []]
        self.ERR_traj = [[], [], [], []]
        self.RMS_traj1 = [[], [], [], []]
        self.RMS_traj2 = [[], [], [], []]
        self.MAP_traj1 = [[], [], [], []]
        self.MAP_traj2 = [[], [], [], []]
        self.FOM_traj1 = [[], [], [], []]
        self.FOM_traj2 = [[], [], [], []]
        self.ERR_traj1 = [[], [], [], []]
        self.ERR_traj2 = [[], [], [], []]
                
        for k in range(0, len(part_stop)):
            start_time = part_start[k] + self.Y_POS_CURSOR/self.VITESSE
            start_time = start_time * self.facteurDilatation
            start_line = self.time2line(start_time) + 10
            
            end_time = part_stop[k] + self.Y_POS_CURSOR/self.VITESSE
            end_time = end_time * self.facteurDilatation
            end_line = self.time2line(end_time)
            
            tempRMS = 0.
            tempMAP = 0.
            tempFOM = 0.
            tempERR = 0.
            tempRMS1 = 0.
            tempRMS2 = 0.
            tempMAP1 = 0.
            tempMAP2 = 0.
            tempFOM1 = 0.
            tempFOM2 = 0.
            tempERR1 = 0.
            tempERR2 = 0. 
            
            for j in range (start_line, end_line):
                if(self.Time[j+1]-self.Time[j-1] != 0):
                    deltaT = self.Time[j+1]-self.Time[j-1]                                  
                if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
#                    if j%5000==0:
#                        print self.Time[j]-4, self.Path_pos1[j], self.Curs_pos[j], (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j])))**2                  
                    tempRMS += (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j])))**2
                    tempMAP += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for2[j]))
                    tempFOM += abs(self.Subj_for1[j]) + abs( self.Subj_for2[j])
#                    if np.sign(self.Subj_for1[j]) != np.sign(self.Subj_for2[j]):
#                        if abs(self.Subj_for1[j]) > abs(self.Subj_for2[j]):
#                            tempFOM += abs(abs(self.Subj_for1[j]) - (self.Subj_for1[j] + self.Subj_for2[j]))
#                        else:
#                            tempFOM += abs(abs(self.Subj_for2[j]) - (self.Subj_for1[j] + self.Subj_for2[j]))
#                    else:
#                        if abs(self.Subj_for1[j]) > abs(self.Subj_for2[j]):
#                            tempFOM += self.Subj_for1[j] -  self.Subj_for2[j]
#                        else:
#                            tempFOM += self.Subj_for2[j] -  self.Subj_for1[j]                       
                    tempERR += min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j]))
    
                elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                    tempRMS1 += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j])))**2                                               
                    tempRMS2 += (min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j])))**2
                    tempMAP1 += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(deltaT)*self.Subj_for1[j])
                    tempMAP2 += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(deltaT)*self.Subj_for2[j])
                    tempFOM1 += abs(self.Subj_for1[j])
                    tempFOM2 += abs(self.Subj_for2[j])
                    tempERR1 += min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j]))
                    tempERR2 += min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j]))
    
                          
            if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
                self.RMS_traj[part_type[k]].append(sqrt(tempRMS)/(end_line - start_line))
                self.MAP_traj[part_type[k]].append(tempMAP/(end_line - start_line))
                self.FOM_traj[part_type[k]].append(tempFOM/(end_line - start_line))
                self.ERR_traj[part_type[k]].append(tempERR/(end_line - start_line))
            elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
                self.RMS_traj1[part_type[k]].append(sqrt(tempRMS1)/(end_line - start_line))
                self.RMS_traj2[part_type[k]].append(sqrt(tempRMS2)/(end_line - start_line))
                self.MAP_traj1[part_type[k]].append(tempMAP1/(end_line - start_line))
                self.MAP_traj2[part_type[k]].append(tempMAP2/(end_line - start_line))
                self.FOM_traj1[part_type[k]].append(tempFOM1/(end_line - start_line))
                self.FOM_traj2[part_type[k]].append(tempFOM2/(end_line - start_line))
                self.ERR_traj1[part_type[k]].append(tempERR1/(end_line - start_line))
                self.ERR_traj2[part_type[k]].append(tempERR2/(end_line - start_line))
                
#            print self.Time[start_line], self.Time[end_line], sqrt(tempRMS)/(end_line - start_line)
    
#        print self.RMS_traj
#        print self.MAP_traj 
#        print self.FOM_traj 
#        print self.RMS_traj1 
#        print self.RMS_traj2 
#        print self.MAP_traj1 
#        print self.MAP_traj2
#        print self.FOM_traj1
#        print self.FOM_traj2
#        return
#    
#    
#        start_time = self.Y_POS_CURSOR/self.VITESSE
#        start_time = start_time * self.facteurDilatation
#        start_line = self.time2line(start_time) + 10
#        
#        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
#        end_time = end_time * self.facteurDilatation
#        end_line = self.time2line(end_time)
#        
#        
#
#            
#           
#        for j in range (start_line, end_line):
#            if(self.Time[j+1]-self.Time[j-1] != 0):
#                deltaT = self.Time[j+1]-self.Time[j-1]                                  
#            if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
#                self.RMS_traj += (min(abs(self.Path_pos1[j] - self.Curs_pos[j]), abs(self.Path_pos2[j] - self.Curs_pos[j])))**2
#                self.MAP_traj += (abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for1[j]) + abs((self.Curs_pos[j+1] - self.Curs_pos[j-1])/(deltaT)*self.Subj_for2[j]))
#                self.FOM_traj += abs(self.Subj_for1[j]) + abs( self.Subj_for2[j])
#
#            elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
#                self.RMS_traj1 += (min(abs(self.Path_pos1[j] - self.Curs_pos1[j]), abs(self.Path_pos2[j] - self.Curs_pos1[j])))**2                                               
#                self.RMS_traj2 += (min(abs(self.Path_pos1[j] - self.Curs_pos2[j]), abs(self.Path_pos2[j] - self.Curs_pos2[j])))**2
#                self.MAP_traj1 += abs((self.Curs_pos1[j+1] - self.Curs_pos1[j-1])/(deltaT)*self.Subj_for1[j])
#                self.MAP_traj2 += abs((self.Curs_pos2[j+1] - self.Curs_pos2[j-1])/(deltaT)*self.Subj_for2[j])
#                self.FOM_traj1 += abs(self.Subj_for1[j])
#                self.FOM_traj2 += abs(self.Subj_for2[j])
#
#                      
#        if self.fileType == 'HFO' or self.fileType == 'HFOP' or self.fileType == 'PPHARD' or self.fileType == 'PPSOFT' or self.fileType == 'NOISY' or self.fileType == 'DELAYED' or self.fileType == 'HFOP_mou':
#            self.RMS_traj = sqrt(self.RMS_traj/(end_line - start_line))
#            self.MAP_traj /= (end_line - start_line)
#            self.FOM_traj /= (end_line - start_line)
#        elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ALONE' or self.fileType == 'ROBOT':
#            self.RMS_traj1 = sqrt(self.RMS_traj1/(end_line - start_line))
#            self.RMS_traj2 = sqrt(self.RMS_traj2/(end_line - start_line))
#            self.MAP_traj1 /= (end_line - start_line)
#            self.MAP_traj2 /= (end_line - start_line)
#            self.FOM_traj1 /= (end_line - start_line)
#            self.FOM_traj2 /= (end_line - start_line)

            
##################################################################################################### 
    def extractStartingTimes(self):
        self.startTimeLeader = []
        self.startTimeFollower = []  
        if self.fileType == 'HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            self.startTimeLeader1 = []
            self.startTimeLeader2 = []
            self.startTimeFollower1 = []
            self.startTimeFollower2 = []
        
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        

        trialNumber = 0
        if self.fileType == 'HFOP' or self.fileType == 'HFO':
            posLeader=[0]*len(self.Subj_pos1)
            posFollower=[0]*len(self.Subj_pos1)
            while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
    #            if mainApp.checkBoxTrialsVar[trialNumber].get() == 0:
    #                trialNumber += 1
    #                loop_start_time += cycle_time
    #                loop_start_line = self.time2line(loop_start_time)
    #                loop_stop_time  += cycle_time
    #                loop_stop_line  = self.time2line(loop_stop_time)
    #                continue            
                line_studied = loop_stop_line - self.time2line(0.5*self.facteurDilatation)
                barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
                if self.Path_pos1[line_studied] == self.Path_pos2[line_studied]: #SAME
                    loop_start_time += cycle_time
                    loop_start_line = self.time2line(loop_start_time)
                    loop_stop_time  += cycle_time
                    loop_stop_line  = self.time2line(loop_stop_time)
                    continue
        
                elif self.Path_pos1[line_studied] >= 5000: #ONE 1
                    if abs(barycentre - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2):
                        #Leader = Sujet 1
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos1[i]
                            posFollower[i] = self.Subj_pos2[i]
                    else:
                        #leader = sujet 2
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos2[i]
                            posFollower[i] = self.Subj_pos1[i]
                        
                elif self.Path_pos2[line_studied] >= 5000: #ONE 2
                    if abs(barycentre - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2):
                        #leader = sujet 2
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos2[i]
                            posFollower[i] = self.Subj_pos1[i]
                    else:
                        #Leader = Sujet 1
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos1[i]
                            posFollower[i] = self.Subj_pos2[i]
                            
                elif self.Path_pos1[line_studied] != self.Path_pos2[line_studied]: #OPPO
                    if abs(barycentre - self.Path_pos1[line_studied]) < abs(barycentre - self.Path_pos2[line_studied]):
                        #Leader = Sujet 1
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos1[i]
                            posFollower[i] = self.Subj_pos2[i]
                    elif abs(barycentre - self.Path_pos1[line_studied]) > abs(barycentre - self.Path_pos2[line_studied]):
                        #leader = sujet 2
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader[i] = self.Subj_pos2[i]
                            posFollower[i] = self.Subj_pos1[i]
                    else:
                        loop_start_time += cycle_time
                        loop_start_line = self.time2line(loop_start_time)
                        loop_stop_time  += cycle_time
                        loop_stop_line  = self.time2line(loop_stop_time)
                        continue
#OFFSET = mean of the position for the first 0.5s of the timelapse studied (allows to eliminate the residual difference between the 2 positions dur to cocontraction)
                offsetLeader = np.mean(posLeader[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2
                offsetFollower = np.mean(posFollower[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2            
                for i in range (loop_start_line, loop_stop_line):
                    posLeader[i] -= offsetLeader
                    posFollower[i] -= offsetFollower
                    
                timeOffset = self.analysisStartTime*self.facteurDilatation    
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posLeader[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posLeader[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeLeader.append(self.Time[i - loop_start_line])
                        break
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posFollower[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posFollower[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeFollower.append(self.Time[i - loop_start_line])
                        break
                                    
                trialNumber += 1
                loop_start_time += cycle_time
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = self.time2line(loop_stop_time)
    


        elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            posLeader1 = [0]*len(self.Subj_pos1)
            posLeader2 = [0]*len(self.Subj_pos2)
            posFollower1 = [0]*len(self.Subj_pos1)
            posFollower2 = [0]*len(self.Subj_pos2)
            while (loop_start_time <= end_time and loop_stop_time<= end_time):
                line_studied = loop_stop_line - self.time2line(0.5*self.facteurDilatation) #0.5 sec before end of the fork
                barycentre1 = np.mean(self.Curs_pos1[loop_start_line : loop_stop_line])
                barycentre2 = np.mean(self.Curs_pos2[loop_start_line : loop_stop_line])                
                if self.Path_pos1[line_studied] == self.Path_pos2[line_studied]:
                    loop_start_time += cycle_time
                    loop_start_line = self.time2line(loop_start_time)
                    loop_stop_time  += cycle_time
                    loop_stop_line  = self.time2line(loop_stop_time)
                    continue
 
                elif self.Path_pos1[line_studied] >= 5000 : #ONE1 case  
# ONE Case 1 == the human subject 1 doesn't have an indication, if the path chosen is the one of the subject 2 (== robot 1), then robot 1 is the leader, else (if the path chosen isn't the one given to robot 1), then human 1 is the leader
                    if abs(barycentre1 - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 1 chose
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Subj_pos1[i]
                            posFollower1[i] = self.Robot_pos1[i]
                    else: 
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Robot_pos1[i]
                            posFollower1[i] = self.Subj_pos1[i]
# ONE Case 1 == the human subject 2 has an indication, and the robot subject 2 doesn't, if the robot wins the choice anyway, he's the leader, else the human is.
                    if abs(barycentre2 - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means robot 2 chose
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Robot_pos2[i]
                            posFollower2[i] = self.Subj_pos2[i]
                    else: 
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Subj_pos2[i]
                            posFollower2[i] = self.Robot_pos2[i]    
                            
                elif self.Path_pos2[line_studied] >= 5000:
                    if abs(barycentre1 - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 2 chose
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Robot_pos1[i]
                            posFollower1[i] = self.Subj_pos1[i]
                    else: 
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Subj_pos1[i]
                            posFollower1[i] = self.Robot_pos1[i]
                    if abs(barycentre2 - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 2 chose
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Subj_pos2[i]
                            posFollower2[i] = self.Robot_pos2[i] 
                    else: 
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Robot_pos2[i]
                            posFollower2[i] = self.Subj_pos2[i]
                        
                else: # OPPO case
                    if abs(barycentre1 - self.Path_pos1[line_studied]) <= abs(barycentre1 - self.Path_pos2[line_studied]):
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Subj_pos1[i]
                            posFollower1[i] = self.Robot_pos1[i]
                    elif abs(barycentre1 - self.Path_pos1[line_studied]) > abs(barycentre1 - self.Path_pos2[line_studied]):
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader1[i] = self.Robot_pos1[i]
                            posFollower1[i] = self.Subj_pos1[i]
                    if abs(barycentre2 - self.Path_pos1[line_studied]) <= abs(barycentre2 - self.Path_pos2[line_studied]):
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Robot_pos2[i]
                            posFollower2[i] = self.Subj_pos2[i]
                    elif abs(barycentre2 - self.Path_pos1[line_studied]) > abs(barycentre2 - self.Path_pos2[line_studied]):
                        for i in range(loop_start_line, loop_stop_line):
                            posLeader2[i] = self.Subj_pos2[i]
                            posFollower2[i] = self.Robot_pos2[i]

                offsetLeader1 = np.mean(posLeader1[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2
                offsetFollower1 = np.mean(posFollower1[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2            
                offsetLeader2 = np.mean(posLeader2[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2
                offsetFollower2 = np.mean(posFollower2[loop_start_line : loop_start_line + self.time2line(0.5*self.facteurDilatation)]) - self.WINDOW_WIDTH/2            
                for i in range (loop_start_line, loop_stop_line):
                    posLeader1[i] -= offsetLeader1
                    posFollower1[i] -= offsetFollower1
                    posLeader2[i] -= offsetLeader2
                    posFollower2[i] -= offsetFollower2
                    
                timeOffset = self.analysisStartTime*self.facteurDilatation    
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posLeader1[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posLeader1[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeLeader1.append(self.Time[i - loop_start_line])
                        break
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posFollower1[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posFollower1[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeFollower1.append(self.Time[i - loop_start_line])
                        break
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posLeader2[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posLeader2[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeLeader2.append(self.Time[i - loop_start_line])
                        break
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(posFollower2[i] - self.WINDOW_WIDTH/2) > self.threshold and abs(posFollower2[i-1] - self.WINDOW_WIDTH/2) < self.threshold:
                        self.startTimeFollower2.append(self.Time[i - loop_start_line])
                        break
                        
                loop_start_time += cycle_time
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = self.time2line(loop_stop_time)  
            
        elif self.fileType == 'ALONE':
            self.startTimeLeader = []
            self.startTimeFollower = [] 
            



##################################################################################################### 
    def extractForces(self):
        self.forceIntLeader = []
        self.forceIntFollower = []    
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        forceLeader=[0]*len(self.Subj_for1)
        forceFollower=[0]*len(self.Subj_for1)
        trialNumber = 0
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
           
            line_studied = loop_stop_line + self.time2line(0.5*self.facteurDilatation)
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            if self.Path_pos1[line_studied] == self.Path_pos2[line_studied]:
                loop_start_time += cycle_time
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = self.time2line(loop_stop_time)
                continue
    
            elif self.Path_pos1[line_studied] >= 5000:
                if abs(barycentre - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2):
                    #Leader = Sujet 1
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for1[i]
                        forceFollower[i] = self.Subj_for2[i]
                else:
                    #leader = sujet 2
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for2[i]
                        forceFollower[i] = self.Subj_for1[i]
                    
            elif self.Path_pos2[line_studied] >= 5000:
                if abs(barycentre - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2):
                    #leader = sujet 2
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for2[i]
                        forceFollower[i] = self.Subj_for1[i]
                else:
                    #Leader = Sujet 1
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for1[i]
                        forceFollower[i] = self.Subj_for2[i]
                        
            elif self.Path_pos1[line_studied] != self.Path_pos2[line_studied]:
                if abs(barycentre - self.Path_pos1[line_studied]) < abs(barycentre - self.Path_pos2[line_studied]):
                    #Leader = Sujet 1
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for1[i]
                        forceFollower[i] = self.Subj_for2[i]
                elif abs(barycentre - self.Path_pos1[line_studied]) > abs(barycentre - self.Path_pos2[line_studied]):
                    #leader = sujet 2
                    for i in range(loop_start_line, loop_stop_line):
                        forceLeader[i] = self.Subj_for2[i]
                        forceFollower[i] = self.Subj_for1[i]
                else:
                    loop_start_time += cycle_time
                    loop_start_line = self.time2line(loop_start_time)
                    loop_stop_time  += cycle_time
                    loop_stop_line  = self.time2line(loop_stop_time)
                    continue

# Filtering
            N = 100
            tempL = [0]*len(forceLeader)
            tempF = [0]*len(forceFollower)
            for i in range(0,len(forceLeader)):
                if i<N:
                    for j in range (0,i):
                        tempL[i] += forceLeader[j]
                        tempF[i] += forceFollower[j]
                else:
                    for j in range (i-N,i):
                        tempL[i] += forceLeader[j]
                        tempF[i] += forceFollower[j]         
                tempL[i] /= min(i+1, N)
                tempF[i] /= min(i+1, N)
            
            for i in range(0, len(forceLeader)):
                forceLeader[i] = tempL[i]
                forceFollower[i] = tempF[i]
                
                
   
            timeOffset = self.PART_DURATION_CHOICE/2*self.facteurDilatation
            tempL = 0
            tempF = 0
            for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                tempL += forceLeader[i]*(self.Time[i] - self.Time[i-1])
                tempF += forceFollower[i]*(self.Time[i] - self.Time[i-1])
            
            self.forceIntLeader.append(tempL)
            self.forceIntFollower.append(tempF)
                   
            trialNumber += 1
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
            
##################################################################################################### 
    def intentionDetectionST(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        thresholdTimes = []
        endTimes = []
        X_right = 80
        X_left = -80
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            stTime1 = 0
            stTime2 = 0
            stTimeMin = 0
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            timeOffset = self.analysisStartTime*self.facteurDilatation

#############################
#            if abs(self.Subj_pos1[loop_start_line + self.time2line(timeOffset)]) >= self.threshold:
#                stTime1 = loop_start_time + timeOffset
#            else:
#                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
#                    if abs(self.Subj_pos1[i]) >= self.threshold and abs(self.Subj_pos1[i-1]) < self.threshold:
#                        stTime1 = self.Time[i]
#                        break
#                    
#            if abs(self.Subj_pos2[loop_start_line + self.time2line(timeOffset)]) >= self.threshold:
#                stTime2 = loop_start_time + timeOffset
#            else:
#                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
#                    if abs(self.Subj_pos2[i]) >= self.threshold and abs(self.Subj_pos2[i-1]) < self.threshold:
#                        stTime2 = self.Time[i]
#                        break
#            stTimeMin = min(stTime1, stTime2)
###########################                    
            if abs(self.Curs_pos[loop_start_line + self.time2line(timeOffset)]) >= self.threshold:
                stTimeMin = loop_start_time + timeOffset
            else:
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(self.Curs_pos[i]) >= self.threshold and abs(self.Curs_pos[i-1]) < self.threshold:
                        stTimeMin = self.Time[i]
                        print stTimeMin
                        break            
#############################
            
            for i in range(loop_start_line + self.time2line(timeOffset), loop_stop_line):
                if abs(self.Curs_pos[i] - X_right) <= self.threshold_ext and abs(self.Curs_pos[i-1] - X_right) > self.threshold_ext:
                    endTimes.append(self.Time[i - loop_start_line])
                    break
                elif abs(self.Curs_pos[i] - X_left) <= self.threshold_ext and abs(self.Curs_pos[i-1] - X_left) > self.threshold_ext:
                    endTimes.append(self.Time[i - loop_start_line])
                    break
           
            if self.Curs_pos[self.time2line(stTimeMin)]  < 0:
                expectedChoice = -1
            elif self.Curs_pos[self.time2line(stTimeMin)]  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            thresholdTimes.append(stTimeMin-loop_start_time)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)

        return(expectedChoices, finalChoices, thresholdTimes, endTimes)

            
##################################################################################################### 
    def intentionDetectionSTXM(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        thresholdTimes = []
        sample_freq = 2000
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            stTimeMin = 0
            timer = 0
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            start_line = self.time2line(loop_start_time + self.analysisStartTime*self.facteurDilatation)
            stop_line = self.time2line(loop_start_time + self.analysisStopTime*self.facteurDilatation)
            
            if abs(self.Subj_pos1[start_line]) >= self.threshold:
                stTimeMin = loop_start_time + self.analysisStartTime*self.facteurDilatation
            else:
                for i in range (start_line, stop_line):
                    if abs(self.Curs_pos[i]) >= self.threshold and abs(self.Curs_pos[i-1]) < self.threshold:
                        stTimeMin = self.Time[i]
                        break
                
            if stTimeMin == 0:
                stTimeMin = loop_start_time + self.analysisStopTime*self.facteurDilatation
                if self.Curs_pos[stop_line]  < 0:
                    expectedChoice = -1
                elif self.Curs_pos[start_line]  > 0:
                    expectedChoice = 1
                else:
                    expectedChoice = 0                
            else:            
                if self.Curs_pos[self.time2line(stTimeMin)]  < 0:
                    expectedChoice = -1
                elif self.Curs_pos[self.time2line(stTimeMin)]  > 0:
                    expectedChoice = 1
                else:
                    expectedChoice = 0

######################################
#            for i in range(start_line, stop_line):
#                if abs(self.Curs_pos[i]) < self.threshold:
#                    timer = 0
#                else:
#                    timer += 1
#                if timer > sample_freq*self.timerMax:
#                    stTimeMin = self.Time[i] - self.timerMax
#                    break
#                
#            if timer == 0:
#                stTimeMin = self.Time[stop_line]
#                if self.Curs_pos[stop_line]  < 0:
#                    expectedChoice = -1
#                elif self.Curs_pos[stop_line]  > 0:
#                    expectedChoice = 1
#                else:
#                    expectedChoice = 0                
#            else:            
#                if self.Curs_pos[self.time2line(stTimeMin)]  < 0:
#                    expectedChoice = -1
#                elif self.Curs_pos[self.time2line(stTimeMin)]  > 0:
#                    expectedChoice = 1
#                else:
#                    expectedChoice = 0
###################################

                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            thresholdTimes.append(stTimeMin-loop_start_time)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)

        return(expectedChoices, finalChoices, thresholdTimes)
            
                        
##################################################################################################### 
    def intentionDetectionXM(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        
        Xmoy1 = 0
        Xmoy2 = 0
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)
            stop_line = loop_start_line + self.time2line(self.analysisStopTime*self.facteurDilatation)
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            Xmoy1 = np.mean(self.Curs_pos[start_line : stop_line])
            Xmoy2 = np.mean(self.Curs_pos[start_line : stop_line])
            
            if Xmoy1  < 0:
                expectedChoice = -1
            elif Xmoy1  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices)


##################################################################################################### 
    def intentionDetectionXT(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        
        XcT = 0
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        endTimes = []
        X_right = 80
        X_left = -80
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            XcT = self.Curs_pos[loop_start_line + self.time2line(self.analysisTime*self.facteurDilatation)]
                
            if XcT  < 0:
                expectedChoice = -1
            elif XcT  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices, endTimes)
        
##################################################################################################### 
    def intentionDetectionVM(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        VM = 0
        Curs_pos_filt = [0]*len(self.Curs_pos)
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            
            nyq = 0.5*2000
            low = self.low_pass/nyq
            F_order= 2 #order of the filter
            b, a =  sig.butter(F_order, low, btype = 'low')
            Curs_pos_filt[loop_start_line:loop_stop_line] = sig.lfilter(b, a, self.Curs_pos[loop_start_line:loop_stop_line])
            
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)
            stop_line = loop_start_line + self.time2line(self.analysisStopTime*self.facteurDilatation)
            V = [0]*len(self.Curs_pos)
            for i in range(start_line+1, stop_line-1):
                V[i] = (Curs_pos_filt[i+1] - Curs_pos_filt[i-1])/(2*(self.Time[i+1]-self.Time[i]))
            VM = np.mean(V[start_line:stop_line])
            
            if VM  < 0:
                expectedChoice = -1
            elif VM  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices)

##################################################################################################### 
    def intentionDetectionVT(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        
        VcT = 0
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        Curs_pos_filt = [0]*len(self.Curs_pos)
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            nyq = 0.5*2000
            low = self.low_pass/nyq
            F_order= 2 #order of the filter
            b, a =  sig.butter(F_order, low, btype = 'low')
            Curs_pos_filt[loop_start_line:loop_stop_line] = sig.lfilter(b, a, self.Curs_pos[loop_start_line:loop_stop_line])

            V = [0]*len(self.Curs_pos)
            for i in range(loop_start_line+1, loop_stop_line-1):
                V[i] = (Curs_pos_filt[i+1] - Curs_pos_filt[i-1])/(2*(self.Time[i+1]-self.Time[i]))
                
            VcT = V[loop_start_line + self.time2line(self.analysisTime*self.facteurDilatation)]
            
            if VcT  < 0:
                expectedChoice = -1
            elif VcT  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices)


##################################################################################################### 
    def intentionDetectionFM(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        FM = 0
        Force_filt = [0]*len(self.Subj_for1)
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
            
            for i in range (loop_start_line, loop_stop_line):
                Force_filt[i] = self.Subj_for1[i] + self.Subj_for2[i]
            
            nyq = 0.5*2000
            low = self.low_pass/nyq
            F_order= 2 #order of the filter
            b, a =  sig.butter(F_order, low, btype = 'low')
            Force_filt[loop_start_line:loop_stop_line] = sig.lfilter(b, a, Force_filt[loop_start_line:loop_stop_line])
            
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)
            stop_line = loop_start_line + self.time2line(self.analysisStopTime*self.facteurDilatation)

            FM = np.mean(Force_filt[start_line:stop_line])
            
            if FM  < 0:
                expectedChoice = -1
            elif FM  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices)
        
##################################################################################################### 
    def intentionDetectionSRMS(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        SRMS = 0
        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
                        
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)
            stop_line = loop_start_line + self.time2line(self.analysisStopTime*self.facteurDilatation)

            M = np.mean(self.Curs_pos[start_line:stop_line])
            for i in range(start_line, stop_line):
                SRMS += np.sign(self.Curs_pos[i] - M)*(self.Curs_pos[i] - M)**2
            
            if SRMS  < 0:
                expectedChoice = -1
            elif SRMS  > 0:
                expectedChoice = 1
            else:
                expectedChoice = 0
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices)
        
##################################################################################################### 
    def intentionDetectionXI(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        

        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        thresh_times = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            XI = 0
            TI = 0            
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
                        
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)

            for i in range(start_line, loop_stop_line):
                XI += self.Curs_pos[i]
                if XI >= self.threshold:
                    expectedChoice = 1
                    TI = self.Time[i]
                    break
                elif XI < -self.threshold:
                    expectedChoice = -1
                    TI = self.Time[i]
                    break
            if abs(XI) < self.threshold:
                expectedChoice = 0
                TI = self.Time[loop_start_line]+1
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            thresh_times.append(TI - loop_start_time)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices, thresh_times)
        
##################################################################################################### 
    def intentionDetectionXIS(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        

        expectedChoice = 0
        finalChoice = 0
        expectedChoices = []
        finalChoices = []
        thresh_times = []
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            XIP = 0
            XIM = 0
            TI = 0            
            barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
                        
            start_line = loop_start_line + self.time2line(self.analysisStartTime*self.facteurDilatation)

            for i in range(start_line, loop_stop_line):
                if self.Curs_pos[i] >= 0:
                    XIP += self.Curs_pos[i]
                else:
                    XIM += self.Curs_pos[i]
                    
                if XIP >= self.threshold:
                    expectedChoice = 1
                    TI = self.Time[i]
                    break
                elif XIM < -self.threshold:
                    expectedChoice = -1
                    TI = self.Time[i]
                    break
            if abs(XIP) < self.threshold and abs(XIM) < self.threshold:
                expectedChoice = 0
                TI = self.Time[loop_start_line]+1
                
            if barycentre < 0:
                finalChoice = -1
            elif barycentre > 0:
                finalChoice = 1
            else:
                finalChoice = 0
                
            expectedChoices.append(expectedChoice)
            finalChoices.append(finalChoice)
            thresh_times.append(TI - loop_start_time)
            
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(expectedChoices, finalChoices, thresh_times)
                

        
##################################################################################################### 
    def extractEndTime(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        
        endTimes = []
        X_right = 80
        X_left = -80
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):    
            for i in range(loop_start_line + self.time2line(0.4*self.facteurDilatation), loop_stop_line):
                if abs(self.Curs_pos[i] - X_right) <= self.threshold_ext and abs(self.Curs_pos[i-1] - X_right) > self.threshold_ext:
                    endTimes.append(self.Time[i - loop_start_line])  
                    break
                elif abs(self.Curs_pos[i] - X_left) <= self.threshold_ext and abs(self.Curs_pos[i-1] - X_left) > self.threshold_ext:
                    endTimes.append(self.Time[i - loop_start_line])  
                    break
                
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        
        return(endTimes)
        
        
##################################################################################################### 
    def analyzeDominance(self):
    
        start_time = self.Y_POS_CURSOR/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur - ecart entre la position du curseur et le bord de la fenetre - duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY #Start of the choice part
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK #End of the fork
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation

        for i in range(0, len(self.Time)-1):
            if self.Time[i+1] - self.Time[i] > 0.5:
                end_time = self.Time[i]
                print "broken" 
                break
            
        if self.fileType == 'HFOP' or self.fileType == 'HFO' or self.fileType == 'HFOP_mou':
            while (loop_start_time <= end_time and loop_stop_time<= end_time):
                line_studied = loop_stop_line - self.time2line(1*self.facteurDilatation) #1 sec before end of the fork
                barycentre = np.mean(self.Curs_pos[loop_start_line : loop_stop_line])
                if self.Path_pos1[line_studied] == self.Path_pos2[line_studied] : #SAME case
                    self.nbChoices1 += 0
                elif self.Path_pos1[line_studied] >= 5000 : #ONE1 case      
                    if abs(barycentre - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 1 chose
                        self.nbChoices1 += 1
                        self.nbConflicts += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoices1 += 0
                elif self.Path_pos2[line_studied] >= 5000:
                    if abs(barycentre - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 2 chose
                        self.nbChoices2 += 1
                        self.nbConflicts += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoices1 += 0
                else: # OPPO case
                    if abs(barycentre - self.Path_pos1[line_studied]) < 1.3*abs(barycentre - self.Path_pos2[line_studied]):
                        self.nbChoices1 += 1
                        self.nbConflicts += 1
                    elif abs(barycentre - self.Path_pos1[line_studied]) > 1.3*abs(barycentre - self.Path_pos2[line_studied]):
                        self.nbChoices2 += 1
                        self.nbConflicts += 1
                    else:
                        self.nbChoices1 += 1
                        self.nbChoices2 += 1
                        self.nbConflicts += 1
                
                for i in range (loop_start_line, loop_stop_line):
                    self.distParcourue1 += abs(self.Subj_pos1[i] - self.Subj_pos1[i-1])
                    self.distParcourue2 += abs(self.Subj_pos2[i] - self.Subj_pos2[i-1])

                loop_start_time += cycle_time
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = self.time2line(loop_stop_time)  
                    
        elif self.fileType =='HVP' or self.fileType =='KVP' or self.fileType =='KVP' or self.fileType == 'ROBOT':
            while (loop_start_time <= end_time and loop_stop_time<= end_time):
                line_studied = loop_stop_line - self.time2line(0.5*self.facteurDilatation) #0.5 sec before end of the fork
                barycentre1 = np.mean(self.Curs_pos1[loop_start_line : loop_stop_line])
                barycentre2 = np.mean(self.Curs_pos2[loop_start_line : loop_stop_line])                
                if self.Path_pos1[line_studied] == self.Path_pos2[line_studied] : #SAME case
                    self.nbChoices1 += 0
                elif self.Path_pos1[line_studied] >= 5000 : #ONE1 case      
                    if abs(barycentre1 - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 1 chose
                        self.nbChoicesH1 += 1
                        self.nbConflicts1 += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoicesH1 += 0
                    if abs(barycentre2 - self.Path_pos2[line_studied]) > 1.3*abs(self.Path_pos2[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means robot 2 chose
                        self.nbChoicesR2 += 1
                        self.nbConflicts2 += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoicesR2 += 0                    
                elif self.Path_pos2[line_studied] >= 5000:
                    if abs(barycentre1 - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 2 chose
                        self.nbChoicesR1 += 1
                        self.nbConflicts1 += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoices1 += 0
                    if abs(barycentre2 - self.Path_pos1[line_studied]) > 1.3*abs(self.Path_pos1[line_studied] - self.WINDOW_WIDTH/2): #If the path choosen is different from the only one given to the subjects it means subject 2 chose
                        self.nbChoicesH2 += 1
                        self.nbConflicts2 += 1
                    else: #The path chosen is the one given so no conflict
                        self.nbChoicesH2 += 0
                else: # OPPO case
                    if abs(barycentre1 - self.Path_pos1[line_studied]) < abs(barycentre1 - self.Path_pos2[line_studied]):
                        self.nbChoicesH1 += 1
                        self.nbConflicts += 1
                    elif abs(barycentre1 - self.Path_pos1[line_studied]) > abs(barycentre1 - self.Path_pos2[line_studied]):
                        self.nbChoicesR1 += 1
                        self.nbConflicts += 1
                    else:
                        self.nbChoicesH1 += 1
                        self.nbChoicesR1 += 1
                        self.nbConflicts += 1
                    if abs(barycentre2 - self.Path_pos1[line_studied]) < abs(barycentre2 - self.Path_pos2[line_studied]):
                        self.nbChoicesR2 += 1
                        self.nbConflicts += 1
                    elif abs(barycentre2 - self.Path_pos1[line_studied]) > abs(barycentre2 - self.Path_pos2[line_studied]):
                        self.nbChoicesH2 += 1
                        self.nbConflicts += 1
                    else:
                        self.nbChoicesH2 += 1
                        self.nbChoicesR2 += 1
                        self.nbConflicts += 1
                        
                loop_start_time += cycle_time
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = self.time2line(loop_stop_time)  
            
        elif self.fileType == 'ALONE':
            self.nbChoices1 = 0
            self.nbChoices2 = 0
            self.nbConflicts = 0
            
                              
       
##################################################################################################### 
    def analyzeTrajectory(self):
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START + 2*self.PART_DURATION_BODY
        loop_stop_time  = loop_start_time  + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time = self.PART_DURATION_REGRP + self.PART_DURATION_BODY*2 + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK
        cycle_time = cycle_time * self.facteurDilatation
        
        
        stTime1 = 0
        stTime2 = 0
        stTime = 0
        endTime = 0
        k=0
        xi = 0
        xf = 0
        
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            
            timeOffset = self.analysisStartTime*self.facteurDilatation    
            for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                if abs(self.Subj_pos1[i]) > self.threshold and abs(self.Subj_pos1[i-1]) < self.threshold:
                    stTime1 = self.Time[i]
                    break
            for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                if abs(self.Subj_pos2[i]) > self.threshold and abs(self.Subj_pos2[i-1]) < self.threshold:
                    stTime2 = self.Time[i]
                    break
                
            stTime = min(stTime1, stTime2)
            
            if stTime1 < stTime2:
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if (abs(self.WINDOW_WIDTH/10 - self.Subj_pos1[i]) < self.threshold_ext and abs(self.WINDOW_WIDTH/10 - self.Subj_pos1[i-1]) > self.threshold_ext) or (abs(-self.WINDOW_WIDTH/10 - self.Subj_pos1[i]) < self.threshold_ext and abs(-self.WINDOW_WIDTH/10 - self.Subj_pos1[i-1]) > self.threshold_ext):
                        endTime = self.Time[i]
                        break
                    
                trajectory = [0]*(self.time2line(endTime) - self.time2line(stTime))
                time = [0]*(self.time2line(endTime) - self.time2line(stTime))
                for i in range(0, len(trajectory)):
                    trajectory[i] = self.Subj_pos1[self.time2line(stTime) + i]
                    time[i] = self.Time[i]
                xi = self.Subj_pos1[self.time2line(stTime)]
                xf = self.Subj_pos1[self.time2line(endTime)]
                    
            else:
                for i in range (loop_start_line + self.time2line(timeOffset), loop_stop_line):
                    if abs(self.WINDOW_WIDTH/10 - self.Subj_pos2[i]) < self.threshold_ext and abs(self.WINDOW_WIDTH/10 - self.Subj_pos2[i-1]) > self.threshold_ext or (abs(-self.WINDOW_WIDTH/10 - self.Subj_pos2[i]) < self.threshold_ext and abs(-self.WINDOW_WIDTH/10 - self.Subj_pos2[i-1]) > self.threshold_ext):
                        endTime = self.Time[i]
                        break 
                              
                trajectory = [0]*(self.time2line(endTime) - self.time2line(stTime))
                time = [0]*(self.time2line(endTime) - self.time2line(stTime))
                for i in range(0, len(trajectory)):
                    trajectory[i] = self.Subj_pos2[self.time2line(stTime) + i]
                    time[i] = self.Time[i]
                xi = self.Subj_pos2[self.time2line(stTime)]
                xf = self.Subj_pos2[self.time2line(endTime)]
                    
            print k, stTime, endTime, self.Subj_pos2[self.time2line(stTime)]
            
            ideal_trajectory = [0]*len(trajectory)
            tf = endTime - stTime
            for i in range(len(ideal_trajectory)):
                ideal_trajectory[i] = xi + (xf - xi)*(10*(time[i]/tf)**3 - 15*(time[i]/tf)**4 + 6*(time[i]/tf)**5)
            

            plt.figure(k)
            plt.plot(trajectory, time, 'b-')
            plt.plot(ideal_trajectory, time, 'g-')
            plt.draw()
            
            print k, stTime - loop_start_time, endTime - loop_start_time
            
            k += 1
            loop_start_time += cycle_time
            loop_start_line = self.time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = self.time2line(loop_stop_time)
        plt.show()
#####################################################################################################
    def MelendezCalderon(self):        
        start_time = float(self.Y_POS_CURSOR)/self.VITESSE
        
        end_time = (start_time + self.PATH_DURATION - self.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
        end_time = end_time * self.facteurDilatation    
        
        loop_start_time = start_time + self.PART_DURATION_START
        loop_stop_time  = loop_start_time + self.PART_DURATION_BODY
        
        loop_start_time = loop_start_time * self.facteurDilatation
        loop_start_line = self.time2line(loop_start_time)
        
        loop_stop_time  = loop_stop_time * self.facteurDilatation
        loop_stop_line  = self.time2line(loop_stop_time)
        
        cycle_time1 = self.PART_DURATION_BODY
        cycle_time1 = cycle_time1 * self.facteurDilatation
        
        cycle_time2 = self.PART_DURATION_BODY + self.PART_DURATION_CHOICE + self.PART_DURATION_FORK + self.PART_DURATION_REGRP
        cycle_time2 = cycle_time2 * self.facteurDilatation  
        
        cycle_type = 1
        F_BODY = 1.0/self.PART_DURATION_BODY

        
        while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
            A = [0]*5
            Ap = [0]*5
            T = [0]*5
            Subj_for1_filtered = []
            D = [0]*10
        #Creation des templates
            N = (loop_stop_line -  loop_start_line)
            #Initialisation des vecteurs templates en fonction du nombre de data points
            for i in range(0,5):
                T[i] = [i]*N
            #if the BODY curve in on the right, then we can model the curve as -cos(wt)+1 after normalisation ==> (melendez) + 1
            if self.Path_pos1[loop_start_line + int(N/2)] >= 0:
                #D-B
                for k in range(0,N):
                    T[0][k] = 1 + sin(2*pi*F_BODY*k/N)
                #F-E
                for k in range(0,N):
                    T[1][k] = 1 + (cos(4*pi*F_BODY*k/N + pi) + 1)/2
                #D-sC
                for k in range(0,N):
                    T[2][k] = 1 - cos(2*pi*F_BODY*k/N)
                #D-sF
                for k in range(0,N):
                    T[2][k] = 1 + (cos(2*pi*F_BODY*k/N + pi) - 1)/2
                #F-E
                for k in range(0,N):
                    T[2][k] = 1 + (1 - cos(2*pi*F_BODY*k/N + pi))/2
            #if the BODY curve is on the left, then we can model the curve as cos(wt) - 1 after normalisation ==> -(melendez) - 1
            if self.Path_pos1[loop_start_line + int(N/2)] < 0:
                #D-B
                for k in range(0,N):
                    T[0][k] = -1 - sin(2*pi*F_BODY*k/N)
                #F-E
                for k in range(0,N):
                    T[1][k] = -1 - (cos(4*pi*F_BODY*k/N + pi) + 1)/2
                #D-sC
                for k in range(0,N):
                    T[2][k] = -1 + cos(2*pi*F_BODY*k/N)
                #D-sF
                for k in range(0,N):
                    T[2][k] = -1 - (cos(2*pi*F_BODY*k/N + pi) - 1)/2
                #F-E
                for k in range(0,N):
                    T[2][k] = -1 - (1 - cos(2*pi*F_BODY*k/N + pi))/2            

            #Apply low pass filter to data
            nyq = 0.5*2000 #moitie de la freq d'echantillonage
            low = self.low_pass/nyq #low-pass freq
            F_order= 2 #order of the filter
            b, a =  sig.butter(F_order, low, btype = 'low')
            Subj_for1_filtered = sig.lfilter(b, a, self.Subj_for1[loop_start_line:loop_stop_line])
            
            #Normalisation du vecteur force
            MaxF = max(Subj_for1_filtered)
            MinF = min(Subj_for1_filtered)
            if isAllPos(Subj_for1_filtered):
                for k in range(0,N):
                    Subj_for1_filtered[k] = (Subj_for1_filtered[k] - MinF)/(MaxF - MinF)                   
            elif isAllNeg(Subj_for1_filtered):
                for k in range(0,N):
                    Subj_for1_filtered[k] = (Subj_for1_filtered[k] - MaxF)/(MaxF - MinF)
            else:
                for k in range(0,N):
                    if Subj_for1_filtered[k] >= 0:
                        Subj_for1_filtered[k] = Subj_for1_filtered[k]/MaxF
                    else:
                        Subj_for1_filtered[k] = Subj_for1_filtered[k]/abs(MinF)

            #Re filter to remove discontinuities from normalization
            low = self.low_pass/nyq #low-pass freq
            F_order= 2 #order of the filter
            b, a =  sig.butter(F_order, low, btype = 'low')            
            Subj_for1_filtered = sig.lfilter(b, a, Subj_for1_filtered)
            
            #sanity check
            if len(Subj_for1_filtered) != N:
                print 'ERROR: Array length uncompatible', N, '!=', len(Subj_for1_filtered)
                break
            
            #Computation of the Euclidean distance between the normalized force profiles and the templates
            for i in range(0, 5):
                temp = 0
                for k in range(0,N):
                    temp += (Subj_for1_filtered[k] - T[i][k])**2  
                A[i] = sqrt(temp)

            #Computation of the Euclidean distance between the normalized force profiles and the reciprocal templates
            for i in range(0, 5):
                temp = 0
                for k in range(0,N):
                    temp += (-Subj_for1_filtered[k] - T[i][k])**2  
                Ap[i] = sqrt(temp)

            #Concatenate the results array
            B = A + Ap           
            
            #Compute the probability of a pattern occuring
            C = [0]*len(B)
            for i in range(0, len(B)):
                C[i] = 1/B[i]
            for i in range(0, len(B)):
                D[i] = C[i]/sum(C)

            self.D_global.append(D)    
    


            if cycle_type == 1:
                loop_start_time += cycle_time1
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time1
                loop_stop_line  = self.time2line(loop_stop_time)
                cycle_type = 2
            elif cycle_type == 2:
                loop_start_time += cycle_time2
                loop_start_line = self.time2line(loop_start_time)
                loop_stop_time  += cycle_time2
                loop_stop_line  = self.time2line(loop_stop_time)
                cycle_type = 1
        
        
        
##################################################################################################### 
    def resetData(self):
        self.finalTime = 0.0
        self.timeOffset = 0.0
        self.facteurDilatation = 0.0
        self.SUBJECT_NAME1 = ''
        self.SUBJECT_NAME2 = ''
        self.PATH_DURATION = 0.0
        self.VITESSE =0.0
        self.Y_POS_CURSOR =0.0
        self.PART_DURATION_BODY =0.0
        self.PART_DURATION_CHOICE =0.0
        self.PART_DURATION_FORK =0.0
        self.PART_DURATION_REGRP =0.0
        self.PART_DURATION_START =0.0
        self.POSITION_OFFSET =0.0
        self.SENSITIVITY =0.0
        self.WINDOW_WIDTH =0.0 
        self.WINDOW_LENGTH =0.0
        
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Curs_pos  = []
        self.Subj_pos1 = []
        self.Subj_pos2 = []
        self.Subj_for1 = []
        self.Subj_for2 = []
        
        self.TIME_WINDOW_BEFORE = 0
        self.TIME_WINDOW_AFTER = 0
        
##################################################################################################### 
    def clearData(self):
        self.finalTime = None
        self.timeOffset = None
        self.facteurDilatation = None
        self.SUBJECT_NAME1 = None
        self.SUBJECT_NAME2 = None
        self.PATH_DURATION = None
        self.VITESSE = None
        self.Y_POS_CURSOR = None
        self.PART_DURATION_BODY = None
        self.PART_DURATION_CHOICE = None
        self.PART_DURATION_FORK = None
        self.PART_DURATION_REGRP = None
        self.PART_DURATION_START = None
        self.POSITION_OFFSET = None
        self.SENSITIVITY = None
        self.WINDOW_WIDTH = None
        self.WINDOW_LENGTH = None
        
        self.Time      =  None
        self.Path_pos1 = None
        self.Path_pos2 = None
        self.Curs_pos  = None
        self.Subj_pos1 = None
        self.Subj_pos2 = None
        self.Subj_for1 = None
        self.Subj_for2 = None
        
        self.TIME_WINDOW_BEFORE = None
        self.TIME_WINDOW_AFTER = None
        
        
#####################################################################################################             
    def time2line(self, time):
        for i in range (1, len(self.Time)):
            if self.Time[i] >= time and self.Time[i-1] < time:
                return i
        return -1

#####################################################################################################
#####################################################################################################
def customMax(n):
    if not n:
        return 0
    else:
        return max(n)
#####################################################################################################
def removePoints(matrix):
    while(1):
        try:
            matrix[0].remove(".")
        except: 
            break
    while(1):        
        try:
            matrix[1].remove(".")
        except:
            break
    while(1):        
        try:
            matrix[2].remove(".")
        except:
            break
    if not matrix:
        matrix=[0,0,0]
        
    return matrix
    
def isAllPos(n):
    for i in range(0,len(n)):
        if n[i] < 0:
            return False
    return True
    
def isAllNeg(n):
    for i in range(0,len(n)):
        if n[i] > 0:
            return False
    return True