

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
    root = Tk()
    root.withdraw()    
    file_name = askopenfilename(initialdir = "~/phri/lucas/fichiers_csv/")
    root.destroy()
    data = pandas.read_csv(file_name)

    data = data.drop(data[data['RMS']> np.mean(data['RMS'])+3.5*np.std(data['RMS'])].index)        
    data = data.drop(data[data['RMS']> 100].index) 
#    data = data.drop(data[(data['TYPE']=='ALONE') & ((data['TRIAL_NUMBER']==1 )| (data['TRIAL_NUMBER']==2))].index)     
    
    data = data.reset_index()
    
    #Calculate performances and add them to the dataFrame
    N = len(data['RMS'])
    PERFS = [0]*N
    RMSmax = max(data['RMS'])
    for i in range(0, N):
        PERFS[i] = 1 - data['RMS'][i]/RMSmax
    
    data['PERFS'] = PERFS 
    
    data = data[(data['TYPE']=='ALONE') & (data['TRIAL']=='OPPO')]

    old_s=0
    i=0
    plt.figure()
    legend = []
    ax = plt.subplot(111)
    for subject in list(set(data["SUBJ_NAME"])):
        print i
        i+=1
        if subject == old_s:
            continue
        old_s = subject
        perf = data[(data["SUBJ_NAME"] == subject)]['FOM']
        print perf
        ax.plot(perf, 'o-')
        legend.append(subject)
        
    plt.legend(legend, loc=0)
    plt.show()

      
if __name__ == '__main__':
    main()
