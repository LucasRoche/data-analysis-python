# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:42:06 2015

@author: roche
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
#    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
#    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
#    file_names_ULTRON = [x for x in file_names if x.find('_u_')!=-1]
#    file_names_ROBOT = [x for x in file_names if x.find('_r_')!=-1]
#    file_names_ALONE = [x for x in file_names if x.find('_w_')!=-1]
#    
#    file_names = file_names_HFO + file_names_HFOP + file_names_ULTRON + file_names_ROBOT

#    date = time.gmtime(None)
#    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
#    directory_name = "../post-traitement/PT_StartTime_" + date
#    if not os.path.exists(directory_name):
#        os.makedirs(directory_name)       
#
#    results_file = directory_name + "/PT_StT.txt"
#        
#    f = open(results_file, 'w')
#    
#    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
#    f.write("\n")
##    f.write("Sujets : " + str(SUBJECT_NAME1) + " + " + str(SUBJECT_NAME2) + "\n")
#    f.write("\n")
#    f.write("Donnees obetnues a partir des fichiers : \n")
#    for x in file_names:
#        f.write(x + "\n")
#    f.write("\n")
    
        
    startingTimesL = []
    startingTimesF = []
    stTimeL = []
    stTimeF = []
    stTimeL1 = []
    stTimeL2 = []
    stTimeF1 = []
    stTimeF2 = []
#    fileType = []
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        if DataClass.fileType != 'HFOP':
            continue
        if DataClass.fileType == 'ALONE':
            print file, " ignored ..."
            continue
        DataClass.threshold = 15
        DataClass.analysisStartTime = 0.2
        DataClass.extractStartingTimes()

        if DataClass.fileType == 'HFO' or  DataClass.fileType == 'HFOP':    
#        fileType.append(DataClass.fileType)
#            startingTimesL.append(DataClass.startTimeLeader)
#            startingTimesF.append(DataClass.startTimeFollower)
            stTimeL.extend(DataClass.startTimeLeader)
            stTimeF.extend(DataClass.startTimeFollower)        
        #writeInFile(DataClass, f)
        elif DataClass.fileType == 'ULTRON' or  DataClass.fileType == 'ROBOT':
            stTimeL1.extend(DataClass.startTimeLeader1)
            stTimeL2.extend(DataClass.startTimeLeader2)
            stTimeF1.extend(DataClass.startTimeFollower1)
            stTimeF2.extend(DataClass.startTimeFollower2)
        print file, " treated..."

#    writeInFileFinal(startingTimesL, startingTimesF, f)
#    f.close()

    print len(stTimeF), len(stTimeF1), len(stTimeF2)
    print len(stTimeL), len(stTimeL1), len(stTimeL2)

    stTimeF = stTimeF + stTimeF1 + stTimeF2
    stTimeL = stTimeL + stTimeL1 + stTimeL2
    
        
    MF = sum(stTimeF)/len(stTimeF)
    ML = sum(stTimeL)/len(stTimeL)
    
        
    varF = 0
    for i in range (0, len(stTimeF)):
        varF += (stTimeF[i] - MF)**2
    varF /= len(stTimeF)

    varL = 0
    for i in range (0, len(stTimeL)):
        varL += (stTimeL[i] - ML)**2
    varL /= len(stTimeL)
    
    diff = [0]*len(stTimeL)
    for i in range (0, len(stTimeL)):
        diff[i] = stTimeL[i] - stTimeF[i]
        
    
    M = sum(diff)/len(diff)
    var = 0
    for i in range (0, len(diff)):
        var += (diff[i] - M)**2
    var /= len(diff)
        
    t = M / sqrt(var/len(diff))

    print "Min start times (F, L) : ", min(stTimeF), min(stTimeL)
    print "Max start times (F, L) : ", max(stTimeF), max(stTimeL) 
    print "Means (F, L) : ", MF, ML
    print "Stdev (F, L) : ", sqrt(varF), sqrt(varL)
    print "t-value : ", t
    print "df : ", len(diff)-2
    
    print stTimeF
    print stTimeL
    print sum(stTimeF), len(stTimeF), sum(stTimeF)/len(stTimeF)
    

def writeInFile(DataClass, f):
    f.write("\n")
    f.write("Fichier : " + DataClass.fileName)
    f.write('\n')
    f.write("Starting Times Leader :\n")
    for e in DataClass.startTimeLeader:
        f.write(str(e) + '\t')
    f.write('\n')
    f.write('\n')
    f.write("Starting Times Follower :\n")
    for e in DataClass.startTimeFollower:
        f.write(str(e) + '\t')
    f.write('\n')
    f.write('\n')
    
def writeInFileFinal(startingTimesL, startingTimesF, f):
    f.write('\n')
    f.write('Starting times :\n')
    f.write('Leader\n')        
    for i in range (0, len(startingTimesL)):
        f.write(str(startingTimesL[i]) + '\n')
    f.write('\n')
    f.write('Follower\n')    
    for i in range (0, len(startingTimesL)):
        f.write(str(startingTimesF[i]) + '\n')
        
        
if __name__ == '__main__':
    main()
    