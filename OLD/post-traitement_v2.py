#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

# VERSION OBSOLETE
# V2 : implementation du calcul RMS cible sur les trials

import pygame, sys, math, os
from pygame.locals import *
import random

from params import *
from math import *


def main():
    global Time, Path_pos1, Path_pos2, Curs_pos1, Curs_pos2
    #file_name = "../results/" + raw_input("Entrez un nom de fichier de resultats\n")

    file_name = "../results/RESULTS_scenario_36_trial_6_31-3-11-7.txt"
    
    file_name_reduit = file_name[file_name.find("RESULTS_")+8 : ]
    traitement_file_name = "../post-traitement/POST-TRAITEMENT_" + file_name_reduit
    
    results_file = open(file_name, 'r')
    
    i=0
    
    Time      = []
    Path_pos1 = []
    Path_pos2 = []
    Subj_pos1 = []
    Subj_pos2 = []
    Curs_pos1 = []
    Curs_pos2 = []
    Subj_for1 = []
    Subj_for2 = []


    for line in results_file:
        if i>=15:
            lineRead= line[0:line.find("\n")]
            dataList = lineRead.split("\t")
            Time.append(float(dataList[0]))
            Path_pos1.append(float(dataList[1]))
            Path_pos2.append(float(dataList[2]))
            Subj_pos1.append(float(dataList[3]))
            Subj_pos2.append(float(dataList[4]))
            Curs_pos1.append(WINDOW_WIDTH/2*(1 - (float(dataList[3]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Curs_pos2.append(WINDOW_WIDTH/2*(1 - (float(dataList[4]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Subj_for1.append(float(dataList[5]))
            Subj_for2.append(float(dataList[6]))
        i+=1
    
    results_file.close()


    RMS_error_1 = [[0]*100, [0]*100, [0]*100]
    RMS_error_2 = [[0]*100, [0]*100, [0]*100]
    MAP_force_1 = [[0]*100, [0]*100, [0]*100]
    MAP_force_2 = [[0]*100, [0]*100, [0]*100]
    l=0
    m=0
    n=0

    start_time = float(Y_POS_CURSOR)/VITESSE
    start_line = time2line(start_time)
    end_time = start_time + PATH_DURATION - PART_DURATION_FORK #Fin du vecteur -ecart entre la position du curseur et le bord de la fenetre -duree de la ligne droite de fin
    end_line = time2line(end_time)
    
    loop_start_time = start_time + PART_DURATION_START + 2*PART_DURATION_BODY
    loop_start_line = time2line(loop_start_time)
    loop_stop_time  = loop_start_time + PART_DURATION_CHOICE + PART_DURATION_FORK
    loop_stop_line  = time2line(loop_stop_time)
    

    while (loop_start_time <= end_time and loop_stop_time<= end_time):

        if Path_pos1[loop_start_line + time2line(PART_DURATION_CHOICE) + 100] == Path_pos2[loop_start_line + time2line(PART_DURATION_CHOICE) + 100] : #SAME case
            for j in range (loop_start_line, loop_stop_line):  
                RMS_error_1[0][l] += (min(Path_pos1[j] - Curs_pos1[j], Path_pos2[j] - Curs_pos1[j]))**2
                RMS_error_2[0][l] += (min(Path_pos1[j] - Curs_pos2[j], Path_pos2[j] - Curs_pos2[j]))**2
                MAP_force_1[0][l] += (Subj_pos1[j+1] - Subj_pos1[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[0][l] += (Subj_pos2[j+1] - Subj_pos2[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
            RMS_error_1[0][l] = sqrt(RMS_error_1[0][l]/(loop_stop_line - loop_start_line))
            RMS_error_2[0][l] = sqrt(RMS_error_2[0][l]/(loop_stop_line - loop_start_line))
            MAP_force_1[0][l] /= (loop_stop_line - loop_start_line)
            MAP_force_2[0][l] /= (loop_stop_line - loop_start_line)
            l+=1

    
        elif(Path_pos1[loop_start_line + time2line(PART_DURATION_CHOICE) + 100] == 10000 or Path_pos2[loop_start_line + time2line(PART_DURATION_CHOICE) + 100] == 10000): #ONE case      
            for j in range (loop_start_line, loop_stop_line):
                RMS_error_1[1][m] += (min(Path_pos1[j] - Curs_pos1[j], Path_pos2[j] - Curs_pos1[j]))**2
                RMS_error_2[1][m] += (min(Path_pos1[j] - Curs_pos2[j], Path_pos2[j] - Curs_pos2[j]))**2
                MAP_force_1[1][m] += (Subj_pos1[j+1] - Subj_pos1[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[1][m] += (Subj_pos2[j+1] - Subj_pos2[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
            RMS_error_1[1][m] = sqrt(RMS_error_1[1][m]/(loop_stop_line - loop_start_line))
            RMS_error_2[1][m] = sqrt(RMS_error_2[1][m]/(loop_stop_line - loop_start_line))
            MAP_force_1[1][m] /= (loop_stop_line - loop_start_line)
            MAP_force_2[1][m] /= (loop_stop_line - loop_start_line)
            m+=1
    
        else: # OPPO case
            for j in range (loop_start_line, loop_stop_line):
                RMS_error_1[2][n] += (min(Path_pos1[j] - Curs_pos1[j], Path_pos2[j] - Curs_pos1[j]))**2
                RMS_error_2[2][n] += (min(Path_pos1[j] - Curs_pos2[j], Path_pos2[j] - Curs_pos2[j]))**2
                MAP_force_1[2][n] += (Subj_pos1[j+1] - Subj_pos1[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
                MAP_force_2[2][n] += (Subj_pos2[j+1] - Subj_pos2[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]
            RMS_error_1[2][n] = sqrt(RMS_error_1[2][n]/(loop_stop_line - loop_start_line))
            RMS_error_2[2][n] = sqrt(RMS_error_2[2][n]/(loop_stop_line - loop_start_line))
            MAP_force_1[2][n] /= (loop_stop_line - loop_start_line)
            MAP_force_2[2][n] /= (loop_stop_line - loop_start_line)
            n+=1

        loop_start_time += PART_DURATION_REGRP + PART_DURATION_BODY*2 + PART_DURATION_CHOICE + PART_DURATION_FORK
        loop_start_line = time2line(loop_start_time)
        loop_stop_time  += PART_DURATION_REGRP + PART_DURATION_BODY*2 + PART_DURATION_CHOICE + PART_DURATION_FORK
        loop_stop_line  = time2line(loop_stop_time)




    traitement_file = open(traitement_file_name, 'w')
    traitement_file.write("RMS Error 1 : " + str(RMS_error_1) + "\n")
    traitement_file.write("RMS Error 2 : " + str(RMS_error_2) + "\n")
    traitement_file.write("MAP Force 1 : " + str(MAP_force_1) + "\n")
    traitement_file.write("MAP Force 2 : " + str(MAP_force_2) + "\n")
    
    traitement_file.close()


def time2line(time):
    global Time
    for i in range (1, len(Time)):
        if Time[i] >= time and Time[i-1] < time:
            return i
    return -1


if __name__ == '__main__':
    main()

