#!/usr/bin/python

#Code written by Lucas Roche
#March 2015

import sys
import subprocess
import threading
import time
import random

from params import *


##############################################################################################
#Recuperation des infos sur le trial
####################################

try:
    subject_name_1 = raw_input("Nom du sujet 1 : \n")
    if subject_name_1 == "":
        subject_name_1 = "jeanMi1"
except:
    print "error in subject name - default name : subject_error_1"
    subject_name_1 = "subject_error"

try:
    subject_name_2 = raw_input("Nom du sujet 2 : \n")
    if subject_name_2 == "":
        subject_name_2 = "jeanMi2"
except:
    print "error in subject name - default name : subject_error_2"
    subject_name_2 = "subject_error"

try:
    trial_number = raw_input("Numero d'essai : \n")
    if trial_number == "":
        trial_number = "1"
except:
    print "error in trial number - default trial number : 209"
    trial_number = "1"

try:
    haptic_feedback = raw_input("Avec ous sans retour haptique (a/avec/s/sans): \n")
    if haptic_feedback == "":
        haptic_feedback = "a"
except:
    print "error in trial number - default haptic condition: a"
    haptic_feedback = "a"

try:
    scenario_number = raw_input("Numero de scenario :\n")
    if scenario_number == "":
        scenario_number = "255"
except:
    print "error in scenario number - default scenario number : 1"
    scenario_number = "1"

##############################################################################################
#Creation des differents noms de fichiers utilises

date = time.gmtime(None)
date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
if haptic_feedback == "avec" or haptic_feedback == "a" :
    haptic_feedback = "a"
if haptic_feedback == "sans" or haptic_feedback == "s" :
    haptic_feedback = "s"

results_file_name =  "../results/RESULTS_TRAINING_scenario_" + scenario_number + "_trial_" + trial_number + "_" + haptic_feedback + "_" + date + ".txt"
data_file_name = "/home/roche/MANIP_v7/data/DATA_TRAINING_scenario_" + scenario_number + "_trial_" + trial_number + "_" + haptic_feedback + "_" + date + ".txt"
scenario_file_name = "../scenarios/SCENARIO_" + scenario_number + ".txt"
path_file_name_1 = "../path/PATH_TRAINING_scenario_" + scenario_number + "_subject_" + "1" + ".txt"
path_file_name_2 = "../path/PATH_TRAINING_scenario_" + scenario_number + "_subject_" + "2" + ".txt"


##############################################################################################
#Definition et lancement des deux threads (UI sujet 1 et UI sujet 2)
####################################################################

#Definition d'un temps de depart pour la synchronisation des deux threads
start_time = time.time() + 1.5


def UI_Sujet1():
    print "UI Sujet 1 Starting ....\n"
    subprocess.call(["./trainingUI.py", scenario_number, "1" , str(start_time)])



def UI_Sujet2():
    print "UI Sujet 2 Starting ....\n"
    subprocess.call(["./trainingUI.py", scenario_number, "2" , str(start_time)])



t1 = threading.Thread(group = None, target = UI_Sujet1, args = () )
t1.start()

t2 = threading.Thread(group = None, target = UI_Sujet2, args = () )
t2.start()

#Tache de fond pour garder le script en pause pendant que les threads tournent
while (t1.isAlive() or t2.isAlive()):
    time.sleep(1)

##############################################################################################
#Recuperation du fichier de donnees par ssh

subprocess.call(["scp","paddle@10.0.0.2:/home/paddle/Manip/files/Paddle/data/data.txt","/home/roche/MANIP_v7/data/"])

subprocess.call(["mv","/home/roche/MANIP_v7/data/data.txt", data_file_name])




##############################################################################################
#Creation d'un fichier de resultats combinant tous les fichiers
###############################################################

fData = open(data_file_name, 'r')
fPos1 = open(path_file_name_1, 'r')
fPos2 = open(path_file_name_2, 'r')
fResults = open(results_file_name, 'w')

# Ecriture d'un header avec tous les parametres
fResults.write('PARAMETERS\n')
fResults.write("\n")
fResults.write('SUBJECT NAME1 : ' + subject_name_1 + "\n")
fResults.write('SUBJECT NAME2 : ' + subject_name_2 + "\n")
fResults.write('SCENARIO : ' + scenario_number + "\n")
fResults.write('TRIAL : ' + trial_number + "\n")
fResults.write("\n")
fResults.write('TRIAL DURATION : ' + str(PATH_LENGTH/VITESSE) + " s\n")
fResults.write("\n")
fResults.write("\n")
fResults.write("RESULTS\n")
fResults.write("\n")
fResults.write("ROBOT TIME" + "\t" + "UI TIME" + "\t" + "PATH POSITION 1" + "\t" + "PATH POSITION 1" + "\t" + "POSITION SUBJECT 1" + "\t" + "POSITION SUBJECT 2" + "\t" + "FORCE SUBJECT 1" + "\t" + "FORCE SUBJECT 2" + "\t" + "POSITION X OBSTACLE" + "\t" + "POSITION Y OBSTACLE"  + "\t" + "RADIUS OBSTACLE" + "\n")
fResults.write("\n")

PATH_POS1 = [None]*PATH_LENGTH_TRAINING
PATH_POS2 = [None]*PATH_LENGTH_TRAINING

for line in fPos1: #Creation d'un vecteur contenant les positions du path du sujet 1
    lineReadPosition1 = line
    lineReadPosition1 = lineReadPosition1[ 0 : lineReadPosition1.find("\n")]
    posList1 = lineReadPosition1.split('\t')
    pixel = int(posList1[0])
    PATH_POS1[pixel] = posList1[1]



for line in fPos2: #Creation d'un vecteur contenant les positions du path du sujet 2
    lineReadPosition2 = line
    lineReadPosition2 = lineReadPosition2[ 0 : lineReadPosition2.find("\n")]
    posList2 = lineReadPosition2.split('\t')
    pixel = int(posList2[0])
    PATH_POS2[pixel] = posList2[1]



j=0
for line in fData: #Ecriture des donnes (avec synchronisation)
    lineReadData = line
    lineReadData = lineReadData[ 0 : lineReadData.find("\n")]
    dataList=lineReadData.split('\t')

    timePaddle = float(dataList[0])
    position1 = dataList[1]
    force1 = dataList[2]
    position2 = dataList[3]
    force2 = dataList[4]

    time_offset = float(Y_POS_CURSOR)/float(VITESSE)

    if (timePaddle <= time_offset or int((timePaddle-time_offset)*VITESSE) >= len(PATH_POS)):
	pathPos1 = -1
	pathPos2 = -1
	obstPos = -1
    else:
	pathPos1 = PATH_POS1[int((timePaddle-time_offset)*VITESSE)]
	pathPos2 = PATH_POS2[int((timePaddle-time_offset)*VITESSE)]


    lineWritten = str(timePaddle) + "\t" + str(pathPos1) + "\t" + str(pathPos2) + "\t" + str(position1) + "\t" + str(position2) + "\t" + str(force1) + "\t" + str(force2) + "\n"

    fResults.write(lineWritten)


fData.close()
fPos1.close()
fPos2.close()
fResults.close()
