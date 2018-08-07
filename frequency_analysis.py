# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:10:51 2017

@author: lucas
"""


import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
from Tkinter import *
from tkFileDialog import *
from params import *
import matplotlib.pyplot as plt
from math import log10
from postTrait_Module import *
import pandas

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip/tests_freq2/')#'/media/NAS/Public/Lucas/OLD_MANIPS/TESTS/tests_freq')
    file_names = root.tk.splitlist(file_names)
    root.destroy()

#    file_names = ["/home/lucas/Documents/Manip/tests_freq2/RESULTS_scenario_101_trial_1_HVP_3N_0.2-5s-60s.txt"]
    freq = []
    gain = []
    plt.figure()
    for file in file_names:  
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        time = DataClass.Time
        pos1 = DataClass.Subj_pos1
        for1 = DataClass.Subj_for1
        cons1 = [(x - 4970)*10/(0.8*10000/2)*0.123/0.082 for x in DataClass.Consigne1]
    
        
        mins1 = []
        maxs1 = []
        t_end = 120
        if DataClass.fileType == "HVP":
            deltaT = 5
            f0 = 0.1
            f_lim = 2
            f_cons = 2*3*0.123/0.082
        elif DataClass.fileType == "HFOP":
            deltaT = 1
            f0 = 1
            f_lim = 0.1
            f_cons = 2*3*0.123/0.082 
        elif DataClass.fileType == "HFO":
            deltaT = 1
            f0 = 60
            f_lim = 0.1
            f_cons = 2*3*0.123/0.082   
        l0 = DataClass.time2line(deltaT)
        lf = DataClass.time2line(t_end)
        maxs1, mins1 = peakdet(for1[l0:lf], 0.5, time[l0:lf])
        maxs1 = [x for x in maxs1 if x[1] > f_lim]
        mins1 = [x for x in mins1 if x[1] < -f_lim]
        
#        print maxs1
#        print mins1
        
        
        t0 = time[l0]
        tf = t0 + deltaT

        k=0
        while(tf <= t_end+0.1):
            moy_min = np.mean([mins1[i][1] for i in  range(0, len(mins1)) if (mins1[i][0] > t0 and mins1[i][0] < tf)])
            moy_max = np.mean([maxs1[i][1] for i in  range(0, len(maxs1)) if (maxs1[i][0] > t0 and maxs1[i][0] < tf)])
            deltaF = moy_max-moy_min
            print t0, tf, moy_min, moy_max, deltaF, 20*np.log10(deltaF/f_cons), (k+1)*f0
            freq.append(round((k+1)*f0,2))
            gain.append(20*np.log10(deltaF/f_cons))
            t0 += deltaT
            tf += deltaT
            k+=1
            

#        print freq
#        print gain

    bode = pandas.DataFrame({'freq' : freq, 'gain' : gain})
    bode_sorted = bode.sort_values('freq')
#    print bode
#    print bode_sorted
    gain_moyenne = []
    freq_moyenne = []
#    print bode_moyenne
    i=0
    somme = 0.
    nb = 0.0
    N = len(bode_sorted['freq'])-1
    while (i < N):
        somme += bode_sorted['gain'].values[i]
        nb += 1.0
        if (round(bode_sorted['freq'].values[i], 2) == round(bode_sorted['freq'].values[i+1], 2)):
            if i!=N:
                i+=1
                continue
            else:
                somme += bode_sorted['gain'].values[i+1]
                gain_moyenne.append(somme/nb)
                freq_moyenne.append(round(bode_sorted['freq'].values[i+1], 2))                
        else:
            gain_moyenne.append(somme/nb)
            freq_moyenne.append(round(bode_sorted['freq'].values[i], 2))
            somme = 0.
            nb=0
            i+=1
        
#    print freq_moyenne
#    print gain_moyenne
    plt.semilogx(freq_moyenne, gain_moyenne)    
    plt.semilogx(freq, gain, 'k+')
    plt.semilogx([0.2, 300],[-3,-3], 'r')
#    ax1.axis([0.2, 200, -23,3])
    plt.xlim([0.2, 200])
    plt.ylim([-23, 3])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.legend(["Mean", "Individual Tests"], loc=0)

    

    plt.show()
 
def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    Returns two arrays
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    % [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    % maxima and minima ("peaks") in the vector V.
    % MAXTAB and MINTAB consists of two columns. Column 1
    % contains indices in V, and column 2 the found values.
    %
    % With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    % in MAXTAB and MINTAB are replaced with the corresponding
    % X-values.
    %
    % A point is considered a maximum peak if it has the maximal
    % value, and was preceded (to the left) by a value lower by
    % DELTA.
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    """
    maxtab = []
    mintab = []
    if x is None:
        x = arange(len(v))
    v = asarray(v)
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    lookformax = True
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
     
    return array(maxtab), array(mintab)
    
    
if __name__ == '__main__':
    main()