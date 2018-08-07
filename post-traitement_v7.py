#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

# v6 : Recuperation des parametres depuis le fichier RESULTS plutot que le fichier params.py

import sys
import random
import numpy
import os
import time

#from params import *
from math import *
from scipy import stats

FENETRE_TEMPS_AVANT = 1.0 #Define the time window from which data is extracted. The time window is defined as : FENETRE_TEMPS_AVANT before the fork and FENETRE_TEMPS_APRES after.
FENETRE_TEMPS_APRES = 1.0 

#GENERAL NOTATIONS : 
#HFOP : experiments WITH haptic feedback between the two subjects
#HFO : experiments WITHOUT haptic feedback between the two subjects


def main():
    global Time, Path_pos1, Path_pos2, Curs_pos, Pos_moy, directory_name
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY, WINDOW_WIDTH, WINDOW_LENGTH, SUBJECT_NAME1, SUBJECT_NAME2

    results_directory = '/home/roche/phri/MANIP/results/2nd protocol/All/'

    file_names_HFO = []
    file_names_HFOP = []
    for file in os.listdir(results_directory):
        if file.endswith(".txt") and file.find("_a_") != -1:
            file_names_HFOP.append(results_directory + file)
        elif file.endswith(".txt") and file.find("_s_") != -1:
            file_names_HFO.append(results_directory + file)
        else:
            print "Fichier " + file + " non supporte"
            
    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
    
    directory_name = "/home/roche/MANIP_v7/post-traitement/POST_TRAITEMENT_" + date
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)    
    
    traitement_file_name_HFO  = directory_name + "/" + "POST_TRAITEMENT_HFO_" + date
    traitement_file_name_HFOP = directory_name + "/" + "POST_TRAITEMENT_HFOP_" + date
    

    RMS_error_HFO = [[],[],[]]
    RMS_error_HFOP = [[],[],[]]
    MAP_force_HFO = [[],[],[]]
    MAP_force_HFOP = [[],[],[]]
    for name in file_names_HFO:
        recupParams(name)
        (RMS_from_file, MAP_from_file) = getDataFromFile(name)
        writeInFileOne(name, RMS_from_file, MAP_from_file)
        RMS_from_file = removePoints(RMS_from_file)
        MAP_from_file = removePoints(MAP_from_file)
        for i in range(0, len(RMS_from_file)):
            RMS_error_HFO[i].extend(RMS_from_file[i])
            MAP_force_HFO[i].extend(MAP_from_file[i])
    for name in file_names_HFOP:
        (RMS_from_file, MAP_from_file) = getDataFromFile(name)
        writeInFileOne(name, RMS_from_file, MAP_from_file)
        RMS_from_file = removePoints(RMS_from_file)
        MAP_from_file = removePoints(MAP_from_file)
        for i in range(0, len(RMS_from_file)):
            RMS_error_HFOP[i].extend(RMS_from_file[i])
            MAP_force_HFOP[i].extend(MAP_from_file[i])


    try:
        maxHFOP= max(max(RMS_error_HFOP[0]),max(RMS_error_HFOP[1]),max(RMS_error_HFOP[2]))     
    except:
        maxHFOP = 0.
    try:
        maxHFO = max(max(RMS_error_HFO[0]),max(RMS_error_HFO[1]),max(RMS_error_HFO[2]))
    except:
        maxHFO = 0.
    RMS_max = max(maxHFO, maxHFOP)    
    
    (Perf_HFO, Perf_moy_HFO, Stdev_HFO, Stderr_HFO) = calculatePerformance(RMS_error_HFO, RMS_max)
    (Perf_HFOP, Perf_moy_HFOP, Stdev_HFOP, Stderr_HFOP) = calculatePerformance(RMS_error_HFOP, RMS_max)
    
    writeInFileGlobal(file_names_HFO, traitement_file_name_HFO, RMS_error_HFO, Perf_HFO, Perf_moy_HFO, Stdev_HFO, Stderr_HFO, MAP_force_HFO)
    writeInFileGlobal(file_names_HFOP, traitement_file_name_HFOP, RMS_error_HFOP, Perf_HFOP, Perf_moy_HFOP, Stdev_HFOP, Stderr_HFOP, MAP_force_HFOP)


