#!/usr/bin/env python

import pygame, sys, math, os
from pygame.locals import *
import random

from params import *
from math import *

#Code written by Lucas Roche
#March 2015


#file_name = "./results/" + raw_input("Entrez un nom de fichier de resultats\n")

file_name = "/home/roche/MANIP_v7/results/RESULTS_TRAINING_scenario_199_trial_1_s_1-4-14-49.txt"

file_name_reduit = file_name[file_name.find("RESULTS_")+8 : ]
traitement_file_name = "../post-traitement/POST-TRAITEMENT_" + file_name_reduit

results_file = open(file_name, 'r')

i=0
numberOfLines = (PATH_DURATION + int(WINDOW_LENGTH/VITESSE))*int(AQUISITION_FREQUENCY)+100
Time      = []
Path_pos1 = []
Path_pos2 = []
Subj_pos1 = []
Subj_pos2 = []
Subj_for1 = []
Subj_for2 = []
Curs_pos  = []


for line in results_file:
    if i>=15:
        lineRead= line[0:line.find("\n")]
        dataList = lineRead.split("\t")
        Time.append(float(dataList[0]))
        Path_pos1.append(float(dataList[1]))
        Path_pos2.append(float(dataList[2]))
        Subj_pos1.append(float(dataList[3]))
        Subj_pos2.append(float(dataList[4]))
        Subj_for1.append(float(dataList[5]))
        Subj_for2.append(float(dataList[6]))
        Curs_pos.append(WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
    i+=1

results_file.close()


RMS_error_1 = 0
RMS_error_2 = 0
MAP_force_1 = 0
MAP_force_2 = 0

start = int(float(Y_POS_CURSOR)/VITESSE*AQUISITION_FREQUENCY) + 100
end = int(len(Time) - float(WINDOW_LENGTH - Y_POS_CURSOR)/VITESSE*AQUISITION_FREQUENCY) - 200

print len(Time), start, end
for j in range(start, end):
    RMS_error_1 += ((Path_pos1[j] - 400) - (Subj_pos1[j] - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY )**2
    RMS_error_2 += ((Path_pos2[j] - 400) - (Subj_pos2[j] - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY )**2
    MAP_force_1 += (Subj_pos1[j+1] - Subj_pos1[j-1])/(Time[j+1]-Time[j-1])*Subj_for1[j]
    MAP_force_2 += (Subj_pos2[j+1] - Subj_pos2[j-1])/(Time[j+1]-Time[j-1])*Subj_for2[j]

RMS_error_1 = sqrt(RMS_error_1/len(Time))
RMS_error_2 = sqrt(RMS_error_2/len(Time))
MAP_force_1 /= len(Time)
MAP_force_2 /= len(Time)

traitement_file = open(traitement_file_name, 'w')
traitement_file.write("RMS Error 1 : " + str(RMS_error_1) + "\n")
traitement_file.write("RMS Error 2 : " + str(RMS_error_2) + "\n")
traitement_file.write("MAP Force 1 : " + str(MAP_force_1) + "\n")
traitement_file.write("MAP Force 2 : " + str(MAP_force_2) + "\n")

traitement_file.close()


