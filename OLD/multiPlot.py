#!/usr/bin/env python

#Code written by Lucas Roche
#April 2015

import sys
import random
import numpy
import os
import time
import matplotlib as plt

#from params import *
from math import *
from scipy import stats


def main():
    global Time, somme
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY

    dir_name = "/home/roche/MANIP_v7/expe/VM+AS" + "/"

    file_names = []
    for file in os.listdir(dir_name):
        file_names.append(dir_name + file)
        
    for name in file_names:
        plot(name)


def plot(file_name):
    global Time, somme
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY

    #file_name = "/home/roche/MANIP_v7/expe/RESULTS_scenario_16_trial_2_a_9-4-14-48.txt"

    recupParams(file_name)    
    
    f = open(file_name, 'r')
    
    Time      = []
    Path_pos1 = []
    Path_pos2 = []
    Pos1      = []
    Pos2      = []
    Curs_pos  = []
    Subj_for1 = []
    Subj_for2 = []
    #somme=[]
    
    
    i=0
    m=0
    n=0
    
    for line in f:
        lineReadData = line[ 0 : line.find("\n")]
        finalTime = lineReadData.split('\t')[0]
    f.close()
    
    time_offset = float(Y_POS_CURSOR)/float(VITESSE)
    facteurDilatation = float(finalTime)/(PATH_DURATION + float(WINDOW_LENGTH)/VITESSE)
    
    
    f = open(file_name, 'r')
    
    k = 0
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
            Time.append(float(dataList[0]))
            if dataList[1] == "10000":
                Path_pos1.append(float(WINDOW_WIDTH)/2)
            else:
                Path_pos1.append(float(dataList[1]))
            if dataList[2] == "10000":
                Path_pos2.append(float(WINDOW_WIDTH)/2)
            else:
                Path_pos2.append(float(dataList[2]))
            Pos1.append(WINDOW_WIDTH/2*(1 - (float(dataList[3]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Pos2.append(WINDOW_WIDTH/2*(1 - (float(dataList[4]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Curs_pos.append(WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Subj_for1.append(float(dataList[5]))
            Subj_for2.append(float(dataList[6]))
            #somme.append(float(dataList[5])+float(dataList[6]))
        i+=1
    
    f.close()
    
#    Subj_for1_filtered = [0]*len(Subj_for1)
#    Subj_for2_filtered = [0]*len(Subj_for1)
#    for i in range(0,len(Subj_for1)):
#        if i<100:
#            for j in range (0,i):
#                Subj_for1_filtered[i] += Subj_for1[j]
#                Subj_for2_filtered[i] += Subj_for2[j]
#        else:
#            for j in range (i-100,i):
#                Subj_for1_filtered[i] += Subj_for1[j]
#                Subj_for2_filtered[i] += Subj_for2[j]         
#        Subj_for1_filtered[i] /= min(i+1, 100)
#        Subj_for2_filtered[i] /= min(i+1, 100)

#####################################################################################################  
    trial_number =0
#####################################################################################################
     
    first_loop_start_time = float(Y_POS_CURSOR)/VITESSE + PART_DURATION_START + 2*PART_DURATION_BODY - 2
    first_loop_stop_time = first_loop_start_time + PART_DURATION_CHOICE + PART_DURATION_FORK + 2
    
    first_loop_start_time *= facteurDilatation
    first_loop_stop_time *= facteurDilatation
    
    cycle_time = PART_DURATION_REGRP + PART_DURATION_BODY*2 + PART_DURATION_CHOICE + PART_DURATION_FORK
    cycle_time = cycle_time * facteurDilatation 
    
    start_line = time2line(first_loop_start_time)
    stop_line  = time2line(first_loop_stop_time)
    cycle_lines = time2line(cycle_time)

    if trial_number == 0:  
        i = 0
        j = len(Path_pos1)-1
    elif 0 < trial_number and trial_number < 10:
        i = int(start_line + (trial_number-1)*cycle_lines)
        j = int(stop_line + (trial_number-1)*cycle_lines) + 500
    else:
        print "Please select a trial number between 1 and 9 (0 for whole experiment)"
        quit
    
    fig, ax1 = subplots()
    fig.suptitle(file_name)
    path1, = ax1.plot(Path_pos1[i:j], Time[i:j],'b-')
    path2, = ax1.plot(Path_pos2[i:j], Time[i:j],'g-')
    curs,  = ax1.plot(Curs_pos[i:j], Time[i:j],'r')
    ax1.set_xlabel('Position (pix)')
    ax1.set_ylabel('Time (s)')
    ax1.axis([250, 550, int(Time[i])-1, int(Time[j])+1])

    ax2 = ax1.twiny()
    

    ax2.axis([-1.5, 1.5, int(Time[i])-1, int(Time[j])+1])
    for1, = ax2.plot(Subj_for1[i:j], Time[i:j],'c-', alpha=0.5)
    for2, = ax2.plot(Subj_for2[i:j], Time[i:j],'m-', alpha=0.5)       
    #for1, = ax2.plot(Subj_for1_filtered[i:j], Time[i:j],'c-', alpha=0.5)
    #for2, = ax2.plot(Subj_for2_filtered[i:j], Time[i:j],'m-', alpha=0.5)
    ax2.set_xlabel('Force (N)')
    legend([path1, path2, curs, for1, for2], ['Path 1', 'Path 2', 'Cursor', 'Force 1', 'Force 2'], loc='lower right', fontsize='small')
        
#    if file_name.find("_s_") != -1:
#        ax2.axis([2*250, 2*550, int(Time[i])-1, int(Time[j])+1])
#        pos1, = ax2.plot(Pos1[i:j],Time[i:j],'b-', alpha=0.5)
#        pos2, = ax2.plot(Pos2[i:j],Time[i:j],'g-', alpha=0.5)
#        legend([path1, path2, curs, pos1, pos2], ['Path 1', 'Path 2', 'Cursor', 'Subject 1', 'Subject 2'], loc='lower right', fontsize='small')
#        
    grid(1, 'major', 'both')
    


def time2line(time):
    global Time
    for i in range (1, len(Time)):
        if Time[i] >= time and Time[i-1] < time:
            return i
    return -1

def recupParams(file_name):
    global PATH_DURATION, VITESSE, Y_POS_CURSOR, PART_DURATION_BODY, PART_DURATION_CHOICE, PART_DURATION_FORK, PART_DURATION_REGRP, PART_DURATION_START, POSITION_OFFSET, SENSIBILITY, WINDOW_WIDTH, WINDOW_LENGTH
    fp = open(file_name,'r')
    for line in fp:
        if line.find('PATH_DURATION')!=-1:
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
