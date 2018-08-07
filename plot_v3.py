#!/usr/bin/env python

#Code written by Lucas Roche
#April 2015

import sys
import random
import numpy
import os
import time
import matplotlib.pyplot as plt
import scipy.signal as sig

#from Params import *
from math import *
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *

##################################################################################################### 
class GUIplot:

    def __init__(self, master):
        self.master = master
        
        self.frameTOP = Frame(master)
        self.frameTOP.grid(row=0, column=0, columnspan = 2)
       
        self.frameBOT = Frame(master)
        self.frameBOT.grid(row=1, column=0, columnspan = 2)
        
        self.frameLEFT = Frame(master)
        self.frameLEFT.grid(row=2, column=0, padx= 5)
        
        self.frameRIGHT = Frame(master)
        self.frameRIGHT.grid(row=2, column=1, padx= 5)
        
        self.frameBOTBOT = Frame(master)
        self.frameBOTBOT.grid(row=3, column=0, columnspan = 2)
        
        self.file_name = ''
        
        self.checkVar = IntVar()
        self.checkVarPartBody = IntVar()
        self.checkVarPartChoice = IntVar()
        self.checkVarFilter = IntVar()       
        self.checkVarPath1 = IntVar()      
        self.checkVarPath2 = IntVar()
        self.checkVarCurs = IntVar()
        self.checkVarPos1 = IntVar()
        self.checkVarPos2 = IntVar()
        self.checkVarFor1 = IntVar()
        self.checkVarFor2 = IntVar()
        self.checkVarRobPos1 = IntVar()
        self.checkVarRobPos2 = IntVar()
        self.checkVarCurs1 = IntVar()
        self.checkVarCurs2 = IntVar()
        self.checkVarNorm = IntVar()
        
        self.fig = plt.Figure()


       
        self.checkBoxFilter = Checkbutton(self.frameTOP, variable = self.checkVarFilter)
        self.checkBoxFilter.grid(row=0, column=0)
        self.checkBoxFilter.select()
        self.labelFilter1   = Label(self.frameTOP, text = 'Filter (Order =').grid(row=0, column=1)
        self.filterEntry    = Entry(self.frameTOP, width = 4)
        self.filterEntry.grid(row=0, column=2)
        self.filterEntry.insert(0, '3')
        self.labelFilter2   = Label(self.frameTOP, text = ')').grid(row=0, column=3)
        
        self.loadButton = Button(self.frameTOP, text = "LOAD DATA", command = loadDataFromFile, state= DISABLED)
        self.loadButton.grid(row=0, column=4)
        
        self.plotButton = Button(self.frameTOP, text = "PLOT", command = plot, state= DISABLED)
        self.plotButton.grid(row=0, column=5)
        
        self.plotChoicesButton = Button(self.frameTOP, text = "PLOT CHOICES", command = plotChoices, state = DISABLED)
        self.plotChoicesButton.grid(row=0, column=6)
        
        self.checkBoxPartBody = Checkbutton(self.frameTOP, variable = self.checkVarPartBody)
        self.checkBoxPartBody.grid(row = 0, column = 7)
        self.checkBoxPartBody.select()
        self.labelPartBody = Label(self.frameTOP, text = 'Body').grid(row = 0 , column = 8)
        self.checkBoxPartChoice = Checkbutton(self.frameTOP, variable = self.checkVarPartChoice)
        self.checkBoxPartChoice.grid(row = 0, column = 9)
        self.checkBoxPartChoice.select()
        self.labelPartChoice = Label(self.frameTOP, text = 'Choice').grid(row = 0, column = 10)
        self.checkBoxNorm = Checkbutton(self.frameTOP, variable = self.checkVarNorm)
        self.checkBoxNorm.grid(row=0, column=11)
        self.checkBoxNorm.select()
        self.labelNorm = Label(self.frameTOP, text = 'Normalisation').grid(row=0,column=12)

                
