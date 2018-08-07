# -*- coding: utf-8 -*-
"""
Created on Thu May 11 11:39:55 2017

@author: lucas
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
from Tkinter import *
from tkFileDialog import *
import pandas
import matplotlib.patches as mpatches
from scipy import stats



def plotPie(data, name1, name2):
        fig = plt.figure(name1+'+'+ name2)
        blue_patch = mpatches.Patch(color = 'blue')
        red_patch = mpatches.Patch(color='red')
        green_patch = mpatches.Patch(color='green')
        fig.legend((blue_patch, red_patch, green_patch), (name1, name2, 'Robot'), loc= 8, fontsize = 15)
        
        #HFOP    
        labels = name1, name2
        sizes = [np.mean(data[data['TYPE']=='HFOP']['Choices1']), np.mean(data[data['TYPE']=='HFOP']['Choices2'])]
        
        ax1 = plt.subplot(321)
        ax1.pie(sizes#, labels=labels
        , autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.title.set_text('HFOP')

        #HFO  
        labels = name1, name2
        sizes = [np.mean(data[data['TYPE']=='HFO']['Choices1']), np.mean(data[data['TYPE']=='HFO']['Choices2'])]
        
        ax2 = plt.subplot(322)
        ax2.pie(sizes, autopct='%1.1f%%', colors = ['blue', 'red'], startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax2.title.set_text('HFO')


        #HVP1  
        labels = name1, 'Robot1'
        sizes = [np.mean(data[data['TYPE']=='HVP']['Choices1']), np.mean(data[data['TYPE']=='HVP']['Robot1'])]
        
        ax3 = plt.subplot(323)
        ax3.pie(sizes, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
        ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax3.title.set_text('HVP-1')

        #HVP2  
        labels = 'Robot2', name2
        sizes = [np.mean(data[data['TYPE']=='HVP']['Robot2']), np.mean(data[data['TYPE']=='HVP']['Choices2'])]
        
        ax4 = plt.subplot(324)
        ax4.pie(sizes, autopct='%1.1f%%', colors = ['green','red'], startangle=90)
        ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax4.title.set_text('HVP-2')
        
        #KVP1  
        labels = name1, 'Robot1'
        sizes = [np.mean(data[data['TYPE']=='KVP']['Choices1']), np.mean(data[data['TYPE']=='KVP']['Robot1'])]
        
        ax5 = plt.subplot(325)
        ax5.pie(sizes, autopct='%1.1f%%', colors = ['blue', 'green'], startangle=90)
        ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax5.title.set_text('KVP-1')
        
        #KVP2  
        labels = 'Robot2', name2
        sizes = [np.mean(data[data['TYPE']=='KVP']['Robot2']), np.mean(data[data['TYPE']=='KVP']['Choices2'])]
        
        ax6 = plt.subplot(326)
        ax6.pie(sizes, autopct='%1.1f%%', colors = ['green','red'], startangle=90)
        ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax6.title.set_text('KVP-2')

        plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
        plt.tight_layout()
        

def plotBar(data, name1, name2, nb, cond, sujet1, sujet2):
    global ax
    fig = plt.figure(name1+'+'+ name2,figsize=(10,3))
    blue_patch = mpatches.Patch(color = (0.5, 0.5, 1))
    red_patch = mpatches.Patch(color=(1, 0.5, 0.5))
    green_patch = mpatches.Patch(color=(0.5, 1, 0.5))
    fig.legend((blue_patch, green_patch, red_patch), (name1, name2, 'Virtual Partner'), loc= 8, fontsize = 15)
    
    #HFOP    
    labels = name1, name2
    sizes = [np.mean(data[data['TYPE']==cond][sujet1]), np.mean(data[data['TYPE']==cond][sujet2])]
    stderr = 0#stats.sem(data[data['TYPE']==cond][sujet1])    
    
    ax[nb] = plt.subplot(3,2,nb+1)
    if((cond=='HVP'or cond=='KVP')and(sujet1.find('1')!=-1)):
        ax[nb].title.set_text(cond+'- Leader')
    elif((cond=='HVP'or cond=='KVP')and(sujet1.find('2')!=-1)):
        ax[nb].title.set_text(cond+'- Follower')
    else:
        ax[nb].title.set_text(cond)
    ax[nb].axis([0,1,0,1])
    
    if(sujet1=='Choices1'):
        color1=(0.5, 0.5, 1)
    elif(sujet1=='Choices2'):
        color1=(0.5, 1, 0.5)
    else:
        color1=(1, 0.5, 0.5)
    if(sujet2=='Choices1'):
        color2=(0.5, 0.5, 1)
    elif(sujet2=='Choices2'):
        color2=(0.5, 1, 0.5)    
    else:
        color2=(1, 0.5, 0.5)
    
    value1 = sizes[0]/sum(sizes)
    value2 = sizes[1]/sum(sizes)
    ax[nb].barh(bottom=0, width=value1, height=1, color=color1, xerr=stderr, ecolor='black')
    ax[nb].barh(bottom=0, width=value2, height=1, left=value1, color=color2)
    ax[nb].set_xticks([0,1])
    ax[nb].set_xticklabels([0, 100])
    ax[nb].set_yticks([])
    ax[nb].text(value1/2,0.5, str(round(value1*100,1))+"%", ha='center',va='center')
    ax[nb].text(value1+value2/2,0.5, str(round(value2*100,1))+"%", ha='center',va='center')
    
    plt.subplots_adjust(wspace = 1.5, hspace = 2)
#    plt.tight_layout()

def plotBarAll(data, name1, name2):
    plotBar(data, name1, name2, 0, 'HFOP', 'Choices1', 'Choices2')
    plotBar(data, name1, name2, 1, 'HFO', 'Choices1', 'Choices2')
    plotBar(data, name1, name2, 2, 'HVP', 'Choices1', 'Robot1')
    plotBar(data, name1, name2, 3, 'HVP', 'Robot2', 'Choices2')
    plotBar(data, name1, name2, 4, 'KVP', 'Choices1', 'Robot1')
    plotBar(data, name1, name2, 5, 'KVP', 'Robot2', 'Choices2')    
        
def main():
    global ax
    root = Tk()
    root.withdraw()
    file_name = askopenfilename(initialdir = '~/phri/lucas/fichiers_csv/')
    root.destroy()    
    dataTot = pandas.read_csv(file_name)
    nbTests = max(dataTot['EXPE'])+1
    
    choicesSF = []
    choicesSL = []
    fileType = []
    expe_nb = []
    choicesRF = []
    choicesRL = []
    ax = [0]*6
    
    
    data = [0]*nbTests
    for i in range (0, nbTests):
        data[i] = dataTot[dataTot['EXPE']==i].reset_index()
#        plotBarAll(data[i], data[i]['Name1'][0], data[i]['Name2'][0])
        
        expe_nb.extend(data[i]['EXPE'])
        fileType.extend(data[i]['TYPE'])
        #Leader = subject 1
        if(np.mean(data[i][data[i]['TYPE']=='HFOP']['Choices1']) >= np.mean(data[i][data[i]['TYPE']=='HFOP']['Choices2'])):
            choicesSL.extend(data[i]['Choices1'])
            choicesRL.extend(data[i]['Robot1'])
            choicesSF.extend(data[i]['Choices2'])
            choicesRF.extend(data[i]['Robot2'])
        else:
            choicesSL.extend(data[i]['Choices2'])
            choicesRL.extend(data[i]['Robot2'])
            choicesSF.extend(data[i]['Choices1'])
            choicesRF.extend(data[i]['Robot1']) 
            
#    plotPie(dataTot, 'Sujet 1', 'Sujet 2')
    plotBarAll(dataTot, 'Sujet 1', 'Sujet 2')
    
    print "Sujet1 vs Sujet 2 HFOP", stats.ttest_rel(dataTot[dataTot['TYPE']=='HFOP']['Choices1'], dataTot[dataTot['TYPE']=='HFOP']['Choices2'])
    print "Sujet1 vs Sujet 2 HFO", stats.ttest_rel(dataTot[dataTot['TYPE']=='HFO']['Choices1'], dataTot[dataTot['TYPE']=='HFO']['Choices2'])
            
    
    dataTotRecomp = pandas.DataFrame({'EXPE' : expe_nb, 'TYPE' : fileType, 'Choices1': choicesSL, 'Choices2': choicesSF, 'Robot1' : choicesRL, 'Robot2' : choicesRF}) 
    
#    plotPie(dataTotRecomp, 'Leader', 'Follower')    
    plotBarAll(dataTotRecomp, 'Leader', 'Follower') 
    
    S1_HVP= dataTotRecomp[dataTotRecomp['TYPE']=='HVP']['Choices1']
    S1_HFOP= dataTotRecomp[dataTotRecomp['TYPE']=='HFOP']['Choices1']
    S1_HFO= dataTotRecomp[dataTotRecomp['TYPE']=='HFO']['Choices1']
    S1_KVP= dataTotRecomp[dataTotRecomp['TYPE']=='KVP']['Choices1']
    S2_HVP= dataTotRecomp[dataTotRecomp['TYPE']=='HVP']['Choices2']
    S2_HFOP= dataTotRecomp[dataTotRecomp['TYPE']=='HFOP']['Choices2']
    S2_HFO= dataTotRecomp[dataTotRecomp['TYPE']=='HFO']['Choices2']
    S2_KVP= dataTotRecomp[dataTotRecomp['TYPE']=='KVP']['Choices2']
    R1_HVP= dataTotRecomp[dataTotRecomp['TYPE']=='HVP']['Robot1']
    R1_KVP= dataTotRecomp[dataTotRecomp['TYPE']=='KVP']['Robot1']
    R2_HVP= dataTotRecomp[dataTotRecomp['TYPE']=='HVP']['Robot2']
    R2_KVP= dataTotRecomp[dataTotRecomp['TYPE']=='KVP']['Robot2']

    print "\n"
    print "Leader vs Follower HFOP", stats.ttest_rel(S1_HFOP, S2_HFOP), cohenns_d(S1_HFOP, S2_HFOP)
    print "Leader vs Robot HVP", stats.ttest_rel(S1_HVP, R1_HVP), cohenns_d(S1_HVP, R1_HVP)
    print "Leader vs Robot KVP", stats.ttest_rel(S1_KVP, R1_KVP), cohenns_d(S1_KVP, R1_KVP)
    print "Follower vs Robot HVP", stats.ttest_rel(S2_HVP, R2_HVP), cohenns_d(S2_HVP, R2_HVP)
    print "Follower vs Robot KVP", stats.ttest_rel(S2_KVP, R2_KVP), cohenns_d(S2_KVP, R2_KVP)
    print "\n"
    print "Leader, HFOP vs HVP", stats.ttest_ind(S1_HFOP, S1_HVP), cohenns_d(S1_HFOP, S1_HVP)
    print "Leader, HFOP vs KVP", stats.ttest_ind(S1_HFOP, S1_KVP), cohenns_d(S1_HFOP, S1_KVP)
    print "Leader, KVP vs HVP", stats.ttest_ind(S1_KVP, S1_HVP), cohenns_d(S1_KVP, S1_HVP)
    print "\n"
    print "Follower, HFOP vs HVP", stats.ttest_ind(S2_HFOP, S2_HVP), cohenns_d(S2_HFOP, S2_HVP)
    print "Follower, HFOP vs KVP", stats.ttest_ind(S2_HFOP, S2_KVP), cohenns_d(S2_HFOP, S2_KVP)
    print "Follower, KVP vs HVP", stats.ttest_ind(S2_KVP, S2_HVP), cohenns_d(S2_KVP, S2_HVP)
    print "\n"
    print "Leader vs Follower HFOP", stats.ttest_rel(S1_HFOP, S2_HFOP), cohenns_d(S1_HFOP, S2_HFOP)
    print "Leader vs Follower HFO", stats.ttest_rel(S1_HFO, S2_HFO), cohenns_d(S1_HFO, S2_HFO)
    print "Leader, HFOP vs HFO", stats.ttest_ind(S1_HFOP, S1_HFO), cohenns_d(S1_HFOP, S1_HFO)
    print "Follower, HFOP vs HFO", stats.ttest_ind(S2_HFOP, S2_HFO), cohenns_d(S2_HFOP, S2_HFO)
    
    plt.figure('Stats')
    ax1 = plt.subplot(111)

    cell_text=[["Sujet1 vs Sujet 2 HFOP", stats.ttest_rel(dataTot[dataTot['TYPE']=='HFOP']['Choices1'], dataTot[dataTot['TYPE']=='HFOP']['Choices2'])[0], stats.ttest_rel(dataTot[dataTot['TYPE']=='HFOP']['Choices1'], dataTot[dataTot['TYPE']=='HFOP']['Choices2'])[1]],
              ["Sujet1 vs Sujet 2 HFO",stats.ttest_rel(dataTot[dataTot['TYPE']=='HFO']['Choices1'], dataTot[dataTot['TYPE']=='HFO']['Choices2'])[0], stats.ttest_rel(dataTot[dataTot['TYPE']=='HFO']['Choices1'], dataTot[dataTot['TYPE']=='HFO']['Choices2'])[1]],
              ["","",""],
              ["Leader vs Follower HFOP", stats.ttest_rel(S1_HFOP, S2_HFOP)[0], stats.ttest_rel(S1_HFOP, S2_HFOP)[1]],
              ["Leader vs Robot HVP", stats.ttest_rel(S1_HVP, R1_HVP)[0], stats.ttest_rel(S1_HVP, R1_HVP)[1]],
              ["Leader vs Robot KVP", stats.ttest_rel(S1_KVP, R1_KVP)[0], stats.ttest_rel(S1_KVP, R1_KVP)[1]],
              ["Follower vs Robot HVP", stats.ttest_rel(S2_HVP, R2_HVP)[0], stats.ttest_rel(S2_HVP, R2_HVP)[1]],
              ["Follower vs Robot KVP", stats.ttest_rel(S2_KVP, R2_KVP)[0], stats.ttest_rel(S2_KVP, R2_KVP)[1]],
              ["","",""],
              ["Leader, HFOP vs HVP", stats.ttest_ind(S1_HFOP, S1_HVP)[0], stats.ttest_ind(S1_HFOP, S1_HVP)[1]],
              ["Leader, HFOP vs KVP", stats.ttest_ind(S1_HFOP, S1_KVP)[0], stats.ttest_ind(S1_HFOP, S1_KVP)[1]],
              ["Leader, KVP vs HVP", stats.ttest_ind(S1_KVP, S1_HVP)[0], stats.ttest_ind(S1_KVP, S1_HVP)[1]],
              ["","",""],
              ["Follower, HFOP vs HVP", stats.ttest_ind(S2_HFOP, S2_HVP)[0], stats.ttest_ind(S2_HFOP, S2_HVP)[1]],
              ["Follower, HFOP vs KVP", stats.ttest_ind(S2_HFOP, S2_KVP)[0], stats.ttest_ind(S2_HFOP, S2_KVP)[1]],
              ["Follower, KVP vs HVP", stats.ttest_ind(S2_KVP, S2_HVP)[0], stats.ttest_ind(S2_KVP, S2_HVP)[1]]]
     

    ax1.axis('off')
    ax1.axis('tight')
    coll_labels=('Test', 't value', 'p value')
    stats_table = ax1.table(cellText = cell_text, colLabels=coll_labels, loc='center')
    for i in range(0, len(cell_text)):
        if cell_text[i][2] < 0.05:
            stats_table.get_celld()[(i+1,2)]._text.set_color('g')
        else:
            stats_table.get_celld()[(i+1,2)]._text.set_color('r')
    
    plt.show()

def cohenns_d(group1, group2):
    return (np.mean(group1)-np.mean(group2))/np.sqrt(0.5*(np.std(group1)+np.std(group2)))

if __name__ == '__main__':
    main()