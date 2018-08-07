#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:54:44 2015

@author: roche
"""

from scipy import stats
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *

from postTrait_Module import *



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
        self.textZone = Text(self.frameTOPLEFT, height = self.heightTextZone, width = 100)
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
        self.entryForceLimit.insert(0, '1.5')
        
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

        self.buttonProcess = Button(self.frameTOPRIGHT, text = 'Process Files', command = self.process, width = 18)
        self.buttonProcess.grid(row = 1, column = 0, pady = 5)
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
            self.textZone.config(height=self.heightTextZone)
        if filesToAdd:
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
    RMS_all_HFOP = [[],[],[]]  #SAME, ONE, OPPO
    RMS_all_HFO  = [[],[],[]]  #SAME, ONE, OPPO
    RMS_all_ULTRON_1 = [[],[],[]]
    RMS_all_ULTRON_2 = [[],[],[]]
    RMS_all_ALONE_1 = [[],[],[]]
    RMS_all_ALONE_2 = [[],[],[]]      
    
# Get parameters info from each file and recover the data
    for f in fileList:
        if f.find('_mou') != -1:
            continue
        c = FileData(f)
        c.TIME_WINDOW_BEFORE = float(GUIpostTraitement.entryTimeWB.get())
        c.TIME_WINDOW_AFTER = float(GUIpostTraitement.entryTimeWA.get())
        c.forceLimit = float(GUIpostTraitement.entryForceLimit.get())
        c.dataKept = GUIpostTraitement.dataKeptVar.get()
        c.partAnalyzed = GUIpostTraitement.partAnalyzedVar.get()
        c.getDataFromFile()
#        try:
#            c.Part_mark1.index("BODY_GAUCHE")
#            c.calculateRMSandMAP_markers()
#        except ValueError:
#            c.calculateRMSandMAP()
        c.calculateRMSandMAP_markers()
#        print c.RMS_trial_withpoints, c.RMS_trial_withpoints_1, c.RMS_trial_withpoints_2   
        if c.fileType == 'HFOP':
            for k in range (0, len(RMS_all_HFOP)):
                RMS_all_HFOP[k].extend(c.RMS_trial[k])
        elif c.fileType == 'HFO':
            for k in range (0, len(RMS_all_HFO)):
                RMS_all_HFO[k].extend(c.RMS_trial[k])
        elif c.fileType == 'ULTRON' :#or c.fileType == 'ROBOT':
            for k in range (0, len(RMS_all_HFOP)):
                RMS_all_ULTRON_1[k].extend(c.RMS_trial_1[k])
                RMS_all_ULTRON_2[k].extend(c.RMS_trial_2[k])
        elif c.fileType == 'ALONE':
            for k in range (0, len(RMS_all_HFO)):
                RMS_all_ALONE_1[k].extend(c.RMS_trial_1[k])
                RMS_all_ALONE_2[k].extend(c.RMS_trial_2[k])
        print f, " analyzed ... "
        
                
## Calculate performances
#    RMS_mean = (customMean(RMS_all_HFOP[0]) + customMean(RMS_all_HFOP[1]) + customMean(RMS_all_HFOP[2]) + customMean(RMS_all_HFO[0]) + customMean(RMS_all_HFO[1]) + customMean(RMS_all_HFO[2]) + customMean(RMS_all_ULTRON_1[0]) + customMean(RMS_all_ULTRON_1[1]) + customMean(RMS_all_ULTRON_1[2]) + customMean(RMS_all_ULTRON_2[0]) + customMean(RMS_all_ULTRON_2[1]) + customMean(RMS_all_ULTRON_2[2]) + customMean(RMS_all_ALONE_1[0]) + customMean(RMS_all_ALONE_1[1]) + customMean(RMS_all_ALONE_1[2]) + customMean(RMS_all_ALONE_2[0]) + customMean(RMS_all_ALONE_2[1]) + customMean(RMS_all_ALONE_2[2]))/16

    RMS_max_HFOP = max(customMax(RMS_all_HFOP[0]), customMax(RMS_all_HFOP[1]), customMax(RMS_all_HFOP[2]))
    RMS_max_HFO  = max(customMax(RMS_all_HFO[0]), customMax(RMS_all_HFO[1]), customMax(RMS_all_HFO[2]))   
#    RMS_max = max(RMS_max_HFO, RMS_max_HFOP)
#    
#    perf_HFOP = []
#    perf_HFO = []
#    perf_moy_HFOP = 0
#    perf_moy_HFO = 0
#    
#    (perf_HFOP, perf_moy_HFOP) = calculatePerformance(RMS_all_HFOP, RMS_max)
#    (perf_HFO, perf_moy_HFO) = calculatePerformance(RMS_all_HFO, RMS_max)
    


# Calculate performances
    RMS_max_ULTRON_1 = max(customMax(RMS_all_ULTRON_1[0]), customMax(RMS_all_ULTRON_1[1]), customMax(RMS_all_ULTRON_1[2]))
    RMS_max_ULTRON_2 = max(customMax(RMS_all_ULTRON_2[0]), customMax(RMS_all_ULTRON_2[1]), customMax(RMS_all_ULTRON_2[2]))
    RMS_max_ALONE_1 = max(customMax(RMS_all_ALONE_1[0]), customMax(RMS_all_ALONE_1[1]), customMax(RMS_all_ALONE_1[2]))
    RMS_max_ALONE_2 = max(customMax(RMS_all_ALONE_2[0]), customMax(RMS_all_ALONE_2[1]), customMax(RMS_all_ALONE_2[2]))
    
    RMS_max = max(RMS_max_HFO, RMS_max_HFOP, RMS_max_ULTRON_1, RMS_max_ULTRON_2,RMS_max_ALONE_1, RMS_max_ALONE_2)  
    
    RMS_max = 100    
    
    perf_HFOP = []
    perf_HFO = []
    perf_ULTRON_1 = []
    perf_ULTRON_2 = []
    perf_ALONE_1 = []
    perf_ALONE_2 = []
    perf_moy_HFOP = 0
    perf_moy_HFO = 0
    perf_moy_ULTRON_1 = 0
    perf_moy_ULTRON_2 = 0
    perf_moy_ALONE_1 = 0
    perf_moy_ALONE_2 = 0
    
    (perf_HFOP, perf_moy_HFOP) = calculatePerformance(RMS_all_HFOP, RMS_max)
    (perf_HFO, perf_moy_HFO) = calculatePerformance(RMS_all_HFO, RMS_max)
    (perf_ULTRON_1, perf_moy_ULTRON_1) = calculatePerformance(RMS_all_ULTRON_1, RMS_max)
    (perf_ULTRON_2, perf_moy_ULTRON_2) = calculatePerformance(RMS_all_ULTRON_2, RMS_max)
    (perf_ALONE_1, perf_moy_ALONE_1) = calculatePerformance(RMS_all_ALONE_1, RMS_max)
    (perf_ALONE_2, perf_moy_ALONE_2) = calculatePerformance(RMS_all_ALONE_2, RMS_max)
    


    if GUIpostTraitement.partAnalyzedVar.get() == 'CHOICES':
        n = 3
    elif GUIpostTraitement.partAnalyzedVar.get() == 'BODY':
        n = 1

    perf_ULTRON = [0,0,0]
    perf_moy_ULTRON = [0,0,0]
    perf_ALONE = [0,0,0]
    perf_moy_ALONE = [0,0,0]
    for k in range (0,n):
        try:
            perf_ULTRON[k] = perf_ULTRON_1[k] + perf_ULTRON_2[k]
            perf_moy_ULTRON[k] = (perf_moy_ULTRON_1[k] + perf_moy_ULTRON_2[k])/2
        except:
            perf_ULTRON = [0,0,0]
        try:        
            perf_ALONE[k] = perf_ALONE_1[k] + perf_ALONE_2[k]
            perf_moy_ALONE[k] = (perf_moy_ALONE_1[k] + perf_moy_ALONE_2[k])/2
        except:
            perf_ALONE = [0,0,0]


#    print perf_HFOP
#    print RMS_all_HFOP
#    print '\n'
#    print perf_ULTRON_1
#    print RMS_all_ULTRON_1
#    print '\n'
#    print perf_ULTRON_2
#    print RMS_all_ULTRON_2
#    print '\n'
#    print perf_ALONE_1
#    print RMS_all_ALONE_1
#    print '\n'
#    print perf_ALONE_2
#    print RMS_all_ALONE_2
    
    GUIpostTraitement.resultsHFOP = perf_moy_HFOP
    GUIpostTraitement.resultsHFO = perf_moy_HFO     
    GUIpostTraitement.resultsLabelHFOP.set(str(perf_moy_HFOP))
    GUIpostTraitement.resultsLabelHFO.set(str(perf_moy_HFO))

# T-test for comparison between HFO and HFOP
    N_HFOP = [0,0,0]
    N_HFO  = [0,0,0]
    N_ULTRON = [0,0,0]
    N_ALONE = [0,0,0]
    var_HFOP = [0,0,0]
    var_HFO  = [0,0,0]
    var_ULTRON = [0,0,0]
    var_ALONE = [0,0,0]
    SX1X2 = 0.0
    
    t_HFOP_INTER = [0,0,0]
    df_HFOP_INTER = [0,0,0]
    t_HFO_INTER = [0,0,0]
    df_HFO_INTER = [0,0,0]
    t_ALONE_INTER = [0,0,0]
    df_ALONE_INTER = [0,0,0]
    t_ULTRON_INTER = [0,0,0]
    df_ULTRON_INTER = [0,0,0]
    
    t_HFO_HFOP = [0,0,0]
    df_HFO_HFOP = [0,0,0]
    t_ALONE_HFOP = [0,0,0]
    df_ALONE_HFOP = [0,0,0]
    t_HFOP_ULTRON = [0,0,0]
    df_HFOP_ULTRON = [0,0,0]
    t_ALONE_ULTRON = [0,0,0]
    df_ALONE_ULTRON = [0,0,0]
    for k in range (0,n):
        if isinstance(perf_HFOP[k], list):
            N_HFOP[k] = len(perf_HFOP[k])
        else:
            N_HFOP[k] = 0
        if isinstance(perf_HFO[k], list):
            N_HFO[k]  = len(perf_HFO[k])
        else:
            N_HFO[k] = 0
        if isinstance(perf_ULTRON[k], list):
            N_ULTRON[k] = len(perf_ULTRON[k])
        else:
            N_ULTRON[k] = 0
        if isinstance(perf_ALONE[k], list):        
            N_ALONE[k] = len(perf_ALONE[k])
        else:
            N_ALONE[k] = 0
            
    cond_HFOP = 1
    cond_HFO = 1
    cond_ULTRON = 1
    cond_ALONE = 1
    for k in range (0,n):
        cond_HFOP &= (N_HFOP[k] != 0)
        cond_HFO  &= (N_HFO[k] != 0)
        cond_ULTRON  &= (N_ULTRON[k] != 0)
        cond_ALONE  &= (N_ALONE[k] != 0)
    
        
    if cond_HFOP:
        for k in range (0,n):
            for i in range (0, len(perf_HFOP[k])):
                var_HFOP[k] += ((perf_HFOP[k][i]-perf_moy_HFOP[k])**2)
            var_HFOP[k] /= N_HFOP[k]
        
        if GUIpostTraitement.partAnalyzedVar.get() == 'CHOICES':   
            #SAME vs ONE
            SX1X2 = sqrt(var_HFOP[0]/N_HFOP[0] + var_HFOP[1]/N_HFOP[1])           
            t_HFOP_INTER[0] = (perf_moy_HFOP[0] - perf_moy_HFOP[1])/SX1X2
            df_HFOP_INTER[0] = N_HFOP[0] + N_HFOP[1] - 2
            #SAME vs OPPO
            SX1X2 = sqrt(var_HFOP[0]/N_HFOP[0] + var_HFOP[2]/N_HFOP[2])           
            t_HFOP_INTER[1] = (perf_moy_HFOP[0] - perf_moy_HFOP[2])/SX1X2
            df_HFOP_INTER[1] = N_HFOP[0] + N_HFOP[2] - 2
            #ONE vs OPPO
            SX1X2 = sqrt(var_HFOP[1]/N_HFOP[1] + var_HFOP[2]/N_HFOP[2])           
            t_HFOP_INTER[2] = (perf_moy_HFOP[1] - perf_moy_HFOP[2])/SX1X2
            df_HFOP_INTER[2] = N_HFOP[1] + N_HFOP[2] - 2
        

    if cond_HFO:        
        for k in range (0,n):
            for i in range (0, len(perf_HFO[k])):
                var_HFO[k] += ((perf_HFO[k][i]-perf_moy_HFO[k])**2)
            var_HFO[k] /= N_HFO[k]

        if GUIpostTraitement.partAnalyzedVar.get() == 'CHOICES':
            #SAME vs ONE
            SX1X2 = sqrt(var_HFO[0]/N_HFO[0] + var_HFO[1]/N_HFO[1])           
            t_HFO_INTER[0] = (perf_moy_HFO[0] - perf_moy_HFO[1])/SX1X2
            df_HFO_INTER[0] = N_HFO[0] + N_HFO[1] - 2
            #SAME vs OPPO
            SX1X2 = sqrt(var_HFO[0]/N_HFO[0] + var_HFO[2]/N_HFO[2])           
            t_HFO_INTER[1] = (perf_moy_HFO[0] - perf_moy_HFO[2])/SX1X2
            df_HFO_INTER[1] = N_HFO[0] + N_HFO[2] - 2
            #ONE vs OPPO
            SX1X2 = sqrt(var_HFO[1]/N_HFO[1] + var_HFO[2]/N_HFO[2])           
            t_HFO_INTER[2] = (perf_moy_HFO[1] - perf_moy_HFO[2])/SX1X2
            df_HFO_INTER[2] = N_HFO[1] + N_HFO[2] - 2
            
            
    if cond_ULTRON:
        for k in range (0,n):
            for i in range (0, len(perf_ULTRON[k])):
                var_ULTRON[k] += ((perf_ULTRON[k][i]-perf_moy_ULTRON[k])**2)
            var_ULTRON[k] /= N_ULTRON[k]

        if GUIpostTraitement.partAnalyzedVar.get() == 'CHOICES':            
            #SAME vs ONE
            SX1X2 = sqrt(var_ULTRON[0]/N_ULTRON[0] + var_ULTRON[1]/N_ULTRON[1])           
            t_ULTRON_INTER[0] = (perf_moy_ULTRON[0] - perf_moy_ULTRON[1])/SX1X2
            df_ULTRON_INTER[0] = N_ULTRON[0] + N_ULTRON[1] - 2
            #SAME vs OPPO
            SX1X2 = sqrt(var_ULTRON[0]/N_ULTRON[0] + var_ULTRON[2]/N_ULTRON[2])           
            t_ULTRON_INTER[1] = (perf_moy_ULTRON[0] - perf_moy_ULTRON[2])/SX1X2
            df_ULTRON_INTER[1] = N_ULTRON[0] + N_ULTRON[2] - 2
            #ONE vs OPPO
            SX1X2 = sqrt(var_ULTRON[1]/N_ULTRON[1] + var_ULTRON[2]/N_ULTRON[2])           
            t_ULTRON_INTER[2] = (perf_moy_ULTRON[1] - perf_moy_ULTRON[2])/SX1X2
            df_ULTRON_INTER[2] = N_ULTRON[1] + N_ULTRON[2] - 2
            
            
    if cond_ALONE:
        for k in range (0,n):
            for i in range (0, len(perf_ALONE[k])):
                var_ALONE[k] += ((perf_ALONE[k][i]-perf_moy_ALONE[k])**2)
            var_ALONE[k] /= N_ALONE[k]

        if GUIpostTraitement.partAnalyzedVar.get() == 'CHOICES':            
            #SAME vs ONE
            SX1X2 = sqrt(var_ALONE[0]/N_ALONE[0] + var_ALONE[1]/N_ALONE[1])           
            t_ALONE_INTER[0] = (perf_moy_ALONE[0] - perf_moy_ALONE[1])/SX1X2
            df_ALONE_INTER[0] = N_ALONE[0] + N_ALONE[1] - 2
            #SAME vs OPPO
            SX1X2 = sqrt(var_ALONE[0]/N_ALONE[0] + var_ALONE[2]/N_ALONE[2])           
            t_ALONE_INTER[1] = (perf_moy_ALONE[0] - perf_moy_ALONE[2])/SX1X2
            df_ALONE_INTER[1] = N_ALONE[0] + N_ALONE[2] - 2
            #ONE vs OPPO
            SX1X2 = sqrt(var_ALONE[1]/N_ALONE[1] + var_ALONE[2]/N_ALONE[2])           
            t_ALONE_INTER[2] = (perf_moy_ALONE[1] - perf_moy_ALONE[2])/SX1X2
            df_ALONE_INTER[2] = N_ALONE[1] + N_ALONE[2] - 2
            

    if cond_HFO and cond_HFOP:       
        for k in range (0,n):
            SX1X2 = sqrt(var_HFOP[k]/N_HFOP[k] + var_HFO[k]/N_HFO[k])            
            t_HFO_HFOP[k] = (perf_moy_HFOP[k] - perf_moy_HFO[k])/SX1X2
            df_HFO_HFOP[k] = N_HFOP[k] + N_HFO[k] - 2

    if cond_ALONE and cond_HFOP:     
        for k in range (0,n):
            SX1X2 = sqrt(var_HFOP[k]/N_HFOP[k] + var_ALONE[k]/N_ALONE[k])           
            t_ALONE_HFOP[k] = (perf_moy_HFOP[k] - perf_moy_ALONE[k])/SX1X2
            df_ALONE_HFOP[k] = N_HFOP[k] + N_ALONE[k] - 2
            
    if cond_HFOP and cond_ULTRON:       
        for k in range (0,n):
            SX1X2 = sqrt(var_ULTRON[k]/N_ULTRON[k] + var_HFOP[k]/N_HFOP[k])            
            t_HFOP_ULTRON[k] = (perf_moy_ULTRON[k] - perf_moy_HFOP[k])/SX1X2
            df_HFOP_ULTRON[k] = N_ULTRON[k] + N_HFOP[k] - 2
            
    if cond_ALONE and cond_ULTRON:      
        for k in range (0,n):
            SX1X2 = sqrt(var_ULTRON[k]/N_ULTRON[k] + var_ALONE[k]/N_ALONE[k])        
            t_ALONE_ULTRON[k] = (perf_moy_ULTRON[k] - perf_moy_ALONE[k])/SX1X2
            df_ALONE_ULTRON[k] = N_ULTRON[k] + N_ALONE[k] - 2            

           
    print "Perf HFOP : ", perf_moy_HFOP
    print "Stdev HFOP : ", sqrt(var_HFOP[0]), sqrt(var_HFOP[1]), sqrt(var_HFOP[2])
    print "Perf HFO : ", perf_moy_HFO
    print "Stdev HFO : ", sqrt(var_HFO[0]), sqrt(var_HFO[1]), sqrt(var_HFO[2])
    print "Perf ULTRON : ", perf_moy_ULTRON
    print "Stdev ULTRON : ", sqrt(var_ULTRON[0]), sqrt(var_ULTRON[1]), sqrt(var_ULTRON[2])
    print "Perf ALONE : ", perf_moy_ALONE
    print "Stdev ALONE : ", sqrt(var_ALONE[0]), sqrt(var_ALONE[1]), sqrt(var_ALONE[2])
    print "\n"
    print "HFO-HFOP, ALONE-HFOP, HFOP-ULTRON, ALONE-ULTRON "        
    print t_HFO_HFOP, t_ALONE_HFOP, t_HFOP_ULTRON, t_ALONE_ULTRON
    print df_HFO_HFOP, df_ALONE_HFOP, df_HFOP_ULTRON, df_ALONE_ULTRON
    print "\n"
    print "\tSAME vs ONE, SAME vs OPPO, ONE vs OPPO"
    print "HFOP:\t", t_HFOP_INTER
    print "\t", df_HFOP_INTER
    print "HFO:\t", t_HFO_INTER
    print "\t", df_HFO_INTER
    print "ULTRON:\t", t_ULTRON_INTER
    print "\t", df_ULTRON_INTER
    print "ALONE:\t", t_ALONE_INTER
    print "\t", df_ALONE_INTER    


#    if GUIpostTraitement.saveVar.get() == 1:
#        date = time.gmtime(None)
#        date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
#        directory_name = "../post-traitement/POST_TRAITEMENT_" + date
#        if not os.path.exists(directory_name):
#            os.makedirs(directory_name)     
#        for i in range (0, NbSubjects):
#            writeToFileSubject(directory_name, fileListSorted[i], RMS_subject_HFOP[i], RMS_subject_HFO[i], perf_subject_HFOP[i], perf_subject_HFO[i], perf_moy_subject_HFOP[i], perf_moy_subject_HFO[i])



    GUIpostTraitement.buttonExport.config(state=NORMAL)
    
    
    #print c[fileListSorted[2][0]].SUBJECT_NAME1
    
#    for f in fileList:
#        del c[f]

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

#############################################################################################################
def calculatePerformance(RMS_error, RMS_max):
    
    Perf = [[0]*len(RMS_error[0]), [0]*len(RMS_error[1]),[0]*len(RMS_error[2])]
    
    for i in range (0,3):
        for j in range (0,len(RMS_error[i])):
            Perf[i][j] = 1 - RMS_error[i][j]/RMS_max

 
    Perf_moy = [None]*3
#    Stdev = [0]*3
#    Stderr = [0]*3
    for k in range (0, len(Perf_moy)):
        try:
            Perf_moy[k] =  sum(Perf[k])/len(Perf[k]) #numpy.mean(Perf[k], dtype=np.float64 )
        except:
            Perf_moy[k] = '.'
#        Stdev[i] = numpy.std(Perf[i])
#        Stderr[i] = stats.sem(Perf[i])
    
    return(Perf, Perf_moy)


#######################################################################################################
def writeToFile(file_name):
    global GUIpostTraitement, RMS_all_HFOP, RMS_all_HFO, perf_HFOP, perf_HFO, t, df
  
    f = file_name
    
    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    f.write("\n")
#    f.write("Sujets : " + str(SUBJECT_NAME1) + " + " + str(SUBJECT_NAME2) + "\n")
    f.write("\n")
    f.write("Donnees obetnues a partir des fichiers : \n")
    for x in GUIpostTraitement.fileList:
        f.write(x + "\n")
    f.write("\n")
    
    f.write("Fenetre de temps avant fork : " + str(GUIpostTraitement.entryTimeWB.get()) + " s\n")
    f.write("Fenetre de temps apres fork : " + str(GUIpostTraitement.entryTimeWA.get()) + " s\n")
    f.write("Filtre force: donnees gardees = " + GUIpostTraitement.dataKeptVar.get() + " " +  str(GUIpostTraitement.entryForceLimit.get()) + " N")
    f.write("\n")   
    f.write("\n")
    f.write("Mean Performance HFOP: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    f.write(str(GUIpostTraitement.resultsHFOP[0]) + "\t\t" + str(GUIpostTraitement.resultsHFOP[1]) + "\t\t" +str(GUIpostTraitement.resultsHFOP[2]) + "\n")    
    f.write("\n")
    f.write("Mean Performance HFO: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    f.write(str(GUIpostTraitement.resultsHFO[0]) + "\t\t" + str(GUIpostTraitement.resultsHFO[1]) + "\t\t" +str(GUIpostTraitement.resultsHFO[2]) + "\n")
    f.write("\n")
    f.write("\n")
    f.write("df\n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    f.write(str(df[0]) + '\t\t' + str(df[1])  + '\t\t' + str(df[2]))    
    f.write("\n")
    f.write("\n")
    f.write("t value\n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    f.write(str(t[0]) + '\t\t' + str(t[1])  + '\t\t' + str(t[2]))    
    
    
    f.write('\n')
    f.write('\n')
    f.write('Perf HFOP :\n')
    for j in range (0, max(len(perf_HFOP[0]), len(perf_HFOP[1]), len(perf_HFOP[2]))):
        try:
            f.write(str(perf_HFOP[0][j]) + "\t\t")
        except:
            f.write("\t\t")
        try:
            f.write(str(perf_HFOP[1][j]) + "\t\t")
        except:
            f.write("\t\t")        
        try:
            f.write(str(perf_HFOP[2][j]) + "\t\t")
        except:
            f.write("\t\t")
        f.write("\n")
        
    f.write('\n')
    f.write('Perf HFO :\n')
    for j in range (0, max(len(perf_HFO[0]), len(perf_HFO[1]), len(perf_HFO[2]))):
        try:
            f.write(str(perf_HFO[0][j]) + "\t\t")
        except:
            f.write("\t\t")
        try:
            f.write(str(perf_HFO[1][j]) + "\t\t")
        except:
            f.write("\t\t")        
        try:
            f.write(str(perf_HFO[2][j]) + "\t\t")
        except:
            f.write("\t\t")
        f.write("\n")
        

    f.write('\n')
    f.write('RMS HFOP :\n')
    for j in range (0, max(len(RMS_all_HFOP[0]), len(RMS_all_HFOP[1]), len(RMS_all_HFOP[2]))):
        try:
            f.write(str(RMS_all_HFOP[0][j]) + "\t\t")
        except:
            f.write("\t\t")
        try:
            f.write(str(RMS_all_HFOP[1][j]) + "\t\t")
        except:
            f.write("\t\t")        
        try:
            f.write(str(RMS_all_HFOP[2][j]) + "\t\t")
        except:
            f.write("\t\t")
        f.write("\n")

    f.write('\n')
    f.write('RMS HFO :\n')
    for j in range (0, max(len(RMS_all_HFO[0]), len(RMS_all_HFO[1]), len(RMS_all_HFO[2]))):
        try:
            f.write(str(RMS_all_HFO[0][j]) + "\t\t")
        except:
            f.write("\t\t")
        try:
            f.write(str(RMS_all_HFO[1][j]) + "\t\t")
        except:
            f.write("\t\t")        
        try:
            f.write(str(RMS_all_HFO[2][j]) + "\t\t")
        except:
            f.write("\t\t")
        f.write("\n")

 
           
    f.close()
    
    GUIpostTraitement.messageLabel.set('File Saved.')
    

#def writeToFileSubject(directory_name, fileListOneSubject, RMS_HFOP_OneSubject, RMS_HFO_OneSubject, Perf_HFOP_OneSubject, Perf_HFO_OneSubject, Perf_moy_HFOP_OneSubject, Perf_moy_HFO_OneSubject):
#    global c
#    date = time.gmtime(None)
#    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
#    subjectName1 = c[fileListOneSubject[0]].SUBJECT_NAME1
#    subjectName2 = c[fileListOneSubject[0]].SUBJECT_NAME2
#    file_name = directory_name + "/POST-TRAITEMENT_" + subjectName1 + "+" + subjectName2 + "-" + date
#    
#    f = open(file_name , 'w')
#    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
#    f.write("\n")
#    f.write("Sujets : " + subjectName1 + "+" + subjectName2 + "\n")
#    f.write("\n")
#    f.write("Donnees obetnues a partir des fichiers : \n")
#    for fi in fileListOneSubject:
#        f.write(fi + "\n")
#    f.write("\n")
#        
#    f.write("Fenetre de temps avant fork : " + str(GUIpostTraitement.entryTimeWB.get()) + " s\n")
#    f.write("Fenetre de temps apres fork : " + str(GUIpostTraitement.entryTimeWA.get()) + " s\n")
#    f.write("Filtre force: donnees gardees = " + GUIpostTraitement.dataKeptVar.get() + " " +  str(GUIpostTraitement.entryForceLimit.get()) + " N")
#    f.write("\n")
#    f.write("\n")
#    f.write("Perf Moyenne HFOP: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for k in range (0,3):
#        f.write(str(Perf_moy_HFOP_OneSubject[k]) + "\t\t")
#    f.write("\n")
#    f.write("\n")
#    f.write("Perf Moyenne HFO: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for k in range (0,3):
#        f.write(str(Perf_moy_HFO_OneSubject[k]) + "\t\t")
#    f.write("\n")
#    f.write("\n")
#    f.write("\n")
#   
#    f.write("RMS HFOP: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for i in range (0, max(len(RMS_HFOP_OneSubject[0]), len(RMS_HFOP_OneSubject[1]), len(RMS_HFOP_OneSubject[2]))):
#        try:
#            f.write(str(RMS_HFOP_OneSubject[0][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        try:
#            f.write(str(RMS_HFOP_OneSubject[1][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")        
#        try:
#            f.write(str(RMS_HFOP_OneSubject[2][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        f.write("\n")
#    f.write("\n")
#    f.write("\n")
#
#    f.write("RMS HFO: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for i in range (0, max(len(RMS_HFO_OneSubject[0]), len(RMS_HFO_OneSubject[1]), len(RMS_HFO_OneSubject[2]))):
#        try:
#            f.write(str(RMS_HFO_OneSubject[0][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        try:
#            f.write(str(RMS_HFO_OneSubject[1][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")        
#        try:
#            f.write(str(RMS_HFO_OneSubject[2][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        f.write("\n")
#    f.write("\n")
#    f.write("\n")    
#    
#    f.write("Perf HFOP: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for i in range (0, max(len(Perf_HFOP_OneSubject[0]), len(Perf_HFOP_OneSubject[1]), len(Perf_HFOP_OneSubject[2]))):
#        try:
#            f.write(str(Perf_HFOP_OneSubject[0][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        try:
#            f.write(str(Perf_HFOP_OneSubject[1][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")        
#        try:
#            f.write(str(Perf_HFOP_OneSubject[2][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        f.write("\n")
#    f.write("\n")
#    f.write("\n")
#    
#    f.write("Perf HFO: \n")
#    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
#    for i in range (0, max(len(Perf_HFO_OneSubject[0]), len(Perf_HFO_OneSubject[1]), len(Perf_HFO_OneSubject[2]))):
#        try:
#            f.write(str(Perf_HFO_OneSubject[0][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        try:
#            f.write(str(Perf_HFO_OneSubject[1][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")        
#        try:
#            f.write(str(Perf_HFO_OneSubject[2][i]) + "\t\t")
#        except:
#            f.write(".\t\t\t")
#        f.write("\n")
#    f.write("\n")
#    f.write("\n")  
#
#    f.close()
#


      
if __name__ == '__main__':
    main()