#        self.quitButton = Button(self.frameTOP, text = "QUIT", fg = 'red', command = master.destroy)
#        self.quitButton.pack(side = RIGHT)

      
##################################################       
        self.checkBoxPath1 = Checkbutton(self.frameRIGHT, text = 'Path 1', variable = self.checkVarPath1)
        self.checkBoxPath1.grid(row=0, sticky = W)
        self.checkBoxPath1.select()

        self.checkBoxPath2 = Checkbutton(self.frameRIGHT, text = 'Path 2', variable = self.checkVarPath2)
        self.checkBoxPath2.grid(row=1, sticky = W)
        self.checkBoxPath2.select()
          
        self.checkBoxCurs = Checkbutton(self.frameRIGHT, text = 'Curs', variable = self.checkVarCurs)
        self.checkBoxCurs.grid(row=2, sticky = W)
        self.checkBoxCurs.deselect()
        
        self.checkBoxCurs1 = Checkbutton(self.frameRIGHT, text = 'Curs1', variable = self.checkVarCurs1)
        self.checkBoxCurs1.grid(row=3, sticky = W)
        self.checkBoxCurs1.select()
        
        self.checkBoxCurs2 = Checkbutton(self.frameRIGHT, text = 'Curs2', variable = self.checkVarCurs2)
        self.checkBoxCurs2.grid(row=4, sticky = W)
        self.checkBoxCurs2.select()
          
        self.checkBoxPos1 = Checkbutton(self.frameRIGHT, text = 'Pos 1', variable = self.checkVarPos1)
        self.checkBoxPos1.grid(row=5, sticky = W)
        self.checkBoxPos1.select()
                  
        self.checkBoxPos2 = Checkbutton(self.frameRIGHT, text = 'Pos 2', variable = self.checkVarPos2)
        self.checkBoxPos2.grid(row=6, sticky = W)
        self.checkBoxPos2.select()
         
        self.checkBoxFor1 = Checkbutton(self.frameRIGHT, text = 'Force 1', variable = self.checkVarFor1)
        self.checkBoxFor1.grid(row=7, sticky = W)
        self.checkBoxFor1.deselect()
                  
        self.checkBoxFor2 = Checkbutton(self.frameRIGHT, text = 'Force 2', variable = self.checkVarFor2)
        self.checkBoxFor2.grid(row=8, sticky = W)
        self.checkBoxFor2.deselect()
        
        self.checkBoxRobPos1 = Checkbutton(self.frameRIGHT, text = 'Robot 1', variable = self.checkVarRobPos1)
        self.checkBoxRobPos1.grid(row=9, sticky = W)
        self.checkBoxRobPos1.select()       

        self.checkBoxRobPos2 = Checkbutton(self.frameRIGHT, text = 'Robot 2', variable = self.checkVarRobPos2)
        self.checkBoxRobPos2.grid(row=10, sticky = W)
        self.checkBoxRobPos2.select()   
        
###################################################        
        self.canvas = FigureCanvasTkAgg(self.fig, self.frameLEFT)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.frameLEFT)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx = 5)

###################################################
        self.fileEntry = Entry(self.frameBOT, width = '100')
        self.fileEntry.pack(side = LEFT)
        
        self.fileButton = Button(self.frameBOT, text = 'FILE', command=self.choosefile)
        self.fileButton.pack(side = RIGHT)

###################################################
    def choosefile(self):
        self.file_name = askopenfilename(initialdir = "/media/NAS/Public/Lucas/OLD_MANIPS")#"/home/lucas/phri/lucas/results")
        if self.file_name:
            self.fileEntry.delete(0,END)
        self.fileEntry.insert(0, self.file_name)
        self.loadButton.config(state="normal")

###################################################
    def displayCheckBoxes(self, ParamsClass):
        for child in self.frameBOTBOT.winfo_children():
            child.destroy()        
        
        self.nbTrials = int((ParamsClass.PATH_DURATION - ParamsClass.PART_DURATION_START - ParamsClass.PART_DURATION_FORK)/ (2*ParamsClass.PART_DURATION_BODY + ParamsClass.PART_DURATION_CHOICE + ParamsClass.PART_DURATION_FORK + ParamsClass.PART_DURATION_REGRP))
        self.checkBoxTrials = [0]*self.nbTrials
        self.checkBoxTrialsVar = [0]*self.nbTrials
        self.labelTrials = [0]*self.nbTrials
        
        self.labelTrial = Label(self.frameBOTBOT, text = 'Trials :').grid(row = 0, column = 0)
        
        for i in range(0, self.nbTrials):
            self.labelTrials[i] = Label(self.frameBOTBOT, text =str(i+1)).grid(row=0, column = i+1)
            self.checkBoxTrialsVar[i] = IntVar()
            self.checkBoxTrials[i]=Checkbutton(self.frameBOTBOT, variable = self.checkBoxTrialsVar[i])
            self.checkBoxTrials[i].grid(row=1, column = i+1)
            self.checkBoxTrials[i].select()

        self.labelTrialsAll = Label(self.frameBOTBOT, text = 'All').grid(row=0, column = self.nbTrials +2, padx = 5)
        self.checkBoxTrialsVarAll = IntVar()
        self.checkBoxTrialsAll = Checkbutton(self.frameBOTBOT, variable = self.checkBoxTrialsVarAll)
        self.checkBoxTrialsAll.grid(row= 1, column = self.nbTrials +2, padx = 5)
        self.checkBoxTrialsAll.select()
        self.checkBoxTrialsAll.bind('<ButtonRelease-1>', self.checkAll)
        
        self.labelThreshold = Label(self.frameBOTBOT, text = 'Threshold').grid(row=0, column = self.nbTrials +3, sticky = W, padx = 10)
        self.entryThreshold = Entry(self.frameBOTBOT, width = 4)
        self.entryThreshold.insert(0, '20')
        self.entryThreshold.grid(row=1, column = self.nbTrials +3, padx = 10)
        
