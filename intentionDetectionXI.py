# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:54:24 2015

@author: Lucas
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '../results')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
    
    file_names =file_names_HFOP

    expectedChoicesTotal = []
    finalChoicesTotal = []    
        

    print "Threshold\tStartingTime\tAccuracy\taveragetime\tmin\tmax"   

    for k in range (0, 10):
        for j in range(0,5):
            expectedChoicesTotal = []
            finalChoicesTotal = []
#    fileType = []
            for file in file_names:
                DataClass = FileData(file)
                DataClass.getDataFromFile()
                DataClass.threshold = 100*(k+1)
                DataClass.analysisStartTime = 0.2 + j*0.1
                (tempE, tempF, tempT) = DataClass.intentionDetectionXI()
                
                expectedChoicesTotal.extend(tempE)
                finalChoicesTotal.extend(tempF)
                
            thresh_time = np.mean(tempT)
            thresh_min_time = min(tempT)
            thresh_max_time = max(tempT)
                
            results = [0]*len(finalChoicesTotal)
            
            for i in range (0, len(finalChoicesTotal)):
                results[i] = expectedChoicesTotal[i] * finalChoicesTotal[i]
        
            somme = float(sum(results))
            size = float(len(results))
            
            good = (somme+size)/2
            
            print DataClass.threshold, "\t", DataClass.analysisStartTime, "\t", good/size*100, thresh_time, thresh_min_time, thresh_max_time


if __name__ == '__main__':
    main()  