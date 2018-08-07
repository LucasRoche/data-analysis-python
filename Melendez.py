# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 11:51:16 2015

@author: Lucas
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.cm as cmx

def main():
    global D_total
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '../results')
    file_names = root.tk.splitlist(file_names)
#    file_name = '/home/roche/MANIP/results/trial 1-4-2015 - SAJ + BL/RESULTS_scenario_14_trial_2_a_1-4-15-21.txt' 
    root.destroy()
    
    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
    file_names_ULTRON = [x for x in file_names if x.find('_u_')!=-1]
    file_names_ROBOT = [x for x in file_names if x.find('_r_')!=-1]
    file_names_ALONE = [x for x in file_names if x.find('_w_')!=-1]
    
    file_names = file_names_HFOP
    
    
    D_total = []

    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        DataClass.MelendezCalderon()
        D_total.append(DataClass.D_global)

    for i in range(0, len(D_total)):
        cMap = plt.get_cmap('gist_rainbow')
        cNorm = clr.Normalize(vmin=0, vmax=len(D_total[i])/2)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cMap)
        for j in range(0, len(D_total[i])):
            colorVal = scalarMap.to_rgba(int(j/2))
            plt.figure(10*i+int(j/6))
#            plt.figure(i)
            plt.plot(D_total[i][j], color=colorVal)    
            print D_total[i][j].index(max(D_total[i][j]))
#    for k in range (0, len(D_total[0])):
#        plt.figure(k)
#        plt.plot(D_total[0][k])

    plt.show()          
        


    
if __name__ == '__main__':
    main()
    

