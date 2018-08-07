# -*- coding: utf-8 -*-
"""
Created on Fri May  5 20:38:33 2017

@author: lucas
"""


from scipy import stats
import numpy as np
import pandas
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
from Tkinter import *
from tkFileDialog import *
from postTrait_Module import *


root = Tk()
root.withdraw()
file_names = askopenfilenames(initialdir = '~/Documents/Manip/')
file_names = root.tk.splitlist(file_names)
root.destroy()

names_dict = {}
for f in file_names:
    end = f.find('.txt')
    month = f[end - 8 :  end - 6]
    day = f[end - 11: end - 9]
    hour = f[end - 5: end - 3]
    minute = f[end - 2: end]
    names_dict[f] = int(month+day+hour+minute)

sortedList = sorted(names_dict.iteritems(), key=lambda (k,v): (v,k))

file_names_sorted = ['']*len(file_names)
for i in range (0, len(file_names)):
    file_names_sorted[i] = sortedList[i][0]
    print file_names_sorted[i]


test1 = 0
test2 = 0
for f in file_names_sorted:
    print f
    c = FileData(f)
    c.getDataFromFile()
    if(test1 == c.Consigne1[25000] and test2 == c.Consigne2[50000]):
        print 'Echec : ' + f
    test1 = c.Consigne1[25000]
    test2 = c.Consigne2[50000]