# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:19:23 2017

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
from statsmodels.stats.weightstats import ztest
from math import pi

class bcolors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m" 
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 
    
    
def main():
    global HFOP, HFO, ALONE, PPSOFT, PPHARD, NOISY, SAME, ONE, OPPO, ALONE_SAME, ALONE_SAME, ALONE_ONE,ALONE_OPPO, HFO_SAME, HFO_ONE, HFO_OPPO, HFOP_SAME, HFOP_ONE, HFOP_OPPO, PPSOFT_SAME, PPSOFT_ONE, PPSOFT_OPPO, PPHARD_SAME, PPHARD_ONE, PPHARD_OPPO, NOISY_SAME, NOISY_ONE, NOISY_OPPO, DELAYED_SAME, DELAYED_ONE, DELAYED_OPPO
    global SAME2, SAME3, ONE2, ONE3, OPPO2, OPPO3, PPSOFT, PPHARD, NOISY, DELAYED
    
    file = "~/phri/lucas/fichiers_csv/questionnaire.csv"
    data = pandas.read_csv(file)
    
    dictio = {}
    NAMES = []
    MEANS = []
    STERR = []
    for expe in ['TRAJ', 'INT']:    
        for question in set(data['QUESTION']):
            for cond in set(data['COND']):
                name = expe + '-' + cond + '-' + question
#                dictio[name] = np.mean(data[(data['COND']==cond) & (data['QUESTION']==question )][expe])
                NAMES.append(name)
                MEANS.append(np.mean(data[(data['COND']==cond) & (data['QUESTION']==question )][expe]))
                STERR.append(stats.sem(data[(data['COND']==cond) & (data['QUESTION']==question )][expe]))
        
#    y_pos = range(0, len(dictio.keys()))
        y_pos = range(0, len(NAMES))
    i=0
    plt.figure()
#    for reponse in dictio.keys():
#        plt.barh(y_pos[i], dictio[reponse], align='center', height = 0.7)
    for i in range(0, len(NAMES)):
        plt.barh(y_pos[i], MEANS[i], xerr=STERR[i], height = 0.7, ecolor = 'k')
            
#    plt.yticks(y_pos, dictio.keys())
    plt.yticks(y_pos, NAMES)
#    plt.xticks(rotation=90)
    plt.tight_layout()    
    plt.show()

    
def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    return aov
 
def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov

def cohenns_d(group1, group2):
    return (np.mean(group1)-np.mean(group2))/np.sqrt(0.5*(np.std(group1)+np.std(group2)))
    
def print_ttest_results(str_group1, str_group2):
    group1 = eval(str_group1)
    group2 = eval(str_group2)
    if abs(stats.ttest_ind(group1, group2)[1]) < 0.011:
        color = bcolors.GREEN
    else:
        color = bcolors.ENDC
    print color + str_group1+" vs "+str_group2+" :   \tt-value: " , round(stats.ttest_ind(group1, group2)[0], 5), "\tp-value :", round(stats.ttest_ind(group1, group2)[1],5), "\td-value :", round(cohenns_d(group1, group2),5)
    print color + str_group1+" vs "+str_group2+" :   \tz-value: " , round(ztest(group1, group2)[0], 5), "\tp-value :", round(ztest(group1, group2)[1],5), bcolors.ENDC

def print_latex_table(conds):
    print '\\begin{tabular}{l*{' + str(2*(len(conds)-1)) + '}{x{1cm}}}'
    print '\\thickhline'
    temp = ''
    for i in range(0, len(conds)-1):
        temp += ' & \\multicolumn{2}{c}{' + conds[i] + '}'
    print temp + ' \\\\'
    print '\\thickhline'
    for i in range(1, len(conds)):
        temp = str(conds[i]) + ' & '
        for j in range(0, len(conds)-1):
            if i > j:
                p = stats.ttest_ind(eval(conds[i]), eval(conds[j]))[1]*15
                d = cohenns_d(eval(conds[i]), eval(conds[j]))
                if p>=1:
                    p=1
                if p < 0.05:
                    temp += '\\textbf{' + str(round(p, 3)) + '} & \\textbf{' + str(round(d, 3)) + '}'
                else:
                    temp += str(round(p, 3)) + ' & ' + str(round(d, 3))
            else:
                temp +=  " - & - "
            if j < len(conds) -2:
                temp += ' & ' 
            else:
                temp += '\\\\'
        print temp
    print '\\thickhline'
    print '\\end{tabular}'
  
if __name__ == '__main__':
    main()
