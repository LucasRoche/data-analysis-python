#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:54:44 2015

@author: roche
"""

import sys
import random
import numpy
import os
import time

from params import *
from math import *
from scipy import stats
from Tkinter import *
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
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
        self.labelTimeWA.grid(row = 1, column = 2, sticky = E)
        self.entryTimeWA = Entry(self.frameTOPLEFT, width = 3)
        self.entryTimeWA.grid(row=1, column=3, sticky = W)
        self.entryTimeWA.insert(0, '1')
        
        self.labelForceLimit = Label(self.frameTOPLEFT, text = 'Force filter limit :')
        self.labelForceLimit.grid(row=1, column = 4, sticky = E)
        self.entryForceLimit = Entry(self.frameTOPLEFT, width = 3)
        self.entryForceLimit.grid(row =1, column = 5, sticky = W)
        self.entryForceLimit.insert(0, '1.5')
        
        self.labelDataKept = Label(self.frameTOPLEFT, text = 'Data kept :')
        self.labelDataKept.grid(row = 1, column = 6, sticky = E)
        self.dataKeptVar = StringVar()
        self.dataKeptVar.set('INTER')
        self.dataKeptMenu = Menubutton(self.frameTOPLEFT, textvariable=self.dataKeptVar, relief=RAISED, width = 5)
        self.dataKeptMenu.menu  =  Menu ( self.dataKeptMenu, tearoff = 0 )
        self.dataKeptMenu["menu"]  =  self.dataKeptMenu.menu
        self.dataKeptMenu.menu.add_command(label = 'INTER', command = self.setINTER)
        self.dataKeptMenu.menu.add_command(label = 'EXTER', command = self.setEXTER)
        self.dataKeptMenu.grid(row = 1, column = 7, sticky = W)
        
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
        filesToAdd = askopenfilenames(initialdir = "../results")
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

        
# Get parameters info from each file and recover the data
    for f in fileList:
        c = FileData(f)
        c.TIME_WINDOW_BEFORE = float(GUIpostTraitement.entryTimeWB.get())
        c.TIME_WINDOW_AFTER = float(GUIpostTraitement.entryTimeWA.get())
        c.forceLimit = float(GUIpostTraitement.entryForceLimit.get())
        c.dataKept = GUIpostTraitement.dataKeptVar.get()
        c.getDataFromFile()
        c.calculateRMSandMAP()
        if c.fileType == 'HFOP':
            for k in range (0, len(RMS_all_HFOP)):
                RMS_all_HFOP[k].extend(c.RMS_trial[k])
        elif c.fileType == 'HFO':
            for k in range (0, len(RMS_all_HFO)):
                RMS_all_HFO[k].extend(c.RMS_trial[k])
        print f
        print c.RMS_trial[0]
        print c.RMS_trial[1]
        print c.RMS_trial[2]

# Calculate performances
    RMS_max_HFOP = max(max(RMS_all_HFOP[0]), max(RMS_all_HFOP[1]), max(RMS_all_HFOP[2]))
    RMS_max_HFO  = max(max(RMS_all_HFO[0]), max(RMS_all_HFO[1]), max(RMS_all_HFO[2]))   
    RMS_max = max(RMS_max_HFO, RMS_max_HFOP)
    
    perf_HFOP = []
    perf_HFO = []
    perf_moy_HFOP = 0
    perf_moy_HFO = 0
    
    (perf_HFOP, perf_moy_HFOP) = calculatePerformance(RMS_all_HFOP, RMS_max)
    (perf_HFO, perf_moy_HFO) = calculatePerformance(RMS_all_HFO, RMS_max)
    
       

    GUIpostTraitement.resultsHFOP = perf_moy_HFOP
    GUIpostTraitement.resultsHFO = perf_moy_HFO     
    GUIpostTraitement.resultsLabelHFOP.set(str(perf_moy_HFOP))
    GUIpostTraitement.resultsLabelHFO.set(str(perf_moy_HFO))

# T-test for comparison between HFO and HFOP
    N_HFOP = [len(perf_HFOP[0]), len(perf_HFOP[1]), len(perf_HFOP[2])]
    N_HFO  = [len(perf_HFO[0]),  len(perf_HFO[1]),  len(perf_HFO[2])]
    var_HFOP = [0,0,0]
    var_HFO  = [0,0,0]
    SX1X2 = 0.0
    t = [0,0,0]
    df = [0,0,0]
    for k in range (0,3):
        for i in range (0, len(perf_HFOP[k])):
            var_HFOP[k] += ((perf_HFOP[k][i]-perf_moy_HFOP[k])**2)
        var_HFOP[k] /= N_HFOP[k]
        
    for k in range (0,3):
        for i in range (0, len(perf_HFO[k])):
            var_HFO[k] += ((perf_HFO[k][i]-perf_moy_HFO[k])**2)
        var_HFO[k] /= N_HFO[k]
        
    for k in range (0,3):
        SX1X2 = sqrt(var_HFOP[k]/N_HFOP[k] + var_HFO[k]/N_HFO[k])
        
        t[k] = (perf_moy_HFOP[k] - perf_moy_HFO[k])/SX1X2
        df[k] = N_HFOP[k] + N_HFO[k] - 2

    print "Perfs HFOP : ", perf_moy_HFOP
    print "Stdev HFOP : ", sqrt(var_HFOP[0]), ',' , sqrt(var_HFOP[1]), ',' , sqrt(var_HFOP[2])
    print "Perfs HFO : ", perf_moy_HFO
    print "Stdev HFO : ", sqrt(var_HFO[0]), ',' , sqrt(var_HFO[1]), ',' , sqrt(var_HFO[2])
    print t
    print df



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
