# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:47:56 2017

@author: lucas
"""

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
    

    data = pandas.read_csv('/home/lucas/Documents/predictors4.csv')

    old_p=0
    fig1 = plt.figure()
    legend = []
    ax = fig1.add_subplot(211)
    colors = [(0, 0, 1) , (0,0,0.8), (0, 0, 0.6), (0, 0, 0.4), (0, 0, 0.2), (0.9, 0, 0)]
    markers = [ '^', 'v', '<', '>', 's', 'o']
    i=0
    for predictor in data["predictor"]:
        if predictor == old_p or predictor == 'SRMS':
            continue
        old_p = predictor
        stop_time = data[data["predictor"]==predictor]["stop_time"]
        precision = data[data["predictor"]==predictor]["precision"]
        ax.plot(stop_time, precision, marker=markers[i], color = colors[i])
        legend.append(predictor)
        print precision
        i+=1
        
    plt.axis([0.5, 1.35, 0, 100])
    plt.legend(legend, loc =8, ncol=3, prop={'size': 20})
    plt.plot([1.5, 1.5], [0, 100], 'k--')
    plt.plot([0.85, 0.85], [0, 100], 'k--')
    plt.plot([0.75, 0.75], [0, 100], 'k--')
#    plt.plot([0., 2.5], [90, 90], 'k--')
    plt.grid('on', axis='y')
#    plt.xlabel("Analysis end time (s)")
    plt.ylabel("Accuracy (%)", fontsize=20)
    plt.xlabel("$t_{stop} (s)$", fontsize=20)
#    plt.xticks(list(plt.xticks()[0]) + [0.85])  
#    ax.set_aspect(0.008) 
    
    x_locs  = np.linspace(0.5, 2, (2-0.5)/0.1+1)
    x_labels = [str(round(i,1)) for i in x_locs]
    plt.xticks(x_locs, x_labels) 
#    ax.xaxis.get_ticklabels()[10].set_color('red')

#    y_locs  = np.append(np.linspace(0, 100, (100-0)/20+1), 90)
#    y_labels = [str(i) for i in y_locs]
#    plt.yticks(y_locs, y_labels)    
#    ax.yaxis.get_ticklabels()[6].set_color('red')
    
#    fig1 = plt.figure()
    ax1 = fig1.add_subplot(212)
    ax2 = ax1.twinx()
    perc_finish = [4.8148148148, 4.8148148148, 4.8148148148, 5.3703703704, 6.1111111111, 12.962962963, 24.8148148148, 43.5185185185, 60.9259259259, 74.0740740741, 79.0740740741, 85, 90.5555555556, 94.0740740741, 95.7407407407, 97.962962963, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    perc_end = [0.0, 0.0, 0.38461538461538464, 0.7692307692307693, 1.153846153846154, 4.615384615384616, 6.923076923076923, 11.153846153846155, 18.461538461538463, 27.692307692307693, 37.30769230769231, 46.53846153846154, 55.00000000000001, 62.69230769230769, 70.76923076923077, 75.76923076923077, 78.84615384615384, 83.46153846153847, 85.76923076923076, 88.84615384615384, 92.6923076923077, 95.0, 96.15384615384616, 96.53846153846153, 96.92307692307692, 97.3076923076923, 97.3076923076923, 98.07692307692307, 98.07692307692307, 98.07692307692307, 98.46153846153847, 98.84615384615385, 99.23076923076923, 99.23076923076923, 100.0, 100, 100, 100, 100]
    stop_times = [0.5+0.05*x for x in range(0,39)]
    ax1.plot(stop_times, perc_finish, marker='o', color=(0.9,0,0))
    ax1.plot(stop_times, perc_end, marker='d', color='k')
    ax1.legend(["1C","ALL"],loc=2, prop={'size': 18})

    plt.xlabel("Analysis end time (s)")
    ax1.set_ylabel("1C - Detected \n motions (%)", color=(0.9,0,0), fontsize=20)
    ax2.set_ylabel("ALL - Completed \n motions (%)", color='k', fontsize=20)
    ax1.set_xlabel("$Time (s)$", fontsize=20)
    ax1.plot([0.75, 0.75], [0, 100], 'k--')
    ax1.plot([0.85, 0.85], [0, 100], 'k--')
    ax1.plot([1.5, 1.5], [0, 100], 'k--')
    ax1.plot([0.75, 3], [5, 5], 'k--')
    ax1.plot([0.85, 3], [10, 10], 'k--')
    ax1.plot([1.5, 3], [90, 90], 'k--')    
#    x_locs  = np.linspace(0.4, 1.3, (1.3-0.4)/0.1+1)
#    x_labels = [str(i) for i in x_locs]
#    plt.xticks(x_locs, x_labels)    
#    ax.xaxis.get_ticklabels()[10].set_color('r')
    ax1.set_aspect(0.004) 
    ax2.set_aspect(0.004)
    ax1.set(adjustable='box-forced')
    ax2.set(adjustable='box-forced')
    plt.xticks(x_locs, x_labels)
    ax1.axis((0.5, 2, 0, 100))
    ax2.axis((0.5, 2, 0, 100))

    plt.tight_layout()
    plt.show()

      
if __name__ == '__main__':
    main()