###################################################       
    def checkAll(self, event):
        if self.checkBoxTrialsVarAll.get() == 1:
            for i in range (0, self.nbTrials):
                self.checkBoxTrials[i].deselect()
        elif self.checkBoxTrialsVarAll.get() == 0:
            for i in range (0, self.nbTrials):
                self.checkBoxTrials[i].select() 

#####################################################################################################          
class Data:    
    def __init__(self):
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Pos1      = []
        self.Pos2      = []
        self.Curs_pos  = []
        self.Curs_pos1 = []
        self.Curs_pos2 = []
        self.Subj_for1 = []
        self.Subj_for2 = []
        self.Robot_pos1 = []
        self.Robot_pos2 = []
            
        self.startTimeLeader = []
        self.startTimeFollower = []
        
    def reset(self):
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Pos1      = []
        self.Pos2      = []
        self.Curs_pos  = []
        self.Curs_pos1 = []
        self.Curs_pos2 = []
        self.Subj_for1 = []
        self.Subj_for2 = []
        self.Robot_pos1 = []
        self.Robot_pos2 = []
        
        self.startTimeLeader = []
        self.startTimeFollower = []

##################################################################################################### 
class Params:
    def __init__(self):
        self.PATH_DURATION = 0
        self.VITESSE = 0
        self.Y_POS_CURSOR = 0
        self.PART_DURATION_BODY = 0
        self.PART_DURATION_CHOICE = 0
        self.PART_DURATION_FORK = 0
        self.PART_DURATION_REGRP = 0
        self.PART_DURATION_START = 0
        self.POSITION_OFFSET = 0
        self.SENSITIVITY = 0
        self.WINDOW_WIDTH = 0
        self.WINDOW_LENGTH = 0
        self.finalTime = 0
        self.facteurDilatation = 0


#####################################################################################################        
        
