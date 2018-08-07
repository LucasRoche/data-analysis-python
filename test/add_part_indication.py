# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:56:55 2015

@author: roche
"""
import sys
import random
import numpy
import os
import time
from Tkinter import *
from tkFileDialog import *

root = Tk()
root.withdraw()

dir_name = askdirectory(initialdir = '/home/lucas/Documents/TEST/original')


root.destroy()

file_names = []
file_names_modified = []

for file in os.listdir(dir_name):
    if file.endswith(".txt") and file.find('TRAINING')==-1:
        file_names.append(dir_name + "/" + file)
        file_names_modified.append("/home/lucas/Documents/TEST/modified/" + file)
    else:
        print "Fichier" + file + "non supporte"



PATH_DURATION=0
VITESSE = 0
Y_POS_CURSOR = 0
PART_DURATION_CHOICE = 0
WINDOW_LENGTH = 0
finalTime = 0
path1_old = 0
path1 = 0
path2_old = 0
path2 = 0
lines_array = []
cond1 = "test"
cond2 = "test"

######## Get parameters
for j in range (0, len(file_names)):
    print file_names[j]
    fo = open(file_names[j],'r')
    for line in fo:
        if line.find('PATH_DURATION')!=-1:
            PATH_DURATION = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('VITESSE')!=-1:
            VITESSE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('Y_POS_CURSOR')!=-1:
            Y_POS_CURSOR = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_LENGTH')!=-1:
            WINDOW_LENGTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_CHOICE')!=-1:
            PART_DURATION_CHOICE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find("RESULTS") != -1:
            break
    fo.close()

######### Get final time to compute the dilatation factor
    fo = open(file_names[j],'r')
    for line in fo:
        lineReadData = line[ 0 : line.find("\n")]
        try:
            finalTime = float(lineReadData.split('\t')[0])
        except:
            finalTime = 0
    fo.close()
    
    time_offset = float(Y_POS_CURSOR)/float(VITESSE)
    facteurDilatation = finalTime/(PATH_DURATION + float(WINDOW_LENGTH)/VITESSE)
    
########## Stock all lines in one big array
    fo = open(file_names[j], 'r')
    fo.seek(0, 0)
    del lines_array[:]
    for line in fo:
        lines_array.append(line)
            
    fo.close()
    
######### Add conditions into array
    for i in range(0, len(lines_array)):
        if i < 26:
            continue
        
        line = lines_array[i]         
        line = line[0: line.find('\n')]
        line_list = line.split('\t')
        path1_old = path1
        path2_old = path2
        path1 = float(line_list[1])
        path2 = float(line_list[2])

        if path1_old == -1 and path1 >= 0:
            cond1 = "START"
            cond2 = "START"
            for k in range(0, 10):
                lines_array[i + k] = lines_array[i+k][0: lines_array[i+k].find('\n')] + "\t" + cond1 + "\t" + cond2 + "\n"

        if path1_old == 400 and path1 != 400:
            if path1 < 400 and path1 > 320:
                cond1 = "BODY_GAUCHE"
                cond2 = "BODY_GAUCHE"
                for k in range(0, 10):
                    lines_array[i + k] = lines_array[i+k][0: lines_array[i+k].find('\n')] + "\t" + cond1 + "\t" + cond2 + "\n"
            elif path1 > 400 and path1 < 480:
                cond1 = "BODY_DROITE"
                cond2 = "BODY_DROITE"
                for k in range(0, 10):
                    lines_array[i + k] = lines_array[i+k][0: lines_array[i+k].find('\n')] + "\t" + cond1 + "\t" + cond2 + "\n"            
    
            else:
                if path1 == 320:
                    cond1 = "FORK_GAUCHE"
                elif path1 == 480:
                    cond1 = "FORK_DROITE"
                elif path1 == 10000:
                    cond1 = "FORK_MILIEU"
                if path2 == 320:
                    cond2 = "FORK_GAUCHE"
                elif path2 == 480:
                    cond2 = "FORK_DROITE"
                elif path2 == 10000:
                    cond2 = "FORK_MILIEU"
                decal = int(PART_DURATION_CHOICE*facteurDilatation*1000)    #1 second * facteur dil * 1000 Hz
                for k in range(0, 10):
                    lines_array[i - decal + k] = lines_array[i - decal + k][0: lines_array[i - decal + k].find('\n')] + "\t" + cond1 + "\t" + cond2 + "\n"            

                
########## Write modified file    
    fm = open(file_names_modified[j], 'w')    
    for line in lines_array:
        fm.write(line)

    fm.close()
