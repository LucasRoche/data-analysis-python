# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 14:32:15 2015

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
        endTimes = []
        for file in file_names:
            DataClass = FileData(file)
            DataClass.getDataFromFile()
            DataClass.analysisTime = 0 + 0.05*k
            (tempE, tempF, tempT) = DataClass.intentionDetectionXT()
            
            
            expectedChoicesTotal.extend(tempE)
            finalChoicesTotal.extend(tempF)
            endTimes.extend(tempT)
    
        results = [0]*len(finalChoicesTotal)
        
        for i in range (0, len(finalChoicesTotal)):
            results[i] = expectedChoicesTotal[i] * finalChoicesTotal[i]
    
        somme = float(sum(results))
        size = float(len(results))
        
        good = (somme+size)/2
        
        print DataClass.analysisTime, "\t", good/size*100, '\t', np.mean(endTimes), '\t', np.std(endTimes)


if __name__ == '__main__':
    main()  