def loadDataFromFile():
    global Time, mainApp, Data, Params
    Data.reset()

    file_name = mainApp.file_name   
   
    trial_number = 0    
    
    if file_name == '':
        print "Error in file name"
	quit()

    recupParams(file_name)    
    
    f = open(file_name, 'r')
     
    
    i=0
    m=0
    n=0
    
    for line in f:
        lineReadData = line[ 0 : line.find("\n")]
        try:
            Params.finalTime = float(lineReadData.split('\t')[0])
        except:
            Params.finalTime = 0
    f.close()
    
    time_offset = float(Params.Y_POS_CURSOR)/float(Params.VITESSE)
    Params.facteurDilatation = Params.finalTime/(Params.PATH_DURATION + float(Params.WINDOW_LENGTH)/Params.VITESSE)
    
    
    f = open(file_name, 'r')
    
    k = 0
    p1=0
    p=0
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
            if file_name.find('_s_') or file_name.find('_a_') or file_name.find('_w_') or file_name.find('_u_'):
                Data.Time.append(float(dataList[0]))
                if dataList[1] == "10000":
                    Data.Path_pos1.append(0)
                else:
                    Data.Path_pos1.append(float(dataList[1]) - Params.WINDOW_WIDTH/2)
                if dataList[2] == "10000":
                    Data.Path_pos2.append(0)
                else:
                    Data.Path_pos2.append(float(dataList[2]) - Params.WINDOW_WIDTH/2)
                Data.Pos1.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[3]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                Data.Pos2.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[4]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                Data.Subj_for1.append(float(dataList[5]))
                Data.Subj_for2.append(float(dataList[6]))
                if file_name.find('HFO') != -1 or file_name.find('_s_') != -1  or file_name.find('_s_') != -1  or file_name.find('HFOP') != -1 or file_name.find('_a_') != -1 :
                    Data.Curs_pos.append(Params.WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                elif file_name.find('Alone') != -1 or file_name.find('_w_') != -1 :
                    Data.Curs_pos1.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[3]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                    Data.Curs_pos2.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[4]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                elif file_name.find('RP') != -1 or file_name.find('_u_') != -1 :
                    Data.Curs_pos1.append(Params.WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[7]))/2 - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                    Data.Curs_pos2.append(Params.WINDOW_WIDTH/2*(1 - ((float(dataList[4])+float(dataList[8]))/2 - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                    Data.Robot_pos1.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[7]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)
                    Data.Robot_pos2.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[8]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSITIVITY) - Params.WINDOW_WIDTH/2)                
            else:
                Data.Time.append(float(dataList[0]))
                if dataList[1] == "10000":
                    Data.Path_pos1.append(0)
                else:
                    Data.Path_pos1.append(float(dataList[1]) - Params.WINDOW_WIDTH/2)
                if dataList[2] == "10000":
                    Data.Path_pos2.append(0)
                else:
                    Data.Path_pos2.append(float(dataList[2]) - Params.WINDOW_WIDTH/2)
                Data.Pos1.append(-(float(dataList[3]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                Data.Pos2.append(-(float(dataList[4]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                Data.Subj_for1.append(float(dataList[5]))
                Data.Subj_for2.append(float(dataList[6]))
                if file_name.find('HFO') != -1 or file_name.find('_s_') != -1  or file_name.find('HFOP') != -1 or file_name.find('_a_') != -1 :
                    Data.Curs_pos.append(-((float(dataList[3]) + float(dataList[4]))/2 - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                elif file_name.find('Alone') != -1 or file_name.find('_w_') != -1 :
                    Data.Curs_pos1.append(-(float(dataList[3]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                    Data.Curs_pos2.append(-(float(dataList[4]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                elif file_name.find('RP') != -1 or file_name.find('_u_') != -1 :
                    Data.Curs_pos1.append(-((float(dataList[3]) + float(dataList[9]))/2 - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                    Data.Curs_pos2.append(-((float(dataList[4]) + float(dataList[10]))/2 - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                    Data.Robot_pos1.append(-(float(dataList[9]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)
                    Data.Robot_pos2.append( (float(dataList[10]) - Params.POSITION_OFFSET) * Params.WINDOW_WIDTH/10 / Params.SENSITIVITY)

        i+=1

    
    f.close()
    
    
    if int(mainApp.checkVarFilter.get()) ==1:
        N = int(mainApp.filterEntry.get())
        if N == 0:
            N=1
#        Subj_for1_filtered = [0]*len(Data.Subj_for1)
#        Subj_for2_filtered = [0]*len(Data.Subj_for1)
#        for i in range(0,len(Data.Subj_for1)):
#            if i<N:
#                for j in range (0,i):
#                    Subj_for1_filtered[i] += Data.Subj_for1[j]
#                    Subj_for2_filtered[i] += Data.Subj_for2[j]
#            else:
#                for j in range (i-N,i):
#                    Subj_for1_filtered[i] += Data.Subj_for1[j]
#                    Subj_for2_filtered[i] += Data.Subj_for2[j]         
#            Subj_for1_filtered[i] /= min(i+1, N)
#            Subj_for2_filtered[i] /= min(i+1, N)
#        for i in range(0,len(Data.Subj_for1)):
#            Data.Subj_for1[i] = Subj_for1_filtered[i]
#            Data.Subj_for2[i] = Subj_for2_filtered[i]
        nyq = 0.5*2000 #moitie de la freq d'echantillonage
        low = 10/nyq
        b, a =  sig.butter(N, low, btype = 'low')
        Subj_for1_filtered = [0]*len(Data.Subj_for1)
        Subj_for2_filtered = [0]*len(Data.Subj_for2)
        Subj_for1_filtered = sig.lfilter(b, a, Data.Subj_for1)
        Subj_for2_filtered = sig.lfilter(b, a, Data.Subj_for2)
        for i in range(0,len(Data.Subj_for1)):
            Data.Subj_for1[i] = Subj_for1_filtered[i]
            Data.Subj_for2[i] = Subj_for2_filtered[i]        

    mainApp.displayCheckBoxes(Params)
    mainApp.plotButton.config(state="normal")
    mainApp.plotChoicesButton.config(state="normal")
    
    if file_name.find('HFO') != -1 or file_name.find('_s_') != -1  or file_name.find('HFOP') != -1 or file_name.find('_a_') != -1 :
        mainApp.checkBoxCurs.select()
        mainApp.checkBoxCurs1.deselect()
        mainApp.checkBoxCurs2.deselect()
        mainApp.checkBoxPos1.select()
        mainApp.checkBoxPos2.select()
        mainApp.checkBoxFor1.select()
        mainApp.checkBoxFor2.select()
        mainApp.checkBoxRobPos1.deselect()
        mainApp.checkBoxRobPos2.deselect() 
    elif file_name.find('Alone') != -1 or file_name.find('_w_') != -1 :
        mainApp.checkBoxCurs.deselect()
        mainApp.checkBoxCurs1.select()
        mainApp.checkBoxCurs2.select()
        mainApp.checkBoxPos1.deselect()
        mainApp.checkBoxPos2.deselect()
        mainApp.checkBoxFor1.deselect()
        mainApp.checkBoxFor2.deselect()
        mainApp.checkBoxRobPos1.deselect()
        mainApp.checkBoxRobPos2.deselect() 
    elif file_name.find('RP') != -1 or file_name.find('_u_') != -1 :
        mainApp.checkBoxCurs.deselect()
        mainApp.checkBoxCurs1.select()
        mainApp.checkBoxCurs2.select()
        mainApp.checkBoxPos1.select()
        mainApp.checkBoxPos2.select()
        mainApp.checkBoxFor1.deselect()
        mainApp.checkBoxFor2.deselect()
        mainApp.checkBoxRobPos1.select()
        mainApp.checkBoxRobPos2.select()   
#####################################################################################################

def plot():
    global Data, Params
    
    first_loop_start_time = float(Params.Y_POS_CURSOR)/Params.VITESSE + Params.PART_DURATION_START + 2*Params.PART_DURATION_BODY - 2
    first_loop_stop_time = first_loop_start_time + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK + 2
    
    first_loop_start_time *= Params.facteurDilatation
    first_loop_stop_time *= Params.facteurDilatation
    
    cycle_time = Params.PART_DURATION_REGRP + Params.PART_DURATION_BODY*2 + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK
    cycle_time = cycle_time * Params.facteurDilatation 
    
    start_line = time2line(first_loop_start_time)
    stop_line  = time2line(first_loop_stop_time)
    cycle_lines = time2line(cycle_time)

    trial_number = 0

    if trial_number == 0:  
        i = 0
        j = len(Data.Path_pos1)-1
    elif 0 < trial_number and trial_number <= int((Params.PATH_DURATION - Params.PART_DURATION_START - Params.PART_DURATION_FORK)/ (2*Params.PART_DURATION_BODY + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK + Params.PART_DURATION_REGRP)):
        i = int(start_line + (trial_number-1)*cycle_lines)
        j = int(stop_line + (trial_number-1)*cycle_lines) + 500
    else:
        print "Please select a trial number between 1 and 9 (0 for whole experiment)"
        quit
        
    mainApp.fig.clf()

    mainApp.fig.suptitle(mainApp.file_name)
    legendHandles = []
    legendLabels  = []
    
    ax1 = mainApp.fig.add_subplot(111)
    ax1.set_xlabel('Position (pix)')
    ax1.set_ylabel('Time (s)')
    ax1.axis([-400, 400, int(Data.Time[i])-1, int(Data.Time[j])+1])
    ax1.grid(1,'major', 'both')

    if (int(mainApp.checkVarFor1.get()) == 1 or int(mainApp.checkVarFor2.get()) == 1):
        ax2 = ax1.twiny() 
        ax2.grid(1,'major', 'both')
        ax2.set_xlabel('Force (N)')
        ax2.axis([-1.5, 1.5, int(Data.Time[i])-1, int(Data.Time[j])+1])
    
    if int(mainApp.checkVarPath1.get()) == 1:
        path1, = ax1.plot(Data.Path_pos1[i:j], Data.Time[i:j], color = 'b', linestyle = '--')
        legendHandles.append(path1)
        legendLabels.append("Target Path 1")
    if int(mainApp.checkVarPath2.get()) == 1:
        path2, = ax1.plot(Data.Path_pos2[i:j], Data.Time[i:j], color = 'g', linestyle = '--')
        legendHandles.append(path2)
        legendLabels.append("Target Path 2")
    if int(mainApp.checkVarCurs.get()) == 1:    
        curs,  = ax1.plot(Data.Curs_pos[i:j], Data.Time[i:j],'r-')
        legendHandles.append(curs)
        legendLabels.append("Cursor Position")
    if int(mainApp.checkVarPos1.get()) == 1:    
        pos1,  = ax1.plot(Data.Pos1[i:j], Data.Time[i:j], color = 'b')
        legendHandles.append(pos1)
        legendLabels.append("Handle Position 1")
    if int(mainApp.checkVarPos2.get()) == 1:    
        pos2,  = ax1.plot(Data.Pos2[i:j], Data.Time[i:j], color = 'g')
        legendHandles.append(pos2)
        legendLabels.append("Handle Position 2")
    if int(mainApp.checkVarFor1.get()) == 1:         
        for1, = ax2.plot(Data.Subj_for1[i:j], Data.Time[i:j],'c-', alpha=0.5)
        legendHandles.append(for1)
        legendLabels.append("Force 1")
    if int(mainApp.checkVarFor2.get()) == 1:         
        for2, = ax2.plot(Data.Subj_for2[i:j], Data.Time[i:j],'m-', alpha=0.5)
        legendHandles.append(for2)
        legendLabels.append("Force 2")
    if int(mainApp.checkVarRobPos1.get()) == 1:         
        robpos1, = ax1.plot(Data.Robot_pos1[i:j], Data.Time[i:j],color = 'b', linestyle= '-')
        legendHandles.append(robpos1)
        legendLabels.append("Robot 1")
    if int(mainApp.checkVarRobPos2.get()) == 1:         
        robpos2, = ax1.plot(Data.Robot_pos2[i:j], Data.Time[i:j],color = 'g', linestyle= '-.')
        legendHandles.append(robpos2)
        legendLabels.append("Robot 2")  
    if int(mainApp.checkVarCurs1.get()) == 1:
        curs1,  = ax1.plot(Data.Curs_pos1[i:j], Data.Time[i:j], color = 'm')
        legendHandles.append(curs1)
        legendLabels.append("Cursor1")
    if int(mainApp.checkVarCurs2.get()) == 1:    
        curs2,  = ax1.plot(Data.Curs_pos2[i:j], Data.Time[i:j], color = 'r')
        legendHandles.append(curs2)
        legendLabels.append("Cursor2")
        
    
    mainApp.fig.legend(legendHandles, legendLabels, loc='lower right') # fontsize='small',
    mainApp.canvas.show()


##################################################################################################### 
def plotChoices():
    global Data, Params
        
    Data.startTimeLeader = []
    Data.startTimeFollower = []    
    loop_time_array = []
    
    start_time = float(Params.Y_POS_CURSOR)/Params.VITESSE
    
    end_time = (start_time + Params.PATH_DURATION - Params.PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
    end_time = end_time * Params.facteurDilatation 

    body_start_time = start_time + Params.PART_DURATION_START
    choice_start_time = start_time + Params.PART_DURATION_START + 2*Params.PART_DURATION_BODY
    choice_stop_time = start_time + Params.PART_DURATION_START + 2*Params.PART_DURATION_BODY + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK  

    if int(mainApp.checkVarPartBody.get()) == 1:
        loop_start_time = body_start_time
    else:
        loop_start_time = choice_start_time

    if int(mainApp.checkVarPartChoice.get()) == 1:       
        loop_stop_time  = choice_stop_time
    else:
        loop_stop_time  = choice_start_time

    
    loop_start_time *= Params.facteurDilatation
    loop_start_line = time2line(loop_start_time)
    
    loop_stop_time *= Params.facteurDilatation
    loop_stop_line  = time2line(loop_stop_time)
    
    body_start_time *= Params.facteurDilatation
    body_start_line  = time2line(body_start_time)
    
    choice_start_time *= Params.facteurDilatation
    choice_start_line  = time2line(choice_start_time)
    
    choice_stop_time *= Params.facteurDilatation
    choice_stop_line  = time2line(choice_stop_time)
    
    cycle_time = Params.PART_DURATION_REGRP + Params.PART_DURATION_BODY*2 + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK
    cycle_time = cycle_time * Params.facteurDilatation
    
    posLeader=[0]*len(Data.Pos1)
    posFollower=[0]*len(Data.Pos1)
    cursModif = [0]*len(Data.Curs_pos)
    pathL = [0]*len(Data.Path_pos1)
    pathF = [0]*len(Data.Path_pos2)
    forceL = [0]*len(Data.Subj_for1)
    forceF = [0]*len(Data.Subj_for1)
    subjectL = 0
        
    #print facteurDilatation, start_time, end_time, loop_start_time, loop_stop_time
    mainApp.fig.clf()
    ax1 = mainApp.fig.add_subplot(111)
    ax2 = ax1.twiny()
    ax1.set_xlim(-150,150)
    ax1.set_ylim(0, loop_stop_time - loop_start_time)
    ax2.set_xlim(-1.5,1.5)
    trialNumber = 0
    while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
        if mainApp.checkBoxTrialsVar[trialNumber].get() == 0:
            trialNumber += 1
            loop_start_time += cycle_time
            loop_start_line = time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = time2line(loop_stop_time)
            body_start_time  += cycle_time
            body_start_line  = time2line(body_start_time) 
            choice_start_time  += cycle_time
            choice_start_line  = time2line(choice_start_time)
            choice_stop_time  += cycle_time
            choice_stop_line  = time2line(choice_stop_time)
            continue
        
        markerTimeL = 0
        markerPosL  = 0
        markerTimeF = 0
        markerPosF  = 0
        line_studied = choice_stop_line - time2line(0.5*Params.facteurDilatation)
        
        barycentre = numpy.mean(Data.Curs_pos[choice_start_line:choice_stop_line])
        
        if Data.Path_pos1[line_studied] == Data.Path_pos2[line_studied]:
            trialNumber += 1
            loop_start_time += cycle_time
            loop_start_line = time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = time2line(loop_stop_time)
            body_start_time  += cycle_time
            body_start_line  = time2line(body_start_time) 
            choice_start_time  += cycle_time
            choice_start_line  = time2line(choice_start_time)
            choice_stop_time  += cycle_time
            choice_stop_line  = time2line(choice_stop_time)
            print 0
            continue

        elif Data.Path_pos1[line_studied] == 0:
            if abs(barycentre - Data.Path_pos2[line_studied]) > 1.5*abs(Data.Path_pos2[line_studied] - 0):
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 1
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
                    forceL[i] = Data.Subj_for1[i]
                    forceF[i] = Data.Subj_for2[i]
            else:
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 2
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
                    forceL[i] = Data.Subj_for2[i]
                    forceF[i] = Data.Subj_for1[i]
                
        elif Data.Path_pos2[line_studied] == 0:
            if abs(barycentre - Data.Path_pos1[line_studied]) > 1.5*abs(Data.Path_pos1[line_studied] - 0):
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 2
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
                    forceL[i] = Data.Subj_for2[i]
                    forceF[i] = Data.Subj_for1[i]
            else:
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 1
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
                    forceL[i] = Data.Subj_for1[i]
                    forceF[i] = Data.Subj_for2[i]
                    
        elif Data.Path_pos1[line_studied] != Data.Path_pos2[line_studied]:
            if abs(barycentre - Data.Path_pos1[line_studied]) < abs(barycentre - Data.Path_pos2[line_studied]):
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 1
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
                    forceL[i] = Data.Subj_for1[i]
                    forceF[i] = Data.Subj_for2[i]
            elif abs(barycentre - Data.Path_pos1[line_studied]) > abs(barycentre - Data.Path_pos2[line_studied]):
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    subjectL = 2
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
                    forceL[i] = Data.Subj_for2[i]
                    forceF[i] = Data.Subj_for1[i]
            else:
                loop_start_time += cycle_time
                loop_start_line = time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = time2line(loop_stop_time)
                body_start_time  += cycle_time
                body_start_line  = time2line(body_start_time) 
                choice_start_time  += cycle_time
                choice_start_line  = time2line(choice_start_time)
                choice_stop_time  += cycle_time
                choice_stop_line  = time2line(choice_stop_time)
                continue

        plot_duration = loop_stop_time - loop_start_time
        points_number = loop_stop_line - loop_start_line
        loop_time_array = numpy.linspace(0, plot_duration , points_number )
        
        
        offsetLeader = numpy.mean(posLeader[choice_start_line : choice_start_line + time2line(0.5*Params.facteurDilatation)]) - 0
        offsetFollower = numpy.mean(posFollower[choice_start_line : choice_start_line + time2line(0.5*Params.facteurDilatation)]) - 0
        
        for i in range (loop_start_line, loop_stop_line):
            posLeader[i] -= offsetLeader
            posFollower[i] -= offsetFollower
            cursModif[i] = Data.Curs_pos[i] - (offsetLeader + offsetFollower)/2

#        if mainApp.fileEntry.get().find('HFO') != -1:
        if int(mainApp.checkVarNorm.get()) == 1:
#            for i in range (loop_start_line, loop_stop_line): 
#                posLeader[i] -= Params.WINDOW_WIDTH/2
#                posFollower[i] -= Params.WINDOW_WIDTH/2
#                cursModif[i] -= Params.WINDOW_WIDTH/2
#                pathL[i] -= Params.WINDOW_WIDTH/2
#                pathF[i] -= Params.WINDOW_WIDTH/2
                                    
            if numpy.mean(cursModif[choice_start_line : choice_stop_line]) < 0:
                for i in range (loop_start_line, loop_stop_line):
                    cursModif[i] = - cursModif[i]
                    posLeader[i] = - posLeader[i]
                    posFollower[i] = - posFollower[i]
                    pathL[i] = - pathL[i]
                    pathF[i] = - pathF[i]
                    forceL[i] = - forceL[i]
                    forceF[i] = - forceF[i]
                
#            for i in range (loop_start_line, loop_stop_line): 
#                posLeader[i] += Params.WINDOW_WIDTH/2
#                posFollower[i] += Params.WINDOW_WIDTH/2
#                cursModif[i] += Params.WINDOW_WIDTH/2
#                pathL[i] += Params.WINDOW_WIDTH/2
#                pathF[i] += Params.WINDOW_WIDTH/2
                                
        dt = 0.0

        if int(mainApp.checkVarPos1.get()) == 1:
            posL, = ax1.plot(posLeader[loop_start_line + time2line(dt): loop_stop_line + time2line(dt)], loop_time_array, 'b')
        if int(mainApp.checkVarPos2.get()) == 1:
            posF, = ax1.plot(posFollower[loop_start_line + time2line(dt) : loop_stop_line + time2line(dt)], loop_time_array, 'g')
        if int(mainApp.checkVarPath1.get()) == 1:
            path_L, = ax1.plot(pathL[loop_start_line : loop_stop_line], loop_time_array, 'k', linewidth = 2)
        if int(mainApp.checkVarPath2.get()) == 1:
            path_F, = ax1.plot(pathF[loop_start_line : loop_stop_line], loop_time_array, 'k--',  linewidth = 2)
        if int(mainApp.checkVarCurs.get()) == 1:
            cursPos, = ax1.plot(cursModif[loop_start_line + time2line(dt) : loop_stop_line + time2line(dt)], loop_time_array, 'r')
        if int(mainApp.checkVarFor1.get()) == 1:
            force_L, = ax2.plot(forceL[loop_start_line : loop_stop_line], loop_time_array ,'c-', alpha=0.5)
        if int(mainApp.checkVarFor2.get()) == 1:
            force_F, = ax2.plot(forceF[loop_start_line : loop_stop_line], loop_time_array, 'g-', alpha=0.5)
   
     
        threshold = int(mainApp.entryThreshold.get())
        timeOffset = 0.3*Params.facteurDilatation
        for i in range (choice_start_line + time2line(timeOffset), choice_stop_line):
            if abs(posLeader[i] - 0) > threshold and abs(posLeader[i-1] - 0) < threshold:
                markerPosL = posLeader[i]                
                markerTimeL = Data.Time[i - loop_start_line]
                Data.startTimeLeader.append(Data.Time[i - choice_start_line])
                break
        for i in range (choice_start_line + time2line(timeOffset), choice_stop_line):
            if abs(posFollower[i] - 0) > threshold and abs(posFollower[i-1] - 0) < threshold:
                markerPosF = posFollower[i]                
                markerTimeF = Data.Time[i - loop_start_line]                
                Data.startTimeFollower.append(Data.Time[i - choice_start_line])
                break
            
        markerL = ax1.plot(markerPosL, markerTimeL - dt, 'bo')
        markerF = ax1.plot(markerPosF, markerTimeF - dt, 'go')
        
        print subjectL
            
        trialNumber += 1
        loop_start_time += cycle_time
        loop_start_line = time2line(loop_start_time)
        loop_stop_time  += cycle_time
        loop_stop_line  = time2line(loop_stop_time)
        body_start_time  += cycle_time
        body_start_line  = time2line(body_start_time) 
        choice_start_time  += cycle_time
        choice_start_line  = time2line(choice_start_time)
        choice_stop_time  += cycle_time
        choice_stop_line  = time2line(choice_stop_time)
        
    mainApp.canvas.show()

    strL = ''
    strF = ''
    
    for e in Data.startTimeLeader:
        strL += str(e) + '\t'
    for e in Data.startTimeFollower:
        strF += str(e) + '\t' 
    print "Leader"
    print strL
    print "Follower"
    print strF
    
##################################################################################################### 
def time2line(time):
    global Data
    for i in range (1, len(Data.Time)):
        if Data.Time[i] >= time and Data.Time[i-1] < time:
            return i
    return -1

##################################################################################################### 
def recupParams(file_name):
    global Params
    fp = open(file_name,'r')
    for line in fp:
        if line.find('PATH_DURATION')!=-1:
            Params.PATH_DURATION = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('VITESSE')!=-1:
            Params.VITESSE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('Y_POS_CURSOR')!=-1:
            Params.Y_POS_CURSOR = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_BODY')!=-1:
            Params.PART_DURATION_BODY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_CHOICE')!=-1:
            Params.PART_DURATION_CHOICE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_FORK')!=-1:
            Params.PART_DURATION_FORK = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_REGRP')!=-1:
            Params.PART_DURATION_REGRP = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_START')!=-1:
            Params.PART_DURATION_START = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('POSITION_OFFSET')!=-1:
            Params.POSITION_OFFSET = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('SENSITIVITY')!=-1 or line.find('SENSIBILITY')!=-1:
            Params.SENSITIVITY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_WIDTH')!=-1:
            Params.WINDOW_WIDTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_LENGTH')!=-1:
            Params.WINDOW_LENGTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find("RESULTS") != -1:
            break
    fp.close()


##################################################################################################### 
def main():
    global mainApp, Data, Params
    
    Data = Data()
    Params = Params()

    root = Tk()
    root.title("GUI plot")
    root.resizable(False,False)
#    root.geometry('{}x{}'.format('800', '800'))
    
    mainApp = GUIplot(root)

    root.lift()   
 
    root.mainloop()


##################################################################################################### 
if __name__ == '__main__':
    main()
