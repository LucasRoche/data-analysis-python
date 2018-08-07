#!/usr/bin/env python

#Code written by Lucas Roche
#April 2015

import sys
import random
import numpy
import os
import time
import matplotlib.pyplot as plt

#from Params import *
from math import *
from scipy import stats
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
        self.checkVarFilter = IntVar()       
        self.checkVarPath1 = IntVar()      
        self.checkVarPath2 = IntVar()
        self.checkVarCurs = IntVar()
        self.checkVarPos1 = IntVar()
        self.checkVarPos2 = IntVar()
        self.checkVarFor1 = IntVar()
        self.checkVarFor2 = IntVar()
        
        self.fig = plt.Figure()

        self.checkBoxFilter = Checkbutton(self.frameTOP, variable = self.checkVarFilter)
        self.checkBoxFilter.grid(row=0, column=0)
        self.labelFilter1   = Label(self.frameTOP, text = 'Filter (Size :').grid(row=0, column=1)
        self.filterEntry    = Entry(self.frameTOP, width = 4)
        self.filterEntry.grid(row=0, column=2)
        self.filterEntry.insert(0, '100')
        self.labelFilter2   = Label(self.frameTOP, text = ')').grid(row=0, column=3)
        
        self.loadButton = Button(self.frameTOP, text = "LOAD DATA", command = loadDataFromFile, state= DISABLED)
        self.loadButton.grid(row=0, column=4)
        
        self.plotButton = Button(self.frameTOP, text = "PLOT", command = plot, state= DISABLED)
        self.plotButton.grid(row=0, column=5)
        
        self.plotChoicesButton = Button(self.frameTOP, text = "PLOT CHOICES", command = plotChoices, state = DISABLED)
        self.plotChoicesButton.grid(row=0, column=6)
                
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
        self.checkBoxCurs.select()
          
        self.checkBoxPos1 = Checkbutton(self.frameRIGHT, text = 'Pos 1', variable = self.checkVarPos1)
        self.checkBoxPos1.grid(row=3, sticky = W)
        self.checkBoxPos1.deselect()
                  
        self.checkBoxPos2 = Checkbutton(self.frameRIGHT, text = 'Pos 2', variable = self.checkVarPos2)
        self.checkBoxPos2.grid(row=4, sticky = W)
        self.checkBoxPos2.deselect()
         
        self.checkBoxFor1 = Checkbutton(self.frameRIGHT, text = 'Force 1', variable = self.checkVarFor1)
        self.checkBoxFor1.grid(row=5, sticky = W)
        self.checkBoxFor1.select()
                  
        self.checkBoxFor2 = Checkbutton(self.frameRIGHT, text = 'Force 2', variable = self.checkVarFor2)
        self.checkBoxFor2.grid(row=6, sticky = W)
        self.checkBoxFor2.select()

###################################################        
        self.canvas = FigureCanvasTkAgg(self.fig, self.frameLEFT)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.frameLEFT)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx = 5)

###################################################
        self.fileEntry = Entry(self.frameBOT, width = '80')
        self.fileEntry.pack(side = LEFT)
        
        self.fileButton = Button(self.frameBOT, text = 'FILE', command=self.choosefile)
        self.fileButton.pack(side = RIGHT)

###################################################
    def choosefile(self):
        self.fileEntry.delete(0,END)
        self.file_name = askopenfilename(initialdir = '../results')
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
        if self.checkBoxTrialsVarAll.get() == 0:
            for i in range (0, self.nbTrials):
                self.checkBoxTrials[i].deselect()
        elif self.checkBoxTrialsVarAll.get() == 1:
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
        self.Subj_for1 = []
        self.Subj_for2 = []
        
        self.startTimeLeader = []
        self.startTimeFollower = []
        
    def reset(self):
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Pos1      = []
        self.Pos2      = []
        self.Curs_pos  = []
        self.Subj_for1 = []
        self.Subj_for2 = []
        
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
        self.SENSIBILITY = 0
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
            Data.Time.append(float(dataList[0]))
            if dataList[1] == "10000":
                Data.Path_pos1.append(float(Params.WINDOW_WIDTH)/2)
            else:
                Data.Path_pos1.append(float(dataList[1]))
            if dataList[2] == "10000":
                Data.Path_pos2.append(float(Params.WINDOW_WIDTH)/2)
            else:
                Data.Path_pos2.append(float(dataList[2]))
            Data.Pos1.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[3]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSIBILITY))
            Data.Pos2.append(Params.WINDOW_WIDTH/2*(1 - (float(dataList[4]) - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSIBILITY))
            Data.Curs_pos.append(Params.WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - Params.POSITION_OFFSET) / Params.POSITION_OFFSET * Params.SENSIBILITY))
            Data.Subj_for1.append(float(dataList[5]))
            Data.Subj_for2.append(float(dataList[6]))

