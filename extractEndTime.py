# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 16:27:17 2015

@author: lucas
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
    
#    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
#    
#    file_names = file_names_HFOP

    print 'Threshold\tMean\tStd\tMin\tMax'
    for k in range(5,7):
        end_times = []
        for file in file_names:
            if file.find('_r_')!=-1 or file.find('_u_')!=-1 or file.find('_w_')!=-1:
                continue
            DataClass = FileData(file)
            DataClass.getDataFromFile()
            DataClass.threshold_ext = 5*(k+1)*0.8
#            print file
            (tempT) = DataClass.extractEndTime()
            
            end_times.extend(tempT)
            
        mean_end_time = np.mean(end_times)
        end_min_time = min(end_times)
        end_max_time = max(end_times)
        
        YT,XT = np.histogram(end_times, bins=80, range = (0,4))

        for i in range (0, len(YT)):
            Y_hist = DataClass.threshold_ext/0.8
            H_hist = 3.5
            if YT[i]==0:
                continue
            plt.plot([XT[i], XT[i]], [Y_hist, Y_hist + float(YT[i])*H_hist/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
            plt.plot([XT[i], XT[i+1]],[Y_hist + float(YT[i])*H_hist/max(YT), Y_hist + float(YT[i])*H_hist/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
            plt.plot([XT[i+1], XT[i+1]], [Y_hist, Y_hist + float(YT[i])*H_hist/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
        plt.plot([0, 4], [Y_hist, Y_hist], 'k-', linewidth = 1)
        plt.plot(mean_end_time, Y_hist, 'r+',mew=2, ms=12)
        plt.axis([0, 4, 0.0, 30])

        #Extracts the %age of finishedd choice at 0.5+0.05l seconds.
        N= len(end_times)
        lmax = 35
        count = [0]*lmax
        for l in range(0, lmax):
            for i in range(0, N):
                if end_times[i] <= 0.5 + 0.05*l:
                    count[l] += 1      
            count[l] = float(count[l])/N*100
            
        #Computes the time at chich XXX of choices are finished
        N = len(end_times)
        n_max=21
        end_times = np.sort(end_times)
        time_thresh = [0]*n_max
        for l in range(0,n_max):
            pc_thresh = 0.05*l
            l_max = int(pc_thresh*N)
            if l_max == N:
                l_max = N-1
            time_thresh[l] = end_times[l_max]


   
        print DataClass.threshold_ext, '\t', mean_end_time, '\t', np.std(end_times), '\t', count#, '\t', time_thresh

    plt.show()
#    print '\n\n'
#    print thresh_times

if __name__ == '__main__':
    main()  