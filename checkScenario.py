# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:01:19 2017

@author: lucas
"""

from postTrait_Module import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import scipy.signal as sig
import numpy
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/phri/lucas/scenarios/')
    file_names = root.tk.splitlist(file_names)
    root.destroy()

    for file in file_names:
        TYPE = []
        SUBTYPE = []
        SAME = 0
        ONE1 = 0
        ONE2 = 0
        OPPO = 0
        k = 0
        f = open(file,'r')
        for line in f:
            TYPE.append(int(line[line.find('_TYPE')+6 : line.find("\t_")]))
            SUBTYPE.append(int(line[line.find('_SUBTYPE')+9 : line.find("\n")]))
        for i in range(0, len(TYPE)):
#            print TYPE[i], SUBTYPE[i]
            if TYPE[i] == 3 and k < 32:
                k+=1
                if SUBTYPE[i] == 0 or SUBTYPE[i] == 1:
                    SAME += 1
#                    print "same"
                elif SUBTYPE[i] == 2 or SUBTYPE[i] == 3:
                    ONE1 += 1
                elif SUBTYPE[i] == 4 or SUBTYPE[i] == 5:
                    ONE2 += 1    
#                    print "one"
                elif SUBTYPE[i] == 6 or SUBTYPE[i] == 7:
                    OPPO += 1
#                    print "oppo"
        if SAME == (ONE1+ONE2) == OPPO:
            print file[file.find('SCENARIO_'):file.find('.txt')]
        
        print file[file.find('SCENARIO_'):file.find('.txt')], "\t", SAME, ONE1, ONE2, OPPO


if __name__ == '__main__':
    main()