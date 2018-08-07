# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:56:55 2015

@author: roche
"""
from Tkinter import *
from tkFileDialog import *
import os

root = Tk()
root.withdraw()

dir_name = askdirectory(initialdir = '~/Documents/Manip/')


root.destroy()

file_name = []
file_name_modified = []

for file in os.listdir(dir_name):
    if file.endswith(".txt") and file.find('~')==-1:
        suffix = file[file.find('RESULTS_')+8:]
        if suffix.find('KRP')!=-1:
            suffix=suffix[0:suffix.find('KRP')] + 'PPHARD' + suffix[suffix.find('KRP')+3 :]
        elif suffix.find('HRP')!=-1:
            suffix=suffix[0:suffix.find('HRP')] + 'PPSOFT' + suffix[suffix.find('HRP')+3 :]
        elif suffix.find('_5_')!=-1 and suffix[suffix.find('_5_')-5: suffix.find('_5_')] != 'trial':
            suffix=suffix[0:suffix.find('_5_')+1] + 'NOISY' + suffix[suffix.find('_5_')+2 :]            
        elif suffix.find('_6_')!=-1 and suffix[suffix.find('_6_')-5: suffix.find('_6_')] != 'trial':
            suffix=suffix[0:suffix.find('_6_')+1] + 'DELAYED' + suffix[suffix.find('_6_')+2 :]
        
        file_name.append(dir_name + "/" + file)
        
        file_name_modified.append("/home/lucas/Documents/TEST/modified/" + 'RESULTS_TRANSPARENCE_' + suffix)
    else:
        print "Fichier" + file + "non supporte"


#file_name = "/home/roche/MANIP_v7/expe/RESULTS_scenario_11_trial_1_s_1-4-14-51.txt"

for i in range (0, len(file_name)):
    fo = open(file_name[i], 'r')
    fo.seek(0, 0)
    fm = open(file_name_modified[i], 'w')
    
    l=1
    for line in fo:
        fm.write(line)
#        if l < 26:
#            fm.write(line)
#        else:
#            line = line[0: line.find('\n')]
#            line_list = line.split('\t')
#            if len(line_list)<=12:
#                fm.write(line_list[0] + '\t' + line_list[2] + '\t' + line_list[1] + '\t' + line_list[3] + '\t' + line_list[4] + '\t' + line_list[5] + '\t' + line_list[6] + '\t' + line_list[7] + '\t' + line_list[8] + '\t' + line_list[9] + '\t' + line_list[10] + '\n')
#            else:
#                fm.write(line_list[0] + '\t' + line_list[2] + '\t' + line_list[1] + '\t' + line_list[3] + '\t' + line_list[4] + '\t' + line_list[5] + '\t' + line_list[6] + '\t' + line_list[7] + '\t' + line_list[8] + '\t' + line_list[9] + '\t' + line_list[10] + '\t' + line_list[11] + '\t' + line_list[12] +'\n')
#        l+=1
    
    fo.close()
    fm.close()
    
    print file_name[i] + " done ..."