#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

# v4 : Amelioration generale du code, implementation de la correction de dilatation temporelle de l'echantillon

import pygame, sys, math, os
from pygame.locals import *
import random
import numpy
import os
import time

from params import *
from math import *
from scipy import stats


def main():
    global Time, Path_pos1, Path_pos2, Curs_pos, Pos_moy

    file_names_HFO = []
    file_names_HFOP = []
    for file in os.listdir("/home/roche/MANIP_v7/expe"):
        if file.endswith(".txt") and file.find("_a_") != -1:
            file_names_HFOP.append("/home/roche/MANIP_v7/expe/" + file)
        elif file.endswith(".txt") and file.find("_s_") != -1:
            file_names_HFO.append("/home/roche/MANIP_v7/expe/" + file)
        else:
            print "Fichier" + file + "non supporte"
            
    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
    traitement_file_name_HFO  = "/home/roche/MANIP_v7/post-traitement/" + "POST-TRAITEMENT_HFO_" + date
    traitement_file_name_HFOP = "/home/roche/MANIP_v7/post-traitement/" + "POST-TRAITEMENT_HFOP_" + date
    

    RMS_error_HFO = [[],[],[]]
    RMS_error_HFOP = [[],[],[]]
    for names in file_names_HFO:
        RMS_from_file = getDataFromFile(names)
        for i in range(0, len(RMS_from_file)):
            RMS_error_HFO[i].extend(RMS_from_file[i])
    for names in file_names_HFOP:
        RMS_from_file = getDataFromFile(names)
        for i in range(0, len(RMS_from_file)):
            RMS_error_HFOP[i].extend(RMS_from_file[i])


           
    RMS_max = max(max(RMS_error_HFO[0]),max(RMS_error_HFO[1]),max(RMS_error_HFO[2]),max(RMS_error_HFOP[0]),max(RMS_error_HFOP[1]),max(RMS_error_HFOP[2]))
    
    (Perf_HFO, Perf_moy_HFO, Stdev_HFO, Stderr_HFO) = calculatePerformance(RMS_error_HFO, RMS_max)
    (Perf_HFOP, Perf_moy_HFOP, Stdev_HFOP, Stderr_HFOP) = calculatePerformance(RMS_error_HFOP, RMS_max)
    
    writeInFile(file_names_HFO, traitement_file_name_HFO, RMS_error_HFO, Perf_HFO, Perf_moy_HFO, Stdev_HFO, Stderr_HFO)
    writeInFile(file_names_HFOP, traitement_file_name_HFOP, RMS_error_HFOP, Perf_HFOP, Perf_moy_HFOP, Stdev_HFOP, Stderr_HFOP)


