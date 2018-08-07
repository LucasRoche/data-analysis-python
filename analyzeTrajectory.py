# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:50:51 2015

@author: roche
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
#    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
#    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
#    
#    file_names = file_names_HFO + file_names_HFOP

    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        if DataClass.fileType == 'HFO':
            continue
        DataClass.analysisStartTime = 0.3
        DataClass.threshold = 20
        DataClass.threshold_ext = 20

        DataClass.analyzeTrajectory()
     




if __name__ == '__main__':
    main()  