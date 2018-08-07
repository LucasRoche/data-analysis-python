# -*- coding: utf-8 -*-

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '../results')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
    
    file_names = file_names_HFO + file_names_HFOP

    expectedChoicesTotal = []
    finalChoicesTotal = []
    thresh_times = []
        

    print "StartTime\tStopTime\tTimer\tThreshold\tAccuracy"   

    for j in range (0, 5): #start
        for k in range(2,3): #stop
            for l in range(0,1): #timer
                for m in range(0,5): #thresh
                    expectedChoicesTotal = []
                    finalChoicesTotal = []
                    thresh_times = []
                    for file in file_names:
                        DataClass = FileData(file)
                        DataClass.getDataFromFile()
                        if DataClass.fileType == 'HFO':
                            continue
                        DataClass.analysisStartTime = 0.2 + j*0.1
                        DataClass.analysisStopTime = 0.7 + k*0.1
                        DataClass.timerMax = 0.1*l
                        DataClass.threshold = 5*(m+1)
                        (tempE, tempF, tempT) = DataClass.intentionDetectionSTXM()
                        
                        expectedChoicesTotal.extend(tempE)
                        finalChoicesTotal.extend(tempF)
                        thresh_times.extend(tempT)
        
                    mean_thresh_time = np.mean(thresh_times)
                    thresh_min_time = min(thresh_times)
                    thresh_max_time = max(thresh_times)
                    
                    N =  len(finalChoicesTotal)               
                    results = [0]*N
                    
                    for i in range (0, N):
                        results[i] = expectedChoicesTotal[i] * finalChoicesTotal[i]
                
                    somme = float(sum(results))
                    size = float(len(results))            
                    good = (somme+size)/2
                    
                    thresh_times_true = []
                    thresh_times_false = []
                    for i in range (0, N):
                        if results[i] == 1:
                            thresh_times_true.append(thresh_times[i])
                        elif results[i] == -1:
                            thresh_times_false.append(thresh_times[i])
                    
                    YT,XT = np.histogram(thresh_times_true, bins=40, range = (0,2))
                    YF,XF = np.histogram(thresh_times_false, bins=40, range = (0,2))
                    
                             
                    plt.figure(DataClass.threshold)
                    for i in range (0, len(YT)):
                        plt.plot([XT[i], XT[i]], [0.2+0.1*j, 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-')
                        plt.plot([XT[i], XT[i+1]],[0.2+0.1*j + float(YT[i])*0.05/max(YT), 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-')
                        plt.plot([XT[i+1], XT[i+1]], [0.2+0.1*j, 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-')
                        plt.plot([XF[i], XF[i]], [0.2+0.1*j, 0.2+0.1*j - float(YF[i])*0.05/max(YT)], 'r-')
                        plt.plot([XF[i], XF[i+1]],[0.2+0.1*j -float(YF[i])*0.05/max(YT), 0.2+0.1*j -float(YF[i])*0.05/max(YT)], 'r-')
                        plt.plot([XF[i+1], XF[i+1]], [0.2+0.1*j, 0.2+0.1*j - float(YF[i])*0.05/max(YT)], 'r-')
                        plt.plot([0, 2], [0.2+0.1*j, 0.2+0.1*j], 'k-', linewidth = 1)
                    plt.plot(mean_thresh_time, 0.2 + j*0.1, 'k+', markersize = 12)
                    plt.axis([0,2.1,0.1,0.7])
            
                    count_095 = 0.0
                    count_100 = 0.0           
                    for i in range(0, N):
                        if thresh_times[i] >= 0.95:
                            count_095 += 1
                        if thresh_times[i] >= 1.0:
                            count_100 += 1
                    count_095 = float(count_095)/N*100
                    count_100 = float(count_100)/N*100
                    
                    print DataClass.analysisStartTime, '\t', DataClass.analysisStopTime, '\t', DataClass.timerMax, "\t", DataClass.threshold, "\t", good/size*100, "\t",mean_thresh_time, "\t",thresh_min_time, "\t",thresh_max_time, "\t",count_095, "\t",count_100

    plt.show()
#    print '\n\n'
#    print thresh_times

if __name__ == '__main__':
    main()  