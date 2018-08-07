#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:41:14 2017

@author: lucas
"""

from scipy import stats
from Tkinter import *
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *
import pandas
from statsmodels.graphics.gofplots import qqplot
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot


def main():

    data = pandas.read_csv('/home/lucas/Documents/stTime.csv')

    print data[data["StartingTime"] == 0.3][3:4]
    
    stTime = [0]*5
    test = [0]*5
    colors = [(0, 0, 1) , (0,0,0.8), (0, 0, 0.6), (0, 0, 0.4), (0, 0, 0.2), (0, 0, 0.2)]
    markers = ['o', '^', 'v', '<', '>', 's']
    
    for i in range(0,5):
        t_an = round(0.2+i*0.1, 1)
        print t_an
        print data[data["StartingTime"] == t_an]
        stTime[i] = data[data["StartingTime"] == t_an]#["averagetime"]

    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(121)
    ax1.axis([0, 40, 0, 1])
    plt.plot([0,40], [0.85, 0.85], 'r--')
    for i in range(0,5):
        test[i], = plt.plot(stTime[i]["Threshold"], stTime[i]["averagetime"], color=colors[i], marker = markers[i])
    plt.plot(stTime[0]["Threshold"][6:7], stTime[0]["averagetime"][6:7], 'bo', markersize = 10, markeredgewidth = 1)   
    plt.ylabel("Average Analysis Time Completion (s)")
    plt.xlabel("Threshold Size (% of Xmax)")

        
    ax2 = plt.subplot(122)
    ax2.axis([0, 40, 0, 100])
    plt.plot([0,40], [90, 90], 'r--')
    for i in range(0,5):
        plt.plot(stTime[i]["Threshold"], stTime[i]["Accuracy"], color=colors[i], marker = markers[i])        
    plt.plot(stTime[0]["Threshold"][6:7], stTime[0]["Accuracy"][6:7], 'bo', markersize = 10, markeredgewidth = 1)        
    plt.ylabel("Accuracy of the predictor (%)")
    plt.xlabel("Threshold Size (% of Xmax)")
    
    fig.legend(test, ['0.2', '0.3', '0.4', '0.5', '0.6'], loc=8, title='$t_{start} (s)$')
    plt.subplots_adjust(wspace = 0.5, hspace = 2)
        
    plt.show()

      
if __name__ == '__main__':
    main()