def getDataFromFile(file_name):
    global Time, Path_pos1, Path_pos2, Curs_pos, Pos_moy
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY, WINDOW_WIDTH, WINDOW_LENGTH, SUBJECT_NAME1, SUBJECT_NAME2

    
    fData = open(file_name, 'r')
    for line in fData:
        lineReadData = line[ 0 : line.find("\n")]
        finalTime = lineReadData.split('\t')[0]
    fData.close()
    
    time_offset = float(Y_POS_CURSOR)/float(VITESSE)
    facteurDilatation = float(finalTime)/(PATH_DURATION + float(WINDOW_LENGTH)/VITESSE)
    
    results_file = open(file_name, 'r')
    i=0
    Time      = []
    Path_pos1 = []
    Path_pos2 = []
    Pos_moy   = []
    Curs_pos  = []
    Subj_for1 = []
    Subj_for2 = []
    
    
    k = 0
    for line in results_file:
        lineRead= line[0:line.find("\n")]
        if lineRead.find("ROBOT TIME") != -1:
            k =1
            continue
        if k==1 and line == "\n":
            k=2
            continue
        if k ==2:
            dataList = lineRead.split("\t")
            Time.append(float(dataList[0]))
            Path_pos1.append(float(dataList[1]))
            Path_pos2.append(float(dataList[2]))
            Pos_moy.append((float(dataList[3])+float(dataList[4]))/2)
            Curs_pos.append(WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Subj_for1.append(float(dataList[5]))
            Subj_for2.append(float(dataList[6]))
        i+=1
    
    results_file.close()


    RMS_error = [["."]*30, ["."]*30, ["."]*30]

    MAP_force = [["."]*30, ["."]*30, ["."]*30]
    MAP_force_1 = [[0]*30, [0]*30, [0]*30]
    MAP_force_2 = [[0]*30, [0]*30, [0]*30]

    l=0
    m=0
    n=0

    start_time = float(Y_POS_CURSOR)/VITESSE
    
    end_time = (start_time + PATH_DURATION - PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
    end_time = end_time * facteurDilatation    
    
    loop_start_time = start_time + PART_DURATION_START + 2*PART_DURATION_BODY + PART_DURATION_CHOICE  - int(FENETRE_TEMPS_AVANT)
    loop_stop_time  = loop_start_time  + int(FENETRE_TEMPS_AVANT + FENETRE_TEMPS_APRES) #PART_DURATION_CHOICE + PART_DURATION_FORK
    
    loop_start_time = loop_start_time * facteurDilatation
    loop_start_line = time2line(loop_start_time)
    
    loop_stop_time  = loop_stop_time * facteurDilatation
    loop_stop_line  = time2line(loop_stop_time)
    
    cycle_time = PART_DURATION_REGRP + PART_DURATION_BODY*2 + PART_DURATION_CHOICE + PART_DURATION_FORK
    cycle_time = cycle_time * facteurDilatation
    
    #print facteurDilatation, start_time, end_time, loop_start_time, loop_stop_time

    while (loop_start_time <= end_time and loop_stop_time<= end_time):

        if Path_pos1[loop_start_line + time2line(FENETRE_TEMPS_AVANT * facteurDilatation) + 4000] == Path_pos2[loop_start_line + time2line(FENETRE_TEMPS_AVANT * facteurDilatation) + 4000] : #SAME case
            for j in range (loop_start_line, loop_stop_line):
                if RMS_error[0][l] == ".":
                    RMS_error[0][l] = 0
                if MAP_force[0][l] == ".":
                    MAP_force[0][l] = 0
                RMS_error[0][l] += (min(Path_pos1[j] - Curs_pos[j], Path_pos2[j] - Curs_pos[j]))**2
                MAP_force_1[0][l] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[0][l] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[0][l] += (abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]))
                
            RMS_error[0][l] = sqrt(RMS_error[0][l]/(loop_stop_line - loop_start_line))
            MAP_force_1[0][l] /= (loop_stop_line - loop_start_line)
            MAP_force_2[0][l] /= (loop_stop_line - loop_start_line)
            MAP_force[0][l] /= (loop_stop_line - loop_start_line) 
            l+=1
            m+=1
            n+=1

        elif(Path_pos2[loop_start_line + time2line(FENETRE_TEMPS_AVANT * facteurDilatation) + 4000] == 10000): #ONE1 case      
            for j in range (loop_start_line, loop_stop_line):
                if RMS_error[1][m] == ".":
                    RMS_error[1][m] = 0
                if MAP_force[1][m] == ".":
                    MAP_force[1][m] = 0
                RMS_error[1][m] += (Path_pos1[j] - Curs_pos[j])**2
                MAP_force_1[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[1][m] += abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j])
                
            RMS_error[1][m] = sqrt(RMS_error[1][m]/(loop_stop_line - loop_start_line))
            MAP_force_1[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force_2[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force[1][m] /= (loop_stop_line - loop_start_line) 
            m+=1
            l+=1
            n+=1
    
        elif(Path_pos1[loop_start_line + time2line(FENETRE_TEMPS_AVANT * facteurDilatation) + 4000] == 10000): #ONE2 case      
            for j in range (loop_start_line, loop_stop_line):
                if RMS_error[1][m] == ".":
                    RMS_error[1][m] = 0
                if MAP_force[1][m] == ".":
                    MAP_force[1][m] = 0
                RMS_error[1][m] += (Path_pos2[j] - Curs_pos[j])**2
                MAP_force_1[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[1][m] += abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j])
                
            RMS_error[1][m] = sqrt(RMS_error[1][m]/(loop_stop_line - loop_start_line))
            MAP_force_1[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force_2[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force[1][m] /= (loop_stop_line - loop_start_line) 
            m+=1
            l+=1
            n+=1
        
        
    
        else: # OPPO case
            for j in range (loop_start_line, loop_stop_line):
                if RMS_error[2][n] == ".":
                    RMS_error[2][n] = 0
                if MAP_force[2][n] == ".":
                    MAP_force[2][n] = 0
                RMS_error[2][n] += (min(Path_pos1[j] - Curs_pos[j], Path_pos2[j] - Curs_pos[j]))**2
                MAP_force_1[2][n] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[2][n] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[2][n] += abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j])
                
            RMS_error[2][n] = sqrt(RMS_error[2][n]/(loop_stop_line - loop_start_line))
            MAP_force_1[2][n] /= (loop_stop_line - loop_start_line)
            MAP_force_2[2][n] /= (loop_stop_line - loop_start_line)
            MAP_force[2][n] /= (loop_stop_line - loop_start_line)
            n+=1
            l+=1
            m+=1

        loop_start_time += cycle_time
        loop_start_line = time2line(loop_start_time)
        loop_stop_time  += cycle_time
        loop_stop_line  = time2line(loop_stop_time)
        
    return RMS_error, MAP_force


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
              
   
def calculatePerformance(RMS_error, RMS_max):

    
    Perf = [[0]*len(RMS_error[0]), [0]*len(RMS_error[1]),[0]*len(RMS_error[2])]
    
    for i in range (0,3):
        for j in range (0,len(RMS_error[i])):
            Perf[i][j] = 1 - RMS_error[i][j]/RMS_max

 
    Perf_moy = [0]*3
    Stdev = [0]*3
    Stderr = [0]*3
    for i in range (0, len(Perf_moy)):
        Perf_moy[i] = mean(Perf[i])
        Stdev[i] = numpy.std(Perf[i])
        Stderr[i] = stats.sem(Perf[i])
    
        
    return(Perf, Perf_moy, Stdev, Stderr)

    
        
def writeInFileGlobal(file_names, traitement_file_name, RMS_error, Perf, Perf_moy, Stdev, Stderr, MAP_force):
    global SUBJECT_NAME1, SUBJECT_NAME2    
    traitement_file = open(traitement_file_name, 'w')
    
    traitement_file.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    traitement_file.write("\n")
    traitement_file.write("Sujets : " + str(SUBJECT_NAME1) + " + " + str(SUBJECT_NAME2) + "\n")
    traitement_file.write("\n")
    traitement_file.write("Donnees obetnues a partir des fichiers : \n")
    for f in file_names:
        traitement_file.write(f + "\n")
    traitement_file.write("\n")
    
    traitement_file.write("Fenetre de temps avant fork :" + str(FENETRE_TEMPS_AVANT) + "\n")
    traitement_file.write("Fenetre de temps apres fork :" + str(FENETRE_TEMPS_APRES) + "\n")
    traitement_file.write("\n")    
    
    traitement_file.write("RMS Error: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(RMS_error[0]), len(RMS_error[1]), len(RMS_error[2]))):
        try:
            traitement_file.write(str(RMS_error[0][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        try:
            traitement_file.write(str(RMS_error[1][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")        
        try:
            traitement_file.write(str(RMS_error[2][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        traitement_file.write("\n")
    
    traitement_file.write("\n")
    traitement_file.write("Perf: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(RMS_error[0]), len(RMS_error[1]), len(RMS_error[2]))):
        try:
            traitement_file.write(str(Perf[0][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        try:
            traitement_file.write(str(Perf[1][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")        
        try:
            traitement_file.write(str(Perf[2][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        traitement_file.write("\n")
    
    traitement_file.write("\n")
    traitement_file.write("Mean Performance: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    traitement_file.write(str(Perf_moy[0]) + "\t\t" + str(Perf_moy[1]) + "\t\t" +str(Perf_moy[2]) + "\n")
    
    traitement_file.write("\n")
    traitement_file.write("Standard deviation: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    traitement_file.write(str(Stdev[0]) + "\t\t" + str(Stdev[1]) + "\t\t" +str(Stdev[2]) + "\n")
    
    traitement_file.write("\n")
    traitement_file.write("Standard error of measurement: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    traitement_file.write(str(Stderr[0]) + "\t\t" + str(Stderr[1]) + "\t\t" +str(Stderr[2]) + "\n")
    
    traitement_file.write("\n")
    traitement_file.write("\n")
    
    traitement_file.write("MAP Force: \n")
    traitement_file.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(MAP_force[0]), len(MAP_force[1]), len(MAP_force[2]))):
        try:
            traitement_file.write(str(MAP_force[0][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        try:
            traitement_file.write(str(MAP_force[1][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")        
        try:
            traitement_file.write(str(MAP_force[2][i]) + "\t\t")
        except:
            traitement_file.write(".\t\t\t")
        traitement_file.write("\n")       
    traitement_file.write("\n")
    
    traitement_file.close()


def writeInFileOne(file_name, RMS_from_file, MAP_from_file):
    global SUBJECT_NAME1, SUBJECT_NAME2
    global directory_name
    f_name = directory_name + "/" + "POST_TRAITEMENT_" + file_name[file_name.find("RESULTS_")+8 : ]
    f = open(f_name , 'w')
    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    f.write("\n")
    f.write("Sujets : " + str(SUBJECT_NAME1) + " + " + str(SUBJECT_NAME2) + "\n")
    f.write("\n")
    f.write("Donnees obetnues a partir du fichier : \n")
    f.write(file_name + "\n")
    f.write("\n")
        
    f.write("Fenetre de temps avant fork :" + str(FENETRE_TEMPS_AVANT) + "\n")
    f.write("Fenetre de temps apres fork :" + str(FENETRE_TEMPS_APRES) + "\n")
    f.write("\n")
    
    f.write("RMS Error: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(RMS_from_file[0]), len(RMS_from_file[1]), len(RMS_from_file[2]))):
        try:
            f.write(str(RMS_from_file[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(RMS_from_file[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(RMS_from_file[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")
    f.write("\n")
    f.write("\n")

    f.write("MAP Force: \n")
    f.write("SAME\t\t\tONE\t\t\tOPPO\n")
    for i in range (0, max(len(MAP_from_file[0]), len(MAP_from_file[1]), len(MAP_from_file[2]))):
        try:
            f.write(str(MAP_from_file[0][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        try:
            f.write(str(MAP_from_file[1][i]) + "\t\t")
        except:
            f.write(".\t\t\t")        
        try:
            f.write(str(MAP_from_file[2][i]) + "\t\t")
        except:
            f.write(".\t\t\t")
        f.write("\n")       
    f.write("\n")
    

def time2line(time):
    global Time
    for i in range (1, len(Time)):
        if Time[i] >= time and Time[i-1] < time:
            return i
    return -1


def recupParams(file_name):
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY, WINDOW_WIDTH, WINDOW_LENGTH, SUBJECT_NAME1, SUBJECT_NAME2
    fp = open(file_name,'r')
    for line in fp:      
        if line.find('SUBJECT NAME1')!=-1:
            SUBJECT_NAME1 = line[line.find(' : ')+3 : line.find("\n")]
        elif line.find('SUBJECT NAME2')!=-1:
            SUBJECT_NAME2 = line[line.find(' : ')+3 : line.find("\n")]     
        elif line.find('PATH_DURATION')!=-1:
            PATH_DURATION = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('VITESSE')!=-1:
            VITESSE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('Y_POS_CURSOR')!=-1:
            Y_POS_CURSOR = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_BODY')!=-1:
            PART_DURATION_BODY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_CHOICE')!=-1:
            PART_DURATION_CHOICE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_FORK')!=-1:
            PART_DURATION_FORK = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_REGRP')!=-1:
            PART_DURATION_REGRP = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_START')!=-1:
            PART_DURATION_START = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('POSITION_OFFSET')!=-1:
            POSITION_OFFSET = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('SENSIBILITY')!=-1:
            SENSIBILITY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_WIDTH')!=-1:
            WINDOW_WIDTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_LENGTH')!=-1:
            WINDOW_LENGTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find("RESULTS") != -1:
            break
    fp.close()
    
    
if __name__ == '__main__':
    main()

