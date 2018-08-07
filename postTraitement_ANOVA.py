#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:27:32 2017

@author: lucas
"""

from scipy import stats
from Tkinter import *
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *
import pandas
from postTrait_Module import *
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import os
import wx
import wx.lib.agw.multidirdialog as MDD



class GUIpostTraitementClass:
    
    def __init__(self, master):
        
        self.master = master
        
        self.frameTOPLEFT = Frame(master)
        self.frameTOPLEFT.grid(row=0,column=0)
        self.frameTOPRIGHT = Frame(master)
        self.frameTOPRIGHT.grid(row=0,column=1)
        self.frameBOT = Frame(master)
        self.frameBOT.grid(row=1, column=0, columnspan=2)
        
        self.heightTextZone = 1
        self.textZone = Text(self.frameTOPLEFT, height = self.heightTextZone, width = 150)
        self.textZone.grid(row = 0, columnspan = 8, padx=5, pady = 5)
        
        self.labelTimeWB = Label(self.frameTOPLEFT, text = 'Time Window Before :')
        self.labelTimeWB.grid(row = 1, column = 0, sticky = E)
        self.entryTimeWB = Entry(self.frameTOPLEFT, width = 3)
        self.entryTimeWB.grid(row=1, column=1, sticky = W)
        self.entryTimeWB.insert(0, '1')
        
        self.labelTimeWA = Label(self.frameTOPLEFT, text = 'Time Window After :')
        self.labelTimeWA.grid(row = 2, column = 0, sticky = E)
        self.entryTimeWA = Entry(self.frameTOPLEFT, width = 3)
        self.entryTimeWA.grid(row=2, column=1, sticky = W)
        self.entryTimeWA.insert(0, '1')
        
        self.labelForceLimit = Label(self.frameTOPLEFT, text = 'Force filter limit :')
        self.labelForceLimit.grid(row=1, column = 2, sticky = E)
        self.entryForceLimit = Entry(self.frameTOPLEFT, width = 3)
        self.entryForceLimit.grid(row =1, column = 3, sticky = W)
        self.entryForceLimit.insert(0, '15')
        
        self.labelDataKept = Label(self.frameTOPLEFT, text = 'Data kept :')
        self.labelDataKept.grid(row = 2, column = 2, sticky = E)
        self.dataKeptVar = StringVar()
        self.dataKeptVar.set('INTER')
        self.dataKeptMenu = Menubutton(self.frameTOPLEFT, textvariable=self.dataKeptVar, relief=RAISED, width = 5)
        self.dataKeptMenu.menu  =  Menu ( self.dataKeptMenu, tearoff = 0 )
        self.dataKeptMenu["menu"]  =  self.dataKeptMenu.menu
        self.dataKeptMenu.menu.add_command(label = 'INTER', command = self.setINTER)
        self.dataKeptMenu.menu.add_command(label = 'EXTER', command = self.setEXTER)
        self.dataKeptMenu.grid(row = 2, column = 3, sticky = W)
        
        self.labelPartAnalyzed = Label(self.frameTOPLEFT, text = 'Part analyzed :')
        self.labelPartAnalyzed.grid(row = 1, column = 4, sticky = E)
        self.partAnalyzedVar = StringVar()
        self.partAnalyzedVar.set('CHOICES')
        self.partAnalyzedMenu = Menubutton(self.frameTOPLEFT, textvariable=self.partAnalyzedVar, relief=RAISED, width = 6)
        self.partAnalyzedMenu.menu  =  Menu ( self.partAnalyzedMenu, tearoff = 0 )
        self.partAnalyzedMenu["menu"]  =  self.partAnalyzedMenu.menu
        self.partAnalyzedMenu.menu.add_command(label = 'CHOICES', command = self.setCHOICES)
        self.partAnalyzedMenu.menu.add_command(label = 'BODY', command = self.setBODY)
        self.partAnalyzedMenu.grid(row = 1, column = 5, sticky = W)
        
        self.buttonAddFiles = Button(self.frameTOPRIGHT, text = 'Add Files', command = self.addFiles, width = 18)
        self.buttonAddFiles.grid(row = 0, column = 0)

        self.buttonAddDirectories = Button(self.frameTOPRIGHT, text = 'Add Directories', command = self.addDirectories, width = 18)
        self.buttonAddDirectories.grid(row = 1, column = 0, pady = 5)
        
        self.buttonProcess = Button(self.frameTOPRIGHT, text = 'Process Files', command = self.process, width = 18)
        self.buttonProcess.grid(row = 2, column = 0)
        self.buttonProcess.config(state=DISABLED)

#        self.saveVar = IntVar()        
#        self.checkBoxSave = Checkbutton(self.frameTOPRIGHT, text = 'Save individual results', variable = self.saveVar, width = 18)
#        self.checkBoxSave.grid(row = 2, column = 0)
#        self.checkBoxSave.select()

        self.labelResultsText3= Label(self.frameBOT, text = '[ SAME, ONE, OPPO]').grid(row = 0, column = 1)
        self.labelResultsText1= Label(self.frameBOT, text = 'Results (HFOP) :').grid(row = 1, column = 0, sticky = W)
        self.labelResultsText2= Label(self.frameBOT, text = 'Results (HFO) :').grid(row = 2, column = 0, sticky = W)

        self.resultsHFOP = []
        self.resultsLabelHFOP = StringVar()
        self.labelResultsHFOP = Label(self.frameBOT, textvariable = self.resultsLabelHFOP)
        self.labelResultsHFOP.grid(row=1,column=1)
        
        self.resultsHFO = []
        self.resultsLabelHFO = StringVar()
        self.labelResultsHFO = Label(self.frameBOT, textvariable = self.resultsLabelHFO)
        self.labelResultsHFO.grid(row=2,column=1)
        
        self.buttonExport = Button(self.frameBOT, text = 'Export Results', command = self.exportResults)
        self.buttonExport.grid(row = 1, column = 2, padx = 10)
        self.buttonExport.config(state=DISABLED)

        self.messageLabel = StringVar()        
        self.stateLabel = Label(self.frameBOT, textvariable = self.messageLabel)
        self.stateLabel.grid(row=2, column=2)
        

    def addFiles(self):
        filesToAdd = askopenfilenames(initialdir = "/home/lucas/Documents/Manip")
        filesToAdd = self.master.tk.splitlist(filesToAdd)
        for l in filesToAdd:
            self.textZone.insert(END, l+'\n')
            self.heightTextZone +=1
            if self.heightTextZone >= 40:
                self.heightTextZone = 40
            self.textZone.config(height=self.heightTextZone)
        if filesToAdd:
            self.buttonProcess.config(state=NORMAL)
            
    def addDirectories(self):
        app = wx.App(0)
        dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/home/lucas/Documents/Manip/",  # defaultPath="C:/Users/users/Desktop/",
                             agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)    
        if dlg.ShowModal() != wx.ID_OK:
            print("You Cancelled The Dialog!")
            dlg.Destroy()    
        paths = dlg.GetPaths()    
        dlg.Destroy()
        app.MainLoop()
        
        for path in enumerate(paths):
            directory= path[1].replace('Home directory','/home/lucas')
            filesToAdd = os.listdir(directory)
            for l in filesToAdd:
                l = directory + '/' + l
                self.textZone.insert(END, l+'\n')
                self.heightTextZone +=1
                if self.heightTextZone >= 40:
                    self.heightTextZone = 40
                self.textZone.config(height=self.heightTextZone)
            if directory:
                self.buttonProcess.config(state=NORMAL)



    def process(self):
        self.buttonExport.config(state=DISABLED)
        self.messageLabel.set('')
        self.fileList = self.textZone.get(0.0, END).split('\n')
        for i in range(0, len(self.fileList)):
            self.fileList[i] = self.fileList[i].encode('ascii','ignore')
        while(1):
            try:
                self.fileList.remove('')
            except:
                break
        processFiles()

        
    def exportResults(self):
        saveFile = asksaveasfile(mode='w', initialdir = '../post-traitement/')
        if saveFile != None:
            writeToFile(saveFile)
            
    def setINTER(self):
        self.dataKeptVar.set('INTER')
    def setEXTER(self):
        self.dataKeptVar.set('EXTER')
    def setCHOICES(self):
        self.partAnalyzedVar.set('CHOICES')
    def setBODY(self):
        self.partAnalyzedVar.set('BODY')       
        

def main():
    global GUIpostTraitement
    root = Tk()
    root.title("GUI post-traitement")
    
    GUIpostTraitement = GUIpostTraitementClass(root)

    root.mainloop()


def processFiles():
    global GUIpostTraitement, RMS_all_HFOP, RMS_all_HFO, perf_HFOP, perf_HFO, t, df
    fileList = GUIpostTraitement.fileList
    RMS = []
    MAP = []
    FOM = []
    TRIAL = []
    TYPE = []
    SUBJ_NAME = []
    TRIAL_NUMBER = []
    SCENARIO = []
    SCORE = []
    ERR = []
    
    prec_name = '0'
    test_number = 0
    TEST_NUMBER = []
    
# Get parameters info from each file and recover the data
    for f in fileList:
        if f.find('~') != -1:# or f.find('trial_1') != -1:
            continue
        c = FileData(f)
        c.TIME_WINDOW_BEFORE = float(GUIpostTraitement.entryTimeWB.get())
        c.TIME_WINDOW_AFTER = float(GUIpostTraitement.entryTimeWA.get())
        c.forceLimit = float(GUIpostTraitement.entryForceLimit.get())
        c.dataKept = GUIpostTraitement.dataKeptVar.get()
        c.partAnalyzed = GUIpostTraitement.partAnalyzedVar.get()
        c.getDataFromFile()
        
        if (prec_name != c.SUBJECT_NAME1):
            test_number += 1
        prec_name = c.SUBJECT_NAME1
#        try:
#            c.Part_mark1.index("BODY_GAUCHE")
#            c.calculateRMSandMAP_markers()
#        except ValueError:
#            c.calculateRMSandMAP()
        if c.experienceType == 'INT':
            c.calculateRMSandMAP_markers()
            
            if c.fileType == 'HFO' or c.fileType == 'HFOP' or c.fileType == 'PPHARD' or c.fileType == 'PPSOFT' or c.fileType == 'NOISY' or c.fileType == 'DELAYED' or c.fileType == 'HFOP_mou':
                for k in range (0, 3):
                    RMS.append(np.mean(c.RMS_trial[k]))
                    MAP.append(np.mean(c.MAP_trial[k]))
                    FOM.append(np.mean(c.FOM_trial[k]))
                    TYPE.append(c.fileType)
                    TRIAL_NUMBER.append(c.fileTrialNb)
                    TEST_NUMBER.append(test_number)
                    SCORE.append(c.SCORE1)
                    ERR.append(c.ERR_trial[k][j])
                    SUBJ_NAME.append(c.SUBJECT_NAME1 + "+" + c.SUBJECT_NAME2)
                    if k == 0:
                        TRIAL.append('SAME')
                    elif k == 1:
                        TRIAL.append('ONE')
                    elif k == 2:
                        TRIAL.append('OPPO')
                        #    for k in range (0, 3):

#                    for j in range (0, len(c.RMS_trial[k])):
#                        RMS.append(c.RMS_trial[k][j])
#                        MAP.append(c.MAP_trial[k][j])
#                        FOM.append(c.FOM_trial[k][j])
#                        ERR.append(c.ERR_trial[k][j])
#                        TYPE.append(c.fileType)
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME1 + "+" + c.SUBJECT_NAME2)
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE1)
#                        if k == 0:
#                            TRIAL.append('SAME')
#                        elif k == 1:
#                            TRIAL.append('ONE')
#                        elif k == 2:
#                            TRIAL.append('OPPO')

    
                        
                            
            elif c.fileType == 'HVP' or c.fileType == 'KVP' or c.fileType == 'ALONE' or c.fileType == 'ROBOT': 
                for k in range (0, 3):
                    temp1 = []
                    temp2 = []
                    temp3 = []
                    RMS.append(np.mean(c.RMS_trial_1[k]))
                    MAP.append(np.mean(c.MAP_trial_1[k]))
                    FOM.append(np.mean(c.FOM_trial_1[k]))
                    TYPE.append(c.fileType) 
                    TRIAL_NUMBER.append(c.fileTrialNb)
                    TEST_NUMBER.append(test_number)
                    SUBJ_NAME.append(c.SUBJECT_NAME1) 
                    SCORE.append(c.SCORE1)
                    ERR.append(c.ERR_trial_1[k][j])
                    if k == 0:
                        TRIAL.append('SAME')
                    elif k == 1:
                        TRIAL.append('ONE')
                    elif k == 2:
                        TRIAL.append('OPPO')                   
    
                    RMS.append(np.mean(c.RMS_trial_2[k]))
                    MAP.append(np.mean(c.MAP_trial_2[k]))
                    FOM.append(np.mean(c.FOM_trial_2[k]))
                    TYPE.append(c.fileType)    
                    TRIAL_NUMBER.append(c.fileTrialNb)
                    TEST_NUMBER.append(test_number)
                    SUBJ_NAME.append(c.SUBJECT_NAME2) 
                    SCORE.append(c.SCORE2)
                    ERR.append(c.ERR_trial_2[k][j])                    
                    if k == 0:
                        TRIAL.append('SAME')
                    elif k == 1:
                        TRIAL.append('ONE')
                    elif k == 2:
                        TRIAL.append('OPPO')
                        
#                    for j in range (0, len(c.RMS_trial_1[k])):
#                        RMS.append(c.RMS_trial_1[k][j])
#                        temp1.append(c.MAP_trial_1[k][j])
#                        FOM.append(c.FOM_trial_1[k][j])
#                        TYPE.append(c.fileType) 
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME1)
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE1)
#                        ERR.append(c.ERR_trial_1[k][j])
#                        if k == 0:
#                            TRIAL.append('SAME')
#                        elif k == 1:
#                            TRIAL.append('ONE')
#                        elif k == 2:
#                            TRIAL.append('OPPO')                   
#                    for j in range (0, len(c.RMS_trial_2[k])):
#                        RMS.append(c.RMS_trial_2[k][j])
#                        temp2.append(c.MAP_trial_2[k][j])
#                        FOM.append(c.FOM_trial_2[k][j])
#                        TYPE.append(c.fileType)    
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME2)
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE2)
#                        ERR.append(c.ERR_trial_2[k][j])
#                        if k == 0:
#                            TRIAL.append('SAME')
#                        elif k == 1:
#                            TRIAL.append('ONE')
#                        elif k == 2:
#                            TRIAL.append('OPPO')
#                    temp3 = [temp1[i] + temp2[i] for i in range(0, len(temp1))]
#                    MAP.extend(temp3)
#                    MAP.extend(temp3)
                        
                        
        elif c.experienceType == 'TRAJ':
            c.calculateRMSandMAP_traj()
            
            if c.fileType == 'HFO' or c.fileType == 'HFOP' or c.fileType == 'PPHARD' or c.fileType == 'PPSOFT' or c.fileType == 'NOISY' or c.fileType == 'DELAYED' or c.fileType == 'HFOP_mou':
                RMS.append(np.mean([np.mean(x) for x in c.RMS_traj]))
                MAP.append(np.mean([np.mean(x) for x in c.MAP_traj]))
                FOM.append(np.mean([np.mean(x) for x in c.FOM_traj]))
                ERR.append(np.mean([np.mean(x) for x in c.ERR_traj]))
                TYPE.append(c.fileType)
                TRIAL_NUMBER.append(c.fileTrialNb)
                TEST_NUMBER.append(test_number)
                SUBJ_NAME.append(c.SUBJECT_NAME1 + "+" + c.SUBJECT_NAME2)   
                TRIAL.append('MEAN')
                SCENARIO.append(c.fileScenarioNb)
                SCORE.append(c.SCORE1)
                
#                for k in range (0, len(c.RMS_traj)):
#                    for j in range (0, len(c.RMS_traj[k])):
#                        RMS.append(c.RMS_traj[k][j])
#                        MAP.append(c.MAP_traj[k][j])
#                        FOM.append(c.FOM_traj[k][j])
#                        TYPE.append(c.fileType)
#                        ERR.append(c.ERR_traj[k][j])
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME1 + "+" + c.SUBJECT_NAME2)
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE1)
#                        if k == 0:
#                            TRIAL.append('RAMP')
#                        elif k == 1:
#                            TRIAL.append('SINUS')
#                        elif k == 2:
#                            TRIAL.append('JUMP')
#                        elif k == 3:
#                            TRIAL.append('STRAIGHT')
                        
                            
            elif c.fileType == 'HVP' or c.fileType == 'KVP' or c.fileType == 'ALONE' or c.fileType == 'ROBOT': 
                RMS.append(np.mean([np.mean(x) for x in c.RMS_traj1]))
                MAP.append(np.mean([np.mean(x) for x in c.MAP_traj1]))
                FOM.append(np.mean([np.mean(x) for x in c.FOM_traj1]))
                ERR.append(np.mean([np.mean(x) for x in c.ERR_traj1]))
                TYPE.append(c.fileType) 
                TRIAL_NUMBER.append(c.fileTrialNb)
                TEST_NUMBER.append(test_number)
                SUBJ_NAME.append(c.SUBJECT_NAME1)   
                TRIAL.append('MEAN')
                SCENARIO.append(c.fileScenarioNb)
                SCORE.append(c.SCORE1)

                RMS.append(np.mean([np.mean(x) for x in c.RMS_traj2]))
                MAP.append(np.mean([np.mean(x) for x in c.MAP_traj2]))
                FOM.append(np.mean([np.mean(x) for x in c.FOM_traj2]))
                ERR.append(np.mean([np.mean(x) for x in c.FOM_traj2]))
                TYPE.append(c.fileType)    
                TRIAL_NUMBER.append(c.fileTrialNb)
                TEST_NUMBEforR.append(test_number)
                SUBJ_NAME.append(c.SUBJECT_NAME2)
                TRIAL.append(0)    
                SCENARIO.append(c.fileScenarioNb)
                SCORE.append(c.SCORE2)
            
#                for k in range (0, len(c.RMS_traj)):
#                    for j in range (0, len(c.RMS_traj1[k])):
#                        RMS.append(c.RMS_traj1[k][j])
#                        MAP.append(c.MAP_traj1[k][j])
#                        FOM.append(c.FOM_traj1[k][j])
#                        ERR.append(c.ERR_traj1[k][j])
#                        TYPE.append(c.fileType) 
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME1) 
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE1)
#                        if k == 0:
#                            TRIAL.append('RAMP')
#                        elif k == 1:
#                            TRIAforL.append('SINUS')
#                        elif k == 2:
#                            TRIAL.append('JUMP')
#                        elif k == 3:
#                            TRIAL.append('STRAIGHT')                  
#                    for j in range (0, len(c.RMS_traj2[k])):
#                        RMS.append(c.RMS_traj2[k][j])
#                        MAP.append(c.MAP_traj2[k][j])
#                        FOM.append(c.FOM_traj2[k][j])
#                        ERR.append(c.ERR_traj2[k][j])
#                        TYPE.append(c.fileType)    
#                        TRIAL_NUMBER.append(c.fileTrialNb)
#                        TEST_NUMBER.append(test_number)
#                        SUBJ_NAME.append(c.SUBJECT_NAME2)      
#                        SCENARIO.append(c.fileScenarioNb)
#                        SCORE.append(c.SCORE2)
#                        if k == 0:
#                            TRIAL.append('RAMP')
#                        elif k == 1:
#                            TRIAL.append('SINUS')
#                        elif k == 2:
#                            TRIAL.append('JUMP')
#                        elif k == 3:
#                            TRIAL.append('STRAIGHT')
          
                    
        print f, " analyzed ... "
        
        
    data = pandas.DataFrame({'RMS' : RMS, 'MAP' : MAP, 'FOM' : FOM, 'TRIAL': TRIAL, 'TYPE': TYPE, 'TRIAL_NUMBER' : TRIAL_NUMBER, 'TEST_NUMBER' : TEST_NUMBER, 'SUBJ_NAME' : SUBJ_NAME, 'SCENARIO' : SCENARIO, 'SCORE' : SCORE, 'ERR' : ERR}) 

    print data
    
    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)    
    data.to_csv('/home/lucas/phri/lucas/fichiers_csv/data_' + date + '.csv')
    
    for t in set(data['TYPE']):
        print data[data['TYPE'] == 'HFOP']['RMS']
 
 
 
###############################################################################################################
def customMax(n):
    if not n:
        return 0
    else:
        return max(n)
        
def customMean(n):
    if not n:
        return 0
    else:
        return sum(n)/len(n)


      
if __name__ == '__main__':
    main()