#            p1=p
#            p=int(100*float(dataList[0])/Params.finalTime)
#            if p!=p1:
#                print p
        i+=1

    
    f.close()
    
    if int(mainApp.checkVarFilter.get()) ==1:
        N = int(mainApp.filterEntry.get())
        if N == 0:
            N=1
        Subj_for1_filtered = [0]*len(Data.Subj_for1)
        Subj_for2_filtered = [0]*len(Data.Subj_for1)
        for i in range(0,len(Data.Subj_for1)):
            if i<N:
                for j in range (0,i):
                    Subj_for1_filtered[i] += Data.Subj_for1[j]
                    Subj_for2_filtered[i] += Data.Subj_for2[j]
            else:
                for j in range (i-N,i):
                    Subj_for1_filtered[i] += Data.Subj_for1[j]
                    Subj_for2_filtered[i] += Data.Subj_for2[j]         
            Subj_for1_filtered[i] /= min(i+1, N)
            Subj_for2_filtered[i] /= min(i+1, N)
        for i in range(0,len(Data.Subj_for1)):
            Data.Subj_for1[i] = Subj_for1_filtered[i]
            Data.Subj_for2[i] = Subj_for2_filtered[i]

    mainApp.displayCheckBoxes(Params)
    mainApp.plotButton.config(state="normal")
    mainApp.plotChoicesButton.config(state="normal")
 

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
    ax1.axis([0, 800, int(Data.Time[i])-1, int(Data.Time[j])+1])
    ax1.grid(1,'major', 'both')

    if (int(mainApp.checkVarFor1.get()) == 1 or int(mainApp.checkVarFor2.get()) == 1):
        ax2 = ax1.twiny() 
        ax2.grid(1,'major', 'both')
        ax2.set_xlabel('Force (N)')
        ax2.axis([-1.5, 1.5, int(Data.Time[i])-1, int(Data.Time[j])+1])
    
    if int(mainApp.checkVarPath1.get()) == 1:
        path1, = ax1.plot(Data.Path_pos1[i:j], Data.Time[i:j],'b-')
        legendHandles.append(path1)
        legendLabels.append("Path 1")
    if int(mainApp.checkVarPath2.get()) == 1:
        path2, = ax1.plot(Data.Path_pos2[i:j], Data.Time[i:j],'g-')
        legendHandles.append(path2)
        legendLabels.append("Path 2")
    if int(mainApp.checkVarCurs.get()) == 1:    
        curs,  = ax1.plot(Data.Curs_pos[i:j], Data.Time[i:j],'r-')
        legendHandles.append(curs)
        legendLabels.append("Cursor")
    if int(mainApp.checkVarPos1.get()) == 1:    
        pos1,  = ax1.plot(Data.Pos1[i:j], Data.Time[i:j],'c-')
        legendHandles.append(pos1)
        legendLabels.append("Pos 1")
    if int(mainApp.checkVarPos2.get()) == 1:    
        pos2,  = ax1.plot(Data.Pos2[i:j], Data.Time[i:j],'m-')
        legendHandles.append(pos2)
        legendLabels.append("Pos 2")
    if int(mainApp.checkVarFor1.get()) == 1:         
        for1, = ax2.plot(Data.Subj_for1[i:j], Data.Time[i:j],'c-', alpha=0.5)
        legendHandles.append(for1)
        legendLabels.append("Force 1")
    if int(mainApp.checkVarFor2.get()) == 1:         
        for2, = ax2.plot(Data.Subj_for2[i:j], Data.Time[i:j],'m-', alpha=0.5)
        legendHandles.append(for2)
        legendLabels.append("Force 2")
    
    
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
    
    loop_start_time = start_time + Params.PART_DURATION_START + 2*Params.PART_DURATION_BODY
    loop_stop_time  = loop_start_time  + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK
    
    loop_start_time = loop_start_time * Params.facteurDilatation
    loop_start_line = time2line(loop_start_time)
    
    loop_stop_time  = loop_stop_time * Params.facteurDilatation
    loop_stop_line  = time2line(loop_stop_time)
    
    cycle_time = Params.PART_DURATION_REGRP + Params.PART_DURATION_BODY*2 + Params.PART_DURATION_CHOICE + Params.PART_DURATION_FORK
    cycle_time = cycle_time * Params.facteurDilatation
    
    posLeader=[0]*len(Data.Pos1)
    posFollower=[0]*len(Data.Pos1)
    cursModif = [0]*len(Data.Curs_pos)
    pathL = [0]*len(Data.Path_pos1)
    pathF = [0]*len(Data.Path_pos2)
        
    #print facteurDilatation, start_time, end_time, loop_start_time, loop_stop_time
    mainApp.fig.clf()
    ax1 = mainApp.fig.add_subplot(111)
    trialNumber = 0
    while (loop_start_time <= end_time and loop_stop_time <= end_time): #start_time + 4*cycle_time):
        if mainApp.checkBoxTrialsVar[trialNumber].get() == 0:
            trialNumber += 1
            loop_start_time += cycle_time
            loop_start_line = time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = time2line(loop_stop_time)
            continue
        
        markerTimeL = 0
        markerPosL  = 0
        markerTimeF = 0
        markerPosF  = 0
        line_studied = loop_stop_line - time2line(0.5*Params.facteurDilatation)
        barycentre = numpy.mean(Data.Curs_pos[loop_start_line : loop_stop_line])
        if Data.Path_pos1[line_studied] == Data.Path_pos2[line_studied]:
            loop_start_time += cycle_time
            loop_start_line = time2line(loop_start_time)
            loop_stop_time  += cycle_time
            loop_stop_line  = time2line(loop_stop_time)
            continue

        elif Data.Path_pos1[line_studied] == 400:
            if abs(barycentre - Data.Path_pos2[line_studied]) > 1.5*abs(Data.Path_pos2[line_studied] - Params.WINDOW_WIDTH/2):
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
            else:
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
                
        elif Data.Path_pos2[line_studied] == 400:
            if abs(barycentre - Data.Path_pos1[line_studied]) > 1.5*abs(Data.Path_pos1[line_studied] - Params.WINDOW_WIDTH/2):
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
            else:
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
                    
        elif Data.Path_pos1[line_studied] != Data.Path_pos2[line_studied]:
            if abs(barycentre - Data.Path_pos1[line_studied]) < abs(barycentre - Data.Path_pos2[line_studied]):
                #Leader = Sujet 1
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos1[i]
                    posFollower[i] = Data.Pos2[i]
                    pathL[i] = Data.Path_pos1[i]
                    pathF[i] = Data.Path_pos2[i]
            elif abs(barycentre - Data.Path_pos1[line_studied]) > abs(barycentre - Data.Path_pos2[line_studied]):
                #leader = sujet 2
                for i in range(loop_start_line, loop_stop_line):
                    posLeader[i] = Data.Pos2[i]
                    posFollower[i] = Data.Pos1[i]
                    pathL[i] = Data.Path_pos2[i]
                    pathF[i] = Data.Path_pos1[i]
            else:
                loop_start_time += cycle_time
                loop_start_line = time2line(loop_start_time)
                loop_stop_time  += cycle_time
                loop_stop_line  = time2line(loop_stop_time)
                continue

        plot_duration = loop_stop_time - loop_start_time
        points_number = loop_stop_line - loop_start_line
        loop_time_array = numpy.linspace(0, plot_duration , points_number )
        
        
        offsetLeader = numpy.mean(posLeader[loop_start_line : loop_start_line + time2line(0.5*Params.facteurDilatation)]) - Params.WINDOW_WIDTH/2
        offsetFollower = numpy.mean(posFollower[loop_start_line : loop_start_line + time2line(0.5*Params.facteurDilatation)]) - Params.WINDOW_WIDTH/2
        
        for i in range (loop_start_line, loop_stop_line):
            posLeader[i] -= offsetLeader
            posFollower[i] -= offsetFollower
            cursModif[i] = Data.Curs_pos[i] - (offsetLeader + offsetFollower)/2

        if mainApp.fileEntry.get().find('_s_') != -1:
            for i in range (loop_start_line, loop_stop_line): 
                posLeader[i] -= Params.WINDOW_WIDTH/2
                posFollower[i] -= Params.WINDOW_WIDTH/2
                cursModif[i] -= Params.WINDOW_WIDTH/2
                pathL[i] -= Params.WINDOW_WIDTH/2
                pathF[i] -= Params.WINDOW_WIDTH/2
                                    
            if numpy.mean(cursModif[loop_start_line : loop_stop_line]) < 0:
                for i in range (loop_start_line, loop_stop_line):
                    cursModif[i] = - cursModif[i]
                    posLeader[i] = - posLeader[i]
                    posFollower[i] = - posFollower[i]
                    pathL[i] = - pathL[i]
                    pathF[i] = - pathF[i]
                
            for i in range (loop_start_line, loop_stop_line): 
                posLeader[i] += Params.WINDOW_WIDTH/2
                posFollower[i] += Params.WINDOW_WIDTH/2
                cursModif[i] += Params.WINDOW_WIDTH/2
                pathL[i] += Params.WINDOW_WIDTH/2
                pathF[i] += Params.WINDOW_WIDTH/2
                
        elif mainApp.fileEntry.get().find('_a_') != -1:
            for i in range (loop_start_line, loop_stop_line): 
                posLeader[i] -= Params.WINDOW_WIDTH/2
                posFollower[i] -= Params.WINDOW_WIDTH/2
                cursModif[i] -= Params.WINDOW_WIDTH/2
                pathL[i] -= Params.WINDOW_WIDTH/2
                pathF[i] -= Params.WINDOW_WIDTH/2

            if numpy.mean(cursModif[loop_start_line : loop_stop_line]) < 0:
                for i in range (loop_start_line, loop_stop_line):
                    cursModif[i] = - cursModif[i]
                    posLeader[i] = -posLeader[i]
                    posFollower[i] = -posFollower[i]
                    pathL[i] = - pathL[i]
                    pathF[i] = - pathF[i]
                                
            for i in range (loop_start_line, loop_stop_line): 
                posLeader[i] += Params.WINDOW_WIDTH/2
                posFollower[i] += Params.WINDOW_WIDTH/2
                cursModif[i] += Params.WINDOW_WIDTH/2            
                pathL[i] += Params.WINDOW_WIDTH/2
                pathF[i] += Params.WINDOW_WIDTH/2
                

        posL, = ax1.plot(posLeader[loop_start_line : loop_stop_line], loop_time_array, 'b')
        posF, = ax1.plot(posFollower[loop_start_line : loop_stop_line], loop_time_array, 'g')
        path_L, = ax1.plot(pathL[loop_start_line : loop_stop_line], loop_time_array, 'k')
        path_F, = ax1.plot(pathF[loop_start_line : loop_stop_line], loop_time_array, 'k--')
        cursPos, = ax1.plot(cursModif[loop_start_line : loop_stop_line], loop_time_array, 'r')
        
        threshold = int(mainApp.entryThreshold.get())
        timeOffset = 0.4*Params.facteurDilatation
        for i in range (loop_start_line + time2line(timeOffset), loop_stop_line):
            if abs(posLeader[i] - Params.WINDOW_WIDTH/2) > threshold and abs(posLeader[i-1] - Params.WINDOW_WIDTH/2) < threshold:
                markerPosL = posLeader[i]                
                markerTimeL = Data.Time[i - loop_start_line]
                Data.startTimeLeader.append(Data.Time[i - loop_start_line])
                break
        for i in range (loop_start_line + time2line(timeOffset), loop_stop_line):
            if abs(posFollower[i] - Params.WINDOW_WIDTH/2) > threshold and abs(posFollower[i-1] - Params.WINDOW_WIDTH/2) < threshold:
                markerPosF = posFollower[i]                
                markerTimeF = Data.Time[i - loop_start_line]                
                Data.startTimeFollower.append(Data.Time[i - loop_start_line])
                break
            
        markerL = ax1.plot(markerPosL, markerTimeL, 'bo')
        markerF = ax1.plot(markerPosF, markerTimeF, 'go')
            
        trialNumber += 1
        loop_start_time += cycle_time
        loop_start_line = time2line(loop_start_time)
        loop_stop_time  += cycle_time
        loop_stop_line  = time2line(loop_stop_time)
        
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
        elif line.find('SENSIBILITY')!=-1:
            Params.SENSIBILITY = float(line[line.find(' : ')+3 : line.find("\n")])
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