def getDataFromFile(file_name):
    global Time, Path_pos1, Path_pos2, Curs_pos, Pos_moy
    
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


    for line in results_file:
        if i>=15:
            lineRead= line[0:line.find("\n")]
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


    RMS_error = [[0]*15, [0]*15, [0]*15]

    MAP_force = [[0]*15, [0]*15, [0]*15]
    MAP_force_1 = [[0]*15, [0]*15, [0]*15]
    MAP_force_2 = [[0]*15, [0]*15, [0]*15]

    l=0
    m=0
    n=0

    start_time = float(Y_POS_CURSOR)/VITESSE
    start_time = start_time * facteurDilatation
    start_line = time2line(start_time)
    end_time = (start_time + PATH_DURATION - PART_DURATION_FORK)  #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
    end_time = end_time * facteurDilatation    
    end_line = time2line(end_time)
    
    loop_start_time = start_time + PART_DURATION_START + 2*PART_DURATION_BODY
    loop_start_time = loop_start_time * facteurDilatation
    loop_start_line = time2line(loop_start_time)
    loop_stop_time  = loop_start_time + PART_DURATION_CHOICE + PART_DURATION_FORK
    loop_stop_time  = loop_stop_time * facteurDilatation
    loop_stop_line  = time2line(loop_stop_time)
    
    #print facteurDilatation, start_time, end_time, loop_start_time, loop_stop_time

    while (loop_start_time <= end_time and loop_stop_time<= end_time):

        if Path_pos1[loop_start_line + time2line(PART_DURATION_CHOICE * facteurDilatation) + 100] == Path_pos2[loop_start_line + time2line(PART_DURATION_CHOICE * facteurDilatation) + 100] : #SAME case
            for j in range (loop_start_line, loop_stop_line):  
                RMS_error[0][l] += (min(Path_pos1[j] - Curs_pos[j], Path_pos2[j] - Curs_pos[j]))**2
                MAP_force_1[0][l] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[0][l] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[0][l] += (abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]))
                
            RMS_error[0][l] = sqrt(RMS_error[0][l]/(loop_stop_line - loop_start_line))
            MAP_force_1[0][l] /= (loop_stop_line - loop_start_line)
            MAP_force_2[0][l] /= (loop_stop_line - loop_start_line)
            MAP_force[0][l] /= (loop_stop_line - loop_start_line) 
            l+=1

    
        elif(Path_pos1[loop_start_line + time2line(PART_DURATION_CHOICE * facteurDilatation) + 100] == 10000 or Path_pos2[loop_start_line + time2line(PART_DURATION_CHOICE * facteurDilatation) + 100] == 10000): #ONE case      
            for j in range (loop_start_line, loop_stop_line):
                RMS_error[1][m] += (min(Path_pos1[j] - Curs_pos[j], Path_pos2[j] - Curs_pos[j]))**2
                MAP_force_1[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[1][m] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[1][m] += abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j])
                
            RMS_error[1][m] = sqrt(RMS_error[1][m]/(loop_stop_line - loop_start_line))
            MAP_force_1[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force_2[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force[1][m] /= (loop_stop_line - loop_start_line) 
            m+=1
    
        else: # OPPO case
            for j in range (loop_start_line, loop_stop_line):
                RMS_error[2][n] += (min(Path_pos1[j] - Curs_pos[j], Path_pos2[j] - Curs_pos[j]))**2
                MAP_force_1[2][n] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[2][n] += (Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
                MAP_force[2][n] += abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]) + abs((Pos_moy[j+1] - Pos_moy[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j])
                
            RMS_error[2][n] = sqrt(RMS_error[2][n]/(loop_stop_line - loop_start_line))
            MAP_force_1[2][n] /= (loop_stop_line - loop_start_line)
            MAP_force_2[2][n] /= (loop_stop_line - loop_start_line)
            MAP_force[2][n] /= (loop_stop_line - loop_start_line)
            n+=1

        cycle_time = PART_DURATION_REGRP + PART_DURATION_BODY*2 + PART_DURATION_CHOICE + PART_DURATION_FORK
        cycle_time = cycle_time * facteurDilatation
        loop_start_time += cycle_time
        loop_start_line = time2line(loop_start_time)
        loop_stop_time  += cycle_time
        loop_stop_line  = time2line(loop_stop_time)



    while(1):
        try:
            RMS_error[0].remove(0)
        except: 
            break
    while(1):        
        try:
            RMS_error[1].remove(0)
        except:
            break
    while(1):        
        try:
            RMS_error[2].remove(0)
        except:
            break
        
    return RMS_error
              
   
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

    
        
def writeInFile(file_names, traitement_file_name, RMS_error, Perf, Perf_moy, Stdev, Stderr):
    traitement_file = open(traitement_file_name, 'w')
    
    traitement_file.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    traitement_file.write("\n")
    traitement_file.write("Donnees obetnues a partir des fichiers : \n")
    for f in file_names:
        traitement_file.write(f + "\n")
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
    
    traitement_file.close()


def time2line(time):
    global Time
    for i in range (1, len(Time)):
        if Time[i] >= time and Time[i-1] < time:
            return i
    return -1


if __name__ == '__main__':
    main()

