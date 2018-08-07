# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:49:11 2015

@author: Lucas
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *
import numpy
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import os
import wx
import wx.lib.agw.multidirdialog as MDD

def main():
#    root = Tk()
#    root.withdraw()
#    file_names = askopenfilenames(initialdir = '/media/NAS/Public/Lucas/')
#    file_names = root.tk.splitlist(file_names)
##    file_name = '/home/roche/MANIP/results/trial 1-4-2015 - SAJ + BL/RESULTS_scenario_14_trial_2_a_1-4-15-21.txt' 
#    root.destroy()*
    file_names = []
    app = wx.App(0)
    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/media/NAS/Public/Lucas/",  # defaultPath="C:/Users/users/Desktop/",
                         agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)    
    if dlg.ShowModal() != wx.ID_OK:
        print("You Cancelled The Dialog!")
        dlg.Destroy()    
    paths = dlg.GetPaths()    
    dlg.Destroy()
    app.MainLoop()
    for path in enumerate(paths):
        directory= path[1]#.replace('Home directory','/home/lucas')
        filesToAdd = os.listdir(directory)
        for file in filesToAdd:
            file_names.append(directory + '/' + file)
#    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
#    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
#    file_names_ULTRON = [x for x in file_names if x.find('_u_')!=-1]
#    file_names_ROBOT = [x for x in file_names if x.find('_r_')!=-1]
#    file_names_ALONE = [x for x in file_names if x.find('_w_')!=-1]
#    
#    file_names = file_names_HFO + file_names_HFOP + file_names_ULTRON + file_names_ROBOT + file_names_ALONE

    Delta = []  
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        for n in range(0, len(DataClass.Time) - DataClass.time2line(60)):
            Delta.append(DataClass.Time[n+1] - DataClass.Time[n])    
        
    print len(Delta), min(Delta), numpy.mean(Delta), max(Delta)
    print float(len([x for x in Delta if (x < 0.000202 and x > 0.000198)]))/len(Delta)
    print float(len([x for x in Delta if (x < 0.00021 and x > 0.00019)]))/len(Delta)
    print float(len([x for x in Delta if (x < 0.00022 and x > 0.00018)]))/len(Delta)
#    N=100
#    compte = [0]*N
#    compte_pc = [0]*N
#    T = 1/5000.
#    for x in Delta:
#        for n in range(0,N):
#            low = T*(0.95 + 0.1/N*n)
#            high = T*(0.95 + 0.1/N*(n+1))
#            if x >= low and x < high:
#                compte[n] += 1
#                break
#
#    for n in range(0, len(compte)):
#        compte_pc[n] = float(compte[n])/len(Delta)
#    
#    for n in range(0, len(compte)):
#        print T*(0.95 + 0.1/N*n), T*(0.95 + 0.1/N*(n+1)), compte[n]
#
#    plt.figure(1)
#    for n in range(0,N):
#        plt.plot([T*(0.95 + 0.1/N*n), T*(0.95 + 0.1/N*n)], [0, compte[n]], color='k', linestyle='-', linewidth=2)
#
#    plt.figure(2)
#    for n in range(0,N):
#        plt.plot([T*(0.95 + 0.1/N*n), T*(0.95 + 0.1/N*n)], [0, compte_pc[n]], color='k', linestyle='-', linewidth=2)
    plt.figure()
    ax = plt.subplot(111)
    ax.hist(Delta , 100) 
    ax.xaxis.set_ticks_position('none') 
    plt.xlabel("Loop execution time (s)")
    plt.ylabel("Count")
    plt.show()
     
     
if __name__ == '__main__':
    main()