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
        
        frameTOP = Frame(master)
        frameTOP.pack(side = TOP)
        
        frameBOT = Frame(master)
        frameBOT.pack(side = TOP)
        
        frameRIGHT = Frame(master)
        frameRIGHT.pack(side=RIGHT, padx = 5)
        
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
        self.checkVarForSum = IntVar()
        
        self.fig = plt.Figure()

        self.checkBoxFilter = Checkbutton(frameTOP, variable = self.checkVarFilter)
        self.checkBoxFilter.grid(row=0, column=0)
        self.labelFilter1   = Label(frameTOP, text = 'Filter (Size :').grid(row=0, column=1)
        self.filterEntry    = Entry(frameTOP, width = 4)
        self.filterEntry.grid(row=0, column=2)
        self.filterEntry.insert(0, '100')
        self.labelFilter2   = Label(frameTOP, text = ')').grid(row=0, column=3)
        
        self.loadButton = Button(frameTOP, text = "LOAD DATA", command = loadDataFromFile, state= DISABLED)
        self.loadButton.grid(row=0, column=4)
        
        self.plotButton = Button(frameTOP, text = "PLOT", command = plot, state= DISABLED)
        self.plotButton.grid(row=0, column=5)
        
                
#        self.quitButton = Button(frameTOP, text = "QUIT", fg = 'red', command = master.destroy)
#        self.quitButton.pack(side = RIGHT)

##################################################       
        self.checkBoxPath1 = Checkbutton(frameRIGHT, text = 'Path 1', variable = self.checkVarPath1)
        self.checkBoxPath1.grid(row=0, sticky = W)
        self.checkBoxPath1.select()

        self.checkBoxPath2 = Checkbutton(frameRIGHT, text = 'Path 2', variable = self.checkVarPath2)
        self.checkBoxPath2.grid(row=1, sticky = W)
        self.checkBoxPath2.select()
          
        self.checkBoxCurs = Checkbutton(frameRIGHT, text = 'Curs', variable = self.checkVarCurs)
        self.checkBoxCurs.grid(row=2, sticky = W)
        self.checkBoxCurs.select()
          
        self.checkBoxPos1 = Checkbutton(frameRIGHT, text = 'Pos 1', variable = self.checkVarPos1)
        self.checkBoxPos1.grid(row=3, sticky = W)
        self.checkBoxPos1.deselect()
                  
        self.checkBoxPos2 = Checkbutton(frameRIGHT, text = 'Pos 2', variable = self.checkVarPos2)
        self.checkBoxPos2.grid(row=4, sticky = W)
        self.checkBoxPos2.deselect()
         
        self.checkBoxFor1 = Checkbutton(frameRIGHT, text = 'Force 1', variable = self.checkVarFor1)
        self.checkBoxFor1.grid(row=5, sticky = W)
        self.checkBoxFor1.select()
                  
        self.checkBoxFor2 = Checkbutton(frameRIGHT, text = 'Force 2', variable = self.checkVarFor2)
        self.checkBoxFor2.grid(row=6, sticky = W)
        self.checkBoxFor2.select()
        
        self.checkBoxForSum = Checkbutton(frameRIGHT, text = 'Forces Sum', variable = self.checkVarForSum)
        self.checkBoxForSum.grid(row=7, sticky = W)
        self.checkBoxForSum.deselect()

###################################################        
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx = 5)

###################################################
        self.fileEntry = Entry(frameBOT, width = '80')
        self.fileEntry.pack(side = LEFT)
        
        self.fileButton = Button(frameBOT, text = 'FILE', command=self.choosefile)
        self.fileButton.pack(side = RIGHT)

###################################################



    def choosefile(self):
        self.fileEntry.delete(0, END)
        self.file_name = askopenfilename(initialdir = '../results')
        self.fileEntry.insert(0, self.file_name)
        self.loadButton.config(state="normal")


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
    def reset(self):
        self.Time      = []
        self.Path_pos1 = []
        self.Path_pos2 = []
        self.Pos1      = []
        self.Pos2      = []
        self.Curs_pos  = []
        self.Subj_for1 = []
        self.Subj_for2 = []

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
        Subj_for2_filtered = [0]*len(Data.Subj_for2)
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

#    if int(mainApp.checkVarFilter.get()) ==1:
#        alpha = float(mainApp.filterEntry.get())
#        if alpha == 100:
#            alpha = 0.5
#        Subj_for1_filtered = [0]*len(Data.Subj_for1)
#        Subj_for2_filtered = [0]*len(Data.Subj_for2)
#        for i in range (1,len(Data.Subj_for1)):
#            Subj_for1_filtered[i] = alpha*Subj_for1_filtered[i-1] + (1-alpha)*Data.Subj_for1[i]
#            Subj_for2_filtered[i] = alpha*Subj_for2_filtered[i-1] + (1-alpha)*Data.Subj_for2[i]
#        for i in range(0,len(Data.Subj_for1)):
#            Data.Subj_for1[i] = Subj_for1_filtered[i]
#            Data.Subj_for2[i] = Subj_for2_filtered[i]

            
    mainApp.plotButton.config(state="normal")

 

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

#    d_pos = [0]*len(Data.Time)
#    d2_pos = [0]*len(Data.Time)
#    for t in range (i,j):
#        d_pos[t] = (Data.Curs_pos[t]-Data.Curs_pos[t-1])/(Data.Time[t] - Data.Time[t-1])
#    for t in range (i,j):
#        d2_pos[t] = (d_pos[t]-d_pos[t-1])/(Data.Time[t] - Data.Time[t-1])
#        
#    for t in range (i,j):
#        d2_pos[t] = (d2_pos[t+1] + d2_pos[t-1])/2
#
#    ax2.plot(d2_pos[i:j], Data.Time[i:j])

    if int(mainApp.checkVarForSum.get()) == 1:
        Subj_for_sum = [0]*len(Data.Time)
        for t in range (i,j):
            Subj_for_sum[t] = Data.Subj_for1[t] + Data.Subj_for2[t]            
        ax2.plot(Subj_for_sum[i:j], Data.Time[i:j])
       
    mainApp.fig.legend(legendHandles, legendLabels, loc='lower right') # fontsize='small',
    mainApp.canvas.show()



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
    root.geometry('{}x{}'.format('800', '800'))
    
    mainApp = GUIplot(root)

    root.lift()   
 
    root.mainloop()


##################################################################################################### 
if __name__ == '__main__':
    main()
