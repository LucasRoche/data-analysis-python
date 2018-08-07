# -*- coding: utf-8 -*-

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *
import os
import wx
import wx.lib.agw.multidirdialog as MDD
import numpy as np

def main():
#    root = Tk()
#    root.withdraw()
#    file_names = askopenfilenames(initialdir = '/media/NAS/Public/Lucas/OLD_MANIPS/')
#    file_names_total = root.tk.splitlist(file_names)
#    root.destroy()
    
    app = wx.App(0)
    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/media/NAS/Public/Lucas/",  # defaultPath="C:/Users/users/Desktop/",
                             agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)
    
    if dlg.ShowModal() != wx.ID_OK:
        print("You Cancelled The Dialog!")
        dlg.Destroy()
    
    
    paths = dlg.GetPaths()

    dlg.Destroy()
    app.MainLoop()
    
    file_names_total =[]
    
    for path in enumerate(paths):
        directory= path[1].replace('Home directory','/home/lucas')
        print(directory)
        file_names = os.listdir(directory)
            #    
        
        for file in file_names:
            file = directory + '/' + file
            file_names_total.append(file)
    

    expectedChoicesTotal = []
    finalChoicesTotal = []
    thresh_times = []
        

    print "Threshold\tStartingTime\tStopTime\tSize\taveragetime\tAccuracy\tunknown\ttrueAcc"   

    for k in range (6,7):
        for j in range(1,2):
            for l in range(40,45):
                expectedChoicesTotal = []
                finalChoicesTotal = []
                thresh_times = []
                end_times = []
#    fileType = []
                for file in file_names_total:
                    DataClass = FileData(file)
                    DataClass.getDataFromFile()
                    if DataClass.fileType != 'HFOP' or file.find('~')!=-1:
                        continue
                    DataClass.threshold = 5*(k+1)*0.8
                    DataClass.analysisStartTime = 0.2 + j*0.1
    #                print DataClass.threshold, DataClass.analysisStartTime
                    DataClass.threshold_ext = 0.1*80
                    (tempE, tempF, tempT, tempET) = DataClass.intentionDetectionST()
                    
                    expectedChoicesTotal.extend(tempE)
                    finalChoicesTotal.extend(tempF)
                    thresh_times.extend(tempT)
                    end_times.extend(tempET)
                    
                mean_thresh_time = np.mean(thresh_times)
                thresh_min_time = min(thresh_times)
                thresh_max_time = max(thresh_times)
                
                N =  len(finalChoicesTotal) 
                print len(finalChoicesTotal), len(thresh_times), len(end_times)
                diff = []
                for i in range (0, N):
                    try:
                        diff.append(end_times[i] - thresh_times[i])
                    except:
                        print i
    #            
                results = [0]*N
                unknown=0
                
    
                
                for i in range (0, N):
    #                print expectedChoicesTotal[i], "\t",finalChoicesTotal[i], "\t",thresh_times[i]
                    if thresh_times[i] > 0.5 + l*0.05:
                        unknown +=1
                    else:
                        results[i] = expectedChoicesTotal[i] * finalChoicesTotal[i]
                    
                
            
                somme = float(sum(results))
                size = float(len(results))            
                good = (somme+size)/2
                
    #            thresh_times_true = []
    #            thresh_times_false = []
    #            for i in range (0, N):
    #                if results[i] == 1:
    #                    thresh_times_true.append(thresh_times[i])
    #                elif results[i] == -1:
    #                    thresh_times_false.append(thresh_times[i])
    #            
    #            YT,XT = np.histogram(thresh_times_true, bins=40, range = (0,2))
    #            YF,XF = np.histogram(thresh_times_false, bins=40, range = (0,2))
    #            
    #            
    ##            thresh_times = numpy.sort(thresh_times)            
    #            plt.figure(DataClass.threshold)
    ##            for i in range(0, N):
    ##                if results[i] == 1:
    ##                    plt.plot(thresh_times[i], 0.2+j*0.1, 'g+')
    ##                elif results[i] == -1:
    ##                    plt.plot(thresh_times[i], 0.2+j*0.1, 'r+')
    ##            plt.plot(thresh_times, [0.2 + j*0.1]*len(thresh_times), 'b+')
    #            for i in range (0, len(YT)):
    #                if YT.all() == 0 and YF.all() == 0:
    #                    continue
    #                plt.plot([XT[i], XT[i]], [0.2+0.1*j, 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
    #                plt.plot([XT[i], XT[i+1]],[0.2+0.1*j + float(YT[i])*0.05/max(YT), 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
    #                plt.plot([XT[i+1], XT[i+1]], [0.2+0.1*j, 0.2+0.1*j + float(YT[i])*0.05/max(YT)], 'g-', linewidth = 2, solid_capstyle="round")
    #                plt.plot([XF[i], XF[i]], [0.2+0.1*j, 0.2+0.1*j - float(YF[i])*0.05/max(YT)], 'r-', linewidth = 2, solid_capstyle="round")
    #                plt.plot([XF[i], XF[i+1]],[0.2+0.1*j -float(YF[i])*0.05/max(YT), 0.2+0.1*j -float(YF[i])*0.05/max(YT)], 'r-', linewidth = 2, solid_capstyle="round")
    #                plt.plot([XF[i+1], XF[i+1]], [0.2+0.1*j, 0.2+0.1*j - float(YF[i])*0.05/max(YT)], 'r-', linewidth = 2, solid_capstyle="round")
    #            plt.plot([0, 2], [0.2+0.1*j, 0.2+0.1*j], 'k-', linewidth = 1)
    #            plt.plot(mean_thresh_time, 0.2 + j*0.1, 'k+', markersize = 12)
    #            plt.axis([0,2.1,0.1,0.7])
    #
    #            count_095 = 0.0
    #            count_100 = 0.0           
    #            for i in range(0, N):
    #                if thresh_times[i] >= 0.95:
    #                    count_095 += 1
    #                if thresh_times[i] >= 1.0:
    #                    count_100 += 1
    #            count_095 = float(count_095)/N*100
    #            count_100 = float(count_100)/N*100
                accuracy = good/size*100
                if unknown != size:
                    true_accuracy = ((2*size*good/size - size)+ (size-unknown))/(2*(size-unknown))*100
                else:
                    true_accuracy = 'NAN'
                
                print 5*(k+1), "\t", 0.2 + j*0.1,  "\t", 0.5 + l*0.05, "\t" ,size, "\t",mean_thresh_time,  "\t", accuracy, "\t", unknown/size*100, "\t", true_accuracy, "\t", good , "\t", unknown, np.mean(diff), np.std(diff), min(diff), max(diff) #, "\t",thresh_min_time, "\t",thresh_max_time, "\t",count_095, "\t",count_100

    plt.show()
#    print '\n\n'
#    print thresh_times

if __name__ == '__main__':
    main()  