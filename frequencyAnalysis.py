# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:32:56 2015

@author: roche
"""
import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
from Tkinter import *
from tkFileDialog import *
from params import *
import matplotlib.pyplot as plt
from math import log10

def main():
    root = Tk()
    root.withdraw()
    dataFile = askopenfilename(initialdir = '../results/TESTS')
    root.destroy()

    R = 0.068
    r = 0.005
    w = 2*3.14159*5
    km = 0.0234
    A = 0.15*0.208
    J_theo = 1.8e-04 
    
    f = open(dataFile, 'r')
  
    time = []  
    pos1 = []
    pos2 = []    
    k=0    
    for line in f:
        lineRead= line[0:line.find("\n")]
        if lineRead.find("ROBOT TIME") != -1:
            k =1
            continue
        if k==1 and line == "\n":
            k=2
            continue
        if k ==2:
            dataList = lineRead.split("\t")
            time.append(float(dataList[0]))
            pos1.append(float(dataList[3])*r/R)
            pos2.append(float(dataList[4])*r/R)

    f.close()
    
    mins1 = []
    maxs1 = []
    maxs1, mins1 = peakdet(pos1, 1)

    min_moy1 = 0
    for k in range (0, len(mins1)):
        min_moy1 += mins1[k][1]
    min_moy1 = min_moy1/len(mins1)
 
    max_moy1 = 0
    for k in range (0, len(maxs1)):
        max_moy1 += maxs1[k][1]
    max_moy1 = max_moy1/len(maxs1)
    
    mins2 = []
    maxs2 = []
    maxs2, mins2 = peakdet(pos2, 1)

    min_moy2 = 0
    for k in range (0, len(mins2)):
        min_moy2 += mins2[k][1]
    min_moy2 = min_moy2/len(mins2)
 
    max_moy2 = 0
    for k in range (0, len(maxs2)):
        max_moy2 += maxs2[k][1]
    max_moy2 = max_moy2/len(maxs2)
   
    ecart1 =  max_moy1 - min_moy1
    ecart2 = max_moy2 - min_moy2
    ecart1 = ecart1/4000.*2*3.14159
    ecart2 = ecart2/4000.*2*3.14159
      
    
    C = A*R*km/(r*w**2)
    J1 = C/(ecart1/2)
    J2 = C/(ecart2/2)
    
    print ecart1, ecart2, J1, J2, J1/(0.102*0.102), J2/(0.102*0.102)


    periode_max_1 = [0]*min(len(maxs1), len(mins1))
    freq_max_1 = [0]*min(len(maxs1), len(mins1))
    
    vect_ecart1 = [0]*min(len(maxs1), len(mins1))
    vect_J = [0]*min(len(maxs1), len(mins1))
    
    vect_cible1 = [0]*min(len(maxs1), len(mins1))
    bode = [0]*min(len(maxs1), len(mins1))
    t = [0]*min(len(maxs1), len(mins1))
    freq = [0]*min(len(maxs1), len(mins1))
   
    for k in range (0, min(len(maxs1), len(mins1))):
        vect_ecart1[k] = maxs1[k][1] - mins1[k][1]
        vect_ecart1[k] = vect_ecart1[k]/4000.*2*3.14159
        
        t[k] = time[int(maxs1[k][0])]
        
        periode_max_1[k] = time[int(maxs1[k][0])] - time[int(maxs1[k-1][0])]
        freq_max_1[k] = 1/periode_max_1[k]
#        if freq_max_1[k] < 1:
#            freq_max_1[k] = 1
#        if freq_max_1[k]  > 1.5*freq_max_1[k-1]:
#            freq_max_1[k]  = freq_max_1[k-1]
#        if freq_max_1[k] < 1:
#            freq_max_1[k] = 1
        if dataFile.find('INERTIE') != -1:
            freq[k] = 5
            
        elif dataFile.find('RMP30') != -1:
            if t[k] < 250:
                freq[k] = int((t[k]-0)/5)*0.2
            elif t[k] >= 250 and t[k] < 350 :
                freq[k] = 10 + int((t[k]-250)/5)*1
            elif t[k] >= 350 and t[k] < 420 :
                freq[k] = 30 + int((t[k]-350)/5)*5
            elif t[k] >=420 :
                freq[k] = 200            
        else:
            if t[k] < 250:
                freq[k] = int((t[k]-0)/5)*0.2
            elif t[k] >= 250 and t[k] < 300 :
                freq[k] = 10 + int((t[k]-250)/5)*1
            elif t[k] >= 300 and t[k] < 380 :
                freq[k] = 20 + int((t[k]-300)/5)*5
            elif t[k] >=380 :
                freq[k] = 200
            
            
        w = max(1, 2*3.14159*freq[k])
        C = A*R*km/(r*w**2)
        vect_J[k] = C/(vect_ecart1[k]/2)        
       
        
        vect_cible1[k] =  R*km*A/(r*J_theo*w**2)*2
        
        if dataFile.find('PID') != -1:
            vect_cible1[k] =  float(dataFile[dataFile.find('PID-')+4:dataFile.find('PID-')+7])/4000*2*3.14159
        elif dataFile.find('TELE') != -1:
            vect_cible1[k] = 150./4000*2*3.14159
                
        
        bode[k] = 20*log10(abs(vect_ecart1[k]/vect_cible1[k]))
        
        
    plt.figure(1)
    plt.plot(t, freq_max_1)
    plt.plot(t, freq)
    plt.title('frequence')
    plt.figure(2)
    plt.plot(t, vect_ecart1)
    plt.plot(t, vect_cible1)
    plt.axis([0,400,0,10])
    plt.title('amplitude')
    plt.figure(3)
    plt.plot(t, vect_J)
    plt.axis([0,400,0,0.005])
    plt.title('inertie')
    plt.figure(4)
#    plt.plot(freq_max_1, bode)
    plt.plot(freq, bode)
    plt.title('Bode Diagram')
    plt.ylabel('Gain (dB)')
    plt.xlabel('Frequency (Hz)')

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