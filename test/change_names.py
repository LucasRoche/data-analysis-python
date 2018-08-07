# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:32:56 2018

@author: roche
"""

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

dir_name = askdirectory(initialdir = '~/Documents/TEST/')


root.destroy()

file_name = []
file_name_modified = []

for file in os.listdir(dir_name):
    if file.endswith(".txt") and file.find('~')==-1:       
        file_name.append(dir_name + "/" + file)        
        file_name_modified.append("/home/roche/Documents/TEST/Modified/" + file)

#file_name = "/home/roche/MANIP_v7/expe/RESULTS_scenario_11_trial_1_s_1-4-14-51.txt"

for i in range (0, len(file_name)):
    fo = open(file_name[i], 'r')
    fo.seek(0, 0)
    fm = open(file_name_modified[i], 'w')
    
    l=1
    for line in fo:
        if line.find('NAME1')!=-1:
            fm.write('SUBJECT NAME1 : EM\n')
        elif line.find('NAME2')!=-1:
            fm.write('SUBJECT NAME2 : JB\n')      
        else:
            fm.write(line)
    
    fo.close()
    fm.close()
    
    print file_name[i] + " done ..."