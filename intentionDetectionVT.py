# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 17:17:47 2015

@author: Lucas
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '/media/NAS/Public/Lucas/OLD_MANIPS/')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
    
    file_names = file_names_HFOP

    expectedChoicesTotal = []
    finalChoicesTotal = []    
        
    print "AnTime\tAccuracy"   

    for k in range (35, 45):
#        for j in range(0, 5):
        expectedChoicesTotal = []
        finalChoicesTotal = []
        for file in file_names:
            DataClass = FileData(file)
            DataClass.getDataFromFile()
            DataClass.low_pass = 10
            DataClass.analysisTime = 0 + 0.05*k
            (tempE, tempF) = DataClass.intentionDetectionVT()
            
            expectedChoicesTotal.extend(tempE)
            finalChoicesTotal.extend(tempF)        
    
        results = [0]*len(finalChoicesTotal)
        
        for i in range (0, len(finalChoicesTotal)):
            results[i] = expectedChoicesTotal[i] * finalChoicesTotal[i]
    
        somme = float(sum(results))
        size = float(len(results))
        
        good = (somme+size)/2
        
        print DataClass.analysisTime, "\t", good/size*100


if __name__ == '__main__':
    main()  