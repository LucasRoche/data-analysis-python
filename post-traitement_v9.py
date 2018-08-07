#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:34:49 2015

@author: roche
"""

import sys
import random
import numpy
import os
import time

#from params import *
from math import *
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

        self.saveVar = IntVar()        
        self.checkBoxSave = Checkbutton(self.frameTOPRIGHT, text = 'Save individual results', variable = self.saveVar, width = 18)
        self.checkBoxSave.grid(row = 2, column = 0)
        self.checkBoxSave.select()

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
    global GUIpostTraitement, c, fileListSorted, perf_moy_subject_HFOP, perf_moy_subject_HFO, perf_subject_HFOP, perf_subject_HFO
    c = {}
    fileList = GUIpostTraitement.fileList
    fileListSorted = [[]]

        
# Get parameters info from each file and recover the data
    for f in fileList:
        c[f] = FileData(f)
        c[f].TIME_WINDOW_BEFORE = float(GUIpostTraitement.entryTimeWB.get())
        c[f].TIME_WINDOW_AFTER = float(GUIpostTraitement.entryTimeWA.get())
        c[f].forceLimit = float(GUIpostTraitement.entryForceLimit.get())
        c[f].dataKept = GUIpostTraitement.dataKeptVar.get()
        c[f].getDataFromFile()
        c[f].calculateRMSandMAP()


# Sort files by subject names
    choice = [0]*len(fileList)   
    k=0
    for i in range(0, len(fileList)):
        match=False
        if i == 0:
            choice[i] = k
            fileListSorted[0].extend( [fileList[i]] )

        else:
            for j in range(0, i):
                if c[fileList[i]].SUBJECT_NAME1 == c[fileList[j]].SUBJECT_NAME1 and c[fileList[i]].SUBJECT_NAME2 == c[fileList[j]].SUBJECT_NAME2:
                    choice[i]=choice[j]
                    fileListSorted[choice[i]].append(fileList[i])
                    match = True
                    break
            if match == False:
                k += 1
                choice[i] = k
                fileListSorted.append([fileList[i]])
                
# Deleting files that are alone in the list if any
    fileListSorted[:] = [x for x in fileListSorted if len(x)>1]

            
# Define number of subjects (for readability of the code)
    NbSubjects = len(fileListSorted)


# Calculate performances for each subject
    RMS_subject_HFOP = []
    RMS_subject_HFO  = []
    for i in range (0, NbSubjects):
        RMS_subject_HFOP.append( [[],[],[]] )
        RMS_subject_HFO.append( [[],[],[]] )  
    for i in range (0, NbSubjects):            # i = sujet parmi liste
        for j in range (0, len(fileListSorted[i])):     # j = essai parmi sujet
            for k in range(0,3):                        # k = SAME, ONE, OPPO
                if c[fileListSorted[i][j]].fileType == 'HFOP':
                    RMS_subject_HFOP[i][k].extend(c[fileListSorted[i][j]].RMS_trial[k])
                elif c[fileListSorted[i][j]].fileType == 'HFO':
                    RMS_subject_HFO[i][k].extend(c[fileListSorted[i][j]].RMS_trial[k])
                else:
                    print 'fileType parameter error'
                    quit()
                #print i,j,k,c[fileListSorted[i][j]].RMS_trial[k]

     
    maxRMSsubjectHFOP = [0]*NbSubjects
    maxRMSsubjectHFO  = [0]*NbSubjects
    maxRMSsubject     = [0]*NbSubjects            
    for i in range (0, NbSubjects):
        try:
            maxRMSsubjectHFOP[i] = max(max(RMS_subject_HFOP[i][0]),max(RMS_subject_HFOP[i][1]),max(RMS_subject_HFOP[i][2]))     
        except:
            maxRMSsubjectHFOP[i] = 0.
    for i in range (0, NbSubjects):
        try:
            maxRMSsubjectHFO[i] = max(max(RMS_subject_HFO[i][0]),max(RMS_subject_HFO[i][1]),max(RMS_subject_HFO[i][2]))     
        except:
            maxRMSsubjectHFO[i] = 0.        
    for i in range (0, NbSubjects):
        maxRMSsubject[i] = max(maxRMSsubjectHFOP[i],maxRMSsubjectHFO[i])
    

    
    perf_subject_HFOP = [0]*NbSubjects
    perf_subject_HFO  = [0]*NbSubjects
    perf_moy_subject_HFOP = [0]*NbSubjects
    perf_moy_subject_HFO  = [0]*NbSubjects
    for i in range (0, NbSubjects):
        (perf_subject_HFOP[i], perf_moy_subject_HFOP[i]) = calculatePerformance(RMS_subject_HFOP[i], maxRMSsubject[i])
    for i in range (0, NbSubjects):
        (perf_subject_HFO[i], perf_moy_subject_HFO[i]) = calculatePerformance(RMS_subject_HFO[i], maxRMSsubject[i])          

    perf_moy_total_HFOP = [[],[],[]]
    perf_moy_total_HFO  = [[],[],[]]
    for i in range (0, NbSubjects):    
        for k in range (0,3):
            if not numpy.isnan(perf_moy_subject_HFOP[i][k]):
                perf_moy_total_HFOP[k].append(perf_moy_subject_HFOP[i][k])
            if not numpy.isnan(perf_moy_subject_HFO[i][k]):
                perf_moy_total_HFO[k].append(perf_moy_subject_HFO[i][k])


    for k in range(0,3):
        perf_moy_total_HFOP[k] = sum(perf_moy_total_HFOP[k])/len(perf_moy_total_HFOP[k])
        perf_moy_total_HFO[k] = sum(perf_moy_total_HFO[k])/len(perf_moy_total_HFO[k])
        

    GUIpostTraitement.resultsHFOP = perf_moy_total_HFOP
    GUIpostTraitement.resultsHFO = perf_moy_total_HFO     
    GUIpostTraitement.resultsLabelHFOP.set(str(perf_moy_total_HFOP))
    GUIpostTraitement.resultsLabelHFO.set(str(perf_moy_total_HFO))


    if GUIpostTraitement.saveVar.get() == 1:
        date = time.gmtime(None)
        date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
        directory_name = "../post-traitement/POST_TRAITEMENT_" + date
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)     
        for i in range (0, NbSubjects):
            writeToFileSubject(directory_name, fileListSorted[i], RMS_subject_HFOP[i], RMS_subject_HFO[i], perf_subject_HFOP[i], perf_subject_HFO[i], perf_moy_subject_HFOP[i], perf_moy_subject_HFO[i])



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
    global c, fileListSorted, perf_moy_subject_HFOP, perf_moy_subject_HFO, perf_subject_HFOP, perf_subject_HFO
  
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
    
    for i in range (0, len(fileListSorted)):
        f.write("\n")
        f.write('Resultats des sujets : ' + c[fileListSorted[i][0]].SUBJECT_NAME1 + '+' + c[fileListSorted[i][0]].SUBJECT_NAME2 + '\n')
        f.write('\n')
        f.write("Mean Performance HFOP: \n")
        f.write("SAME\t\t\tONE\t\t\tOPPO\n")
        f.write(str(perf_moy_subject_HFOP[i][0]) + "\t\t" + str(perf_moy_subject_HFOP[i][1]) + "\t\t" +str(perf_moy_subject_HFOP[i][2]) + "\n")
        f.write('\n')
        f.write("Mean Performance HFO: \n")
        f.write("SAME\t\t\tONE\t\t\tOPPO\n")
        f.write(str(perf_moy_subject_HFO[i][0]) + "\t\t" + str(perf_moy_subject_HFO[i][1]) + "\t\t" +str(perf_moy_subject_HFO[i][2]) + "\n")
        f.write('\n')

    f.write('\n')
    f.write('Perfs HFOP :\n')
    for i in range(0, len(fileListSorted)):
        f.write('\n')
        for j in range (0, max(len(perf_subject_HFOP[i][0]), len(perf_subject_HFOP[i][1]), len(perf_subject_HFOP[i][2]))):
            try:
                f.write(str(perf_subject_HFOP[i][0][j]) + "\t\t")
            except:
                f.write("\t\t")
            try:
                f.write(str(perf_subject_HFOP[i][1][j]) + "\t\t")
            except:
                f.write("\t\t")        
            try:
                f.write(str(perf_subject_HFOP[i][2][j]) + "\t\t")
            except:
                f.write("\t\t")
            f.write("\n")

    f.write('\n')
    f.write('Perfs HFO :\n')
    for i in range(0, len(fileListSorted)):
        f.write('\n')
        for j in range (0, max(len(perf_subject_HFO[i][0]), len(perf_subject_HFO[i][1]), len(perf_subject_HFO[i][2]))):
            try:
                f.write(str(perf_subject_HFO[i][0][j]) + "\t\t")
            except:
                f.write("\t\t")
            try:
                f.write(str(perf_subject_HFO[i][1][j]) + "\t\t")
            except:
                f.write("\t\t")        
            try:
                f.write(str(perf_subject_HFO[i][2][j]) + "\t\t")
            except:
                f.write("\t\t")
            f.write("\n")
            
    f.close()
    
    GUIpostTraitement.messageLabel.set('File Saved.')
    

def writeToFileSubject(directory_name, fileListOneSubject, RMS_HFOP_OneSubject, RMS_HFO_OneSubject, Perf_HFOP_OneSubject, Perf_HFO_OneSubject, Perf_moy_HFOP_OneSubject, Perf_moy_HFO_OneSubject):
    global c
    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
    subjectName1 = c[fileListOneSubject[0]].SUBJECT_NAME1
    subjectName2 = c[fileListOneSubject[0]].SUBJECT_NAME2
    file_name = directory_name + "/POST-TRAITEMENT_" + subjectName1 + "+" + subjectName2 + "-" + date
    
    f = open(file_name , 'w')
    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    f.write("\n")
    f.write("Sujets : " + subjectName1 + "+" + subjectName2 + "\n")
    f.write("\n")
    f.write("Donnees obetnues a partir des fichiers : \n")
    for fi in fileListOneSubject:
        f.write(fi + "\n")
    f.write("\n")
        
    f.write("Fenetre de temps avant fork : " + str(GUIpostTraitement.entryTimeWB.get()) + " s\n")
    f.write("Fenetre de temps apres fork : " + str(GUIpostTraitement.entryTimeWA.get()) + " s\n")
    f.write("Filtre force: donnees gardees = " + GUIpostTraitement.dataKeptVar.get() + " " +  str(GUIpostTraitement.entryForceLimit.get()) + " N")
    f.write("\n")
    f.write("\n")
    f.write("Perf Moyenne HFOP: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for k in range (0,3):
        f.write(str(Perf_moy_HFOP_OneSubject[k]) + "\t\t")
    f.write("\n")
    f.write("\n")
    f.write("Perf Moyenne HFO: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for k in range (0,3):
        f.write(str(Perf_moy_HFO_OneSubject[k]) + "\t\t")
    f.write("\n")
    f.write("\n")
    f.write("\n")
   
    f.write("RMS HFOP: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(RMS_HFOP_OneSubject[0]), len(RMS_HFOP_OneSubject[1]), len(RMS_HFOP_OneSubject[2]))):
        try:
            f.write(str(RMS_HFOP_OneSubject[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(RMS_HFOP_OneSubject[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(RMS_HFOP_OneSubject[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")
    f.write("\n")
    f.write("\n")

    f.write("RMS HFO: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(RMS_HFO_OneSubject[0]), len(RMS_HFO_OneSubject[1]), len(RMS_HFO_OneSubject[2]))):
        try:
            f.write(str(RMS_HFO_OneSubject[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(RMS_HFO_OneSubject[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(RMS_HFO_OneSubject[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")
    f.write("\n")
    f.write("\n")    
    
    f.write("Perf HFOP: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(Perf_HFOP_OneSubject[0]), len(Perf_HFOP_OneSubject[1]), len(Perf_HFOP_OneSubject[2]))):
        try:
            f.write(str(Perf_HFOP_OneSubject[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(Perf_HFOP_OneSubject[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(Perf_HFOP_OneSubject[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")
    f.write("\n")
    f.write("\n")
    
    f.write("Perf HFO: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(Perf_HFO_OneSubject[0]), len(Perf_HFO_OneSubject[1]), len(Perf_HFO_OneSubject[2]))):
        try:
            f.write(str(Perf_HFO_OneSubject[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(Perf_HFO_OneSubject[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(Perf_HFO_OneSubject[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")
    f.write("\n")
    f.write("\n")  

    f.close()



      
if __name__ == '__main__':
    main()


