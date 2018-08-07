#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 09:31:57 2015

@author: roche
"""

from postTrait_Module import *

import os
import wx
import wx.lib.agw.multidirdialog as MDD
import pandas
import matplotlib.pyplot as plt
import numpy as np
import time

def main():
    # Our normal wxApp-derived class, as usual
    app = wx.App(0)
    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath="/home/lucas/Documents/Manip/",  # defaultPath="C:/Users/users/Desktop/",
                             agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)
    
    if dlg.ShowModal() != wx.ID_OK:
        print("You Cancelled The Dialog!")
        dlg.Destroy()
    
    
    paths = dlg.GetPaths()

    dlg.Destroy()
    app.MainLoop()
    
    nbChoicesS1tot = []
    nbChoicesR1tot = []
    nbChoicesS2tot = []
    nbChoicesR2tot = []  
    nameS1tot = []
    nameS2tot = []
    fileTypetot = []
    expeNbtot = []
    
    expe_nb = 0
    
    for path in enumerate(paths):
        directory= path[1].replace('Home directory','/home/lucas')
        print(directory)
        file_names = os.listdir(directory)
    
        file_names_HFO = [x for x in file_names if x.find('_HFO_')!=-1 or x.find('_s_')!=-1]
        file_names_HFOP = [x for x in file_names if x.find('_HFOP_')!=-1 or x.find('_a_')!=-1]
        file_names_HVP = [x for x in file_names if x.find('_HRP_')!=-1 or x.find('_HVP_')!=-1 or x.find('_u_')!=-1]
        file_names_KVP = [x for x in file_names if x.find('_KRP_')!=-1 or x.find('_KVP_')!=-1]
        file_names_ALONE = [x for x in file_names if x.find('_Alone_')!=-1 or x.find('_w_')!=-1]
    #    
        file_names = file_names_HFO + file_names_HFOP + file_names_HVP + file_names_KVP
 

        nbChoicesS1 = []
        nbChoicesR1 = []
        nbChoicesS2 = []
        nbChoicesR2 = []  
        nameS1 = []
        nameS2 = []
        fileType = []
        expeNb = []
        d=0
        
        for file in file_names:
            file = directory + '/' + file
            if file.find('~') != -1:# or f.find('trial_1') != -1:
                d +=1
                continue
            DataClass = FileData(file)
            DataClass.getDataFromFile()
            DataClass.analyzeDominance()
            
            expeNb.append(expe_nb)
            fileType.append(DataClass.fileType)
            nameS1.append(DataClass.SUBJECT_NAME1)
            nameS2.append(DataClass.SUBJECT_NAME2)
            if DataClass.fileType == 'HFOP' or DataClass.fileType == 'HFO' or DataClass.fileType == 'HFOP_mou':
                nbChoicesS1.append(DataClass.nbChoices1)
                nbChoicesS2.append(DataClass.nbChoices2)
                nbChoicesR1.append(0)
                nbChoicesR2.append(0)                
            elif DataClass.fileType == 'HVP' or DataClass.fileType == 'KVP':
                nbChoicesS1.append(DataClass.nbChoicesH1)
                nbChoicesR1.append(DataClass.nbChoicesR1)
                nbChoicesS2.append(DataClass.nbChoicesH2)
                nbChoicesR2.append(DataClass.nbChoicesR2)
                
            

            print file, " analyzed ... "
        expe_nb += 1
        nbChoicesS1tot.extend(nbChoicesS1)
        nbChoicesR1tot.extend(nbChoicesR1)
        nbChoicesS2tot.extend(nbChoicesS2)
        nbChoicesR2tot.extend(nbChoicesR2)  
        nameS1tot.extend(nameS1)
        nameS2tot.extend(nameS2)
        fileTypetot.extend(fileType)
        expeNbtot.extend(expeNb)
        
        

        data = pandas.DataFrame({'EXPE' : expeNb, 'TYPE' : fileType, 'Name1' : nameS1, 'Name2' : nameS2, 'Choices1': nbChoicesS1, 'Choices2': nbChoicesS2, 'Robot1' : nbChoicesR1, 'Robot2' : nbChoicesR2}) 

        plt.figure(data['Name1'][0]+'+'+ data['Name2'][1])
        #HFOP    
        labels = data['Name1'][0], data['Name2'][0]
        sizes = [np.mean(data[data['TYPE']=='HFOP']['Choices1']), np.mean(data[data['TYPE']=='HFOP']['Choices2'])]
        
        ax1 = plt.subplot(321)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #HFO  
        labels = data['Name1'][0], data['Name2'][0]
        sizes = [np.mean(data[data['TYPE']=='HFO']['Choices1']), np.mean(data[data['TYPE']=='HFO']['Choices2'])]
        
        ax2 = plt.subplot(322)
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        #HVP1  
        labels = data['Name1'][0], 'Robot1'
        sizes = [np.mean(data[data['TYPE']=='HVP']['Choices1']), np.mean(data[data['TYPE']=='HVP']['Robot1'])]
        
        ax3 = plt.subplot(323)
        ax3.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
        ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #HVP2  
        labels = data['Name2'][0], 'Robot2'
        sizes = [np.mean(data[data['TYPE']=='HVP']['Choices2']), np.mean(data[data['TYPE']=='HVP']['Robot2'])]
        
        ax4 = plt.subplot(324)
        ax4.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['red', 'green'], startangle=90)
        ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        #KVP1  
        labels = data['Name1'][0], 'Robot1'
        sizes = [np.mean(data[data['TYPE']=='KVP']['Choices1']), np.mean(data[data['TYPE']=='KVP']['Robot1'])]
        
        ax5 = plt.subplot(325)
        ax5.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
        ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #KVP2  
        labels = data['Name2'][0], 'Robot2'
        sizes = [np.mean(data[data['TYPE']=='KVP']['Choices2']), np.mean(data[data['TYPE']=='KVP']['Robot2'])]
        
        ax6 = plt.subplot(326)
        ax6.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['red', 'green'], startangle=90)
        ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        


    datatot = pandas.DataFrame({'EXPE' : expeNbtot, 'TYPE' : fileTypetot, 'Name1' : nameS1tot, 'Name2' : nameS2tot, 'Choices1': nbChoicesS1tot, 'Choices2': nbChoicesS2tot, 'Robot1' : nbChoicesR1tot, 'Robot2' : nbChoicesR2tot}) 

    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)    
    datatot.to_csv('/home/lucas/phri/lucas/fichiers_csv/data_AnDom_' + date + '.csv')

    plt.figure("Total")
    #HFOP    
    labels = 'Sujet 1', 'Sujet 2'
    sizes = [np.mean(datatot[datatot['TYPE']=='HFOP']['Choices1']), np.mean(datatot[datatot['TYPE']=='HFOP']['Choices2'])]
    
    ax1 = plt.subplot(321)
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #HFO  
    labels = 'Sujet 1', 'Sujet 2'
    sizes = [np.mean(datatot[datatot['TYPE']=='HFO']['Choices1']), np.mean(datatot[datatot['TYPE']=='HFO']['Choices2'])]
    
    ax2 = plt.subplot(322)
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #HVP1  
    labels = 'Sujet 1', 'Robot 1'
    sizes = [np.mean(datatot[datatot['TYPE']=='HVP']['Choices1']), np.mean(datatot[datatot['TYPE']=='HVP']['Robot1'])]
    
    ax3 = plt.subplot(323)
    ax3.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #HVP2  
    labels =  'Robot 2','Sujet 2'
    sizes = [ np.mean(datatot[datatot['TYPE']=='HVP']['Robot2']),np.mean(datatot[datatot['TYPE']=='HVP']['Choices2'])]
    
    ax4 = plt.subplot(324)
    ax4.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['red', 'green'], startangle=90)
    ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    #KVP1  
    labels = 'Sujet 1', 'Robot 1'
    sizes = [np.mean(datatot[datatot['TYPE']=='KVP']['Choices1']), np.mean(datatot[datatot['TYPE']=='KVP']['Robot1'])]
    
    ax5 = plt.subplot(325)
    ax5.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
    ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #KVP2  
    labels = 'Robot 2', 'Sujet 2'
    sizes = [np.mean(datatot[datatot['TYPE']=='KVP']['Robot2']), np.mean(datatot[datatot['TYPE']=='KVP']['Choices2'])]
    
    ax6 = plt.subplot(326)
    ax6.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['red', 'green'], startangle=90)
    ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
    plt.show()
        
        

   
    
if __name__ == '__main__':
    main()
    


