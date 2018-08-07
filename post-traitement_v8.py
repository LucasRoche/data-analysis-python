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
from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *

from postTrait_Module import *


def main():
    root = Tk()
    root.withdraw()
    
    results_directory = askdirectory(initialdir = '/home/roche/MANIP_v7/expe')
    results_directory += "/"

    processFiles(results_directory)

def processFiles(results_directory):
    c = {}
    fileList = []
    fileListSorted = [[]]

# Create file list and initialize a class instance of type FileData for each file  
    for filename in sorted(os.listdir(results_directory)):
        fileList.append(results_directory + filename)
        c[results_directory + filename] = FileData(results_directory + filename)

# Get parameters info from each file and recover the data
    for f in fileList:
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
                
# Sanity checking if there is no file alone
    for subject in fileListSorted:
        if len(subject) <= 1:
            print "Warning : file " + subject + " alone, suppressing the file"
            del subject
            
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

    perf_moy_total_HFOP = [0,0,0]
    perf_moy_total_HFO  = [0,0,0]
    for i in range (0, NbSubjects):
        for k in range (0,3):
            perf_moy_total_HFOP[k] += perf_moy_subject_HFOP[i][k]
            perf_moy_total_HFO[k]  += perf_moy_subject_HFO[i][k]
    
    for k in range(0,3):
        perf_moy_total_HFOP[k] /= NbSubjects
        perf_moy_total_HFO [k] /= NbSubjects
    print perf_moy_total_HFOP
    print perf_moy_total_HFO
    #print c[fileListSorted[2][0]].SUBJECT_NAME1
    
    for f in fileList:
        del c[f]


#############################################################################################################
def calculatePerformance(RMS_error, RMS_max):
    
    Perf = [[0]*len(RMS_error[0]), [0]*len(RMS_error[1]),[0]*len(RMS_error[2])]
    
    for i in range (0,3):
        for j in range (0,len(RMS_error[i])):
            Perf[i][j] = 1 - RMS_error[i][j]/RMS_max

 
    Perf_moy = [0]*3
#    Stdev = [0]*3
#    Stderr = [0]*3
    for i in range (0, len(Perf_moy)):
        Perf_moy[i] = numpy.mean(Perf[i])
#        Stdev[i] = numpy.std(Perf[i])
#        Stderr[i] = stats.sem(Perf[i])
    
        
    return(Perf, Perf_moy)

    
if __name__ == '__main__':
    main()


