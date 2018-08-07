#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:41:14 2017

@author: lucas
"""

from scipy import stats
from Tkinter import *
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
from tkFileDialog import *
import pandas
from postTrait_Module import *
from statsmodels.graphics.gofplots import qqplot
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import statsmodels.api as sm
import pyvttbl as pt

class GUI_Class:
    
    def __init__(self, master):
        
        self.master = master
        
        self.frameTOP = Frame(master)
        self.frameTOP.grid(row=0,column=0)
        self.frameMIDDLE = Frame(master)
        self.frameMIDDLE.grid(row=1,column=0)
        self.frameBOT = Frame(master)
        self.frameBOT.grid(row=2, column=0)
        
        self.heightTextZone = 1
        self.textZone = Text(self.frameTOP, height = self.heightTextZone, width = 100)
        self.textZone.grid(row = 0, columnspan = 8, padx=5, pady = 5)
        
        
        self.buttonAddFiles = Button(self.frameMIDDLE, text = 'SelectFile', command = self.addFiles, width = 12)
        self.buttonAddFiles.grid(row = 0, column = 0)
        
        self.buttonLoadData = Button(self.frameMIDDLE, text = 'Load Data', command = self.onLoad, width = 12)
        self.buttonLoadData.grid(row = 0, column = 1)
        self.buttonLoadData.config(state = DISABLED)

        self.buttonProcess = Button(self.frameMIDDLE, text = 'Process Files', command = self.process, width = 12)
        self.buttonProcess.grid(row = 0, column = 2)
        self.buttonProcess.config(state=DISABLED)

        self.buttonClearFigures = Button(self.frameMIDDLE, text = 'Clear Figures', command = self.clearFigures, width = 12)
        self.buttonClearFigures.grid(row = 0, column = 3)

        self.buttonShow = Button(self.frameMIDDLE, text = 'Block Figures', command = self.show, width = 12)
        self.buttonShow.grid(row = 0, column = 4)
        
        self.nbTests = 0
        self.loaded = 1
        self.nbFig = 0
        

    def addFiles(self):
        self.file = askopenfilename(initialdir = "../../lucas/fichiers_csv/")
        if self.file:
            self.textZone.delete(1.0,END)
            self.textZone.insert(END, self.file)
            self.buttonLoadData.config(state=NORMAL)
            self.buttonProcess.config(state=NORMAL)
            self.loaded = 0


    def process(self):
        self.file = self.file.encode('ascii','ignore')
        while(1):
            try:
                self.file.remove('')
            except:
                break
        self.processFiles()

    def onLoad(self):
        self.loadData()
        self.displayCheckBoxes()
        
    def loadData(self):
        self.data = pandas.read_csv(self.file, index_col=0)
        self.nbTests = max(self.data['TEST_NUMBER'])


    def displayCheckBoxes(self):
        for child in self.frameBOT.winfo_children():
            child.destroy()    
        self.checkBoxTrials = [0]*self.nbTests
        self.checkBoxTrialsVar = [0]*self.nbTests
        self.labelTrials = [0]*self.nbTests
        
        
        self.labelTrial = Label(self.frameBOT, text = 'Expe :').grid(row = 0, column = 0)
        
        for i in range(0, self.nbTests):
            self.labelTrials[i] = Label(self.frameBOT, text =str(i+1)).grid(row=0, column = i+1)
            self.checkBoxTrialsVar[i] = IntVar()
            self.checkBoxTrials[i]=Checkbutton(self.frameBOT, variable = self.checkBoxTrialsVar[i])
            self.checkBoxTrials[i].grid(row=1, column = i+1)
            self.checkBoxTrials[i].select()

        self.buttonCheckAll = Button(self.frameBOT, text = 'All', command = self.checkAll, width = 4)
        self.buttonCheckAll.grid(row=0, column = self.nbTests +2, padx = 5)
        self.buttonUncheckAll = Button(self.frameBOT, text = 'None', command = self.uncheckAll, width = 4)
        self.buttonUncheckAll.grid(row=1, column = self.nbTests +2, padx = 5)
        
        self.labelTrialsSelected = Label(self.frameBOT, text = 'Trials :')
        self.labelTrialsSelected.grid(row = 0, column = self.nbTests + 3, padx = 10)
        self.trialsSelectedVar = StringVar()
        self.trialsSelectedVar.set('ALL')
        self.trialsSelectedMenu = Menubutton(self.frameBOT, textvariable=self.trialsSelectedVar, relief=RAISED, width = 6)
        self.trialsSelectedMenu.menu  =  Menu ( self.trialsSelectedMenu, tearoff = 0 )
        self.trialsSelectedMenu["menu"]  =  self.trialsSelectedMenu.menu
        self.trialsSelectedMenu.menu.add_command(label = 'ALL', command = self.setALL)
        self.trialsSelectedMenu.menu.add_command(label = '1', command = self.setONE)
        self.trialsSelectedMenu.menu.add_command(label = '2', command = self.setTWO)
        self.trialsSelectedMenu.grid(row = 1, column = self.nbTests + 3, padx = 10)

        self.labelMeasureSelected = Label(self.frameBOT, text = 'Measure :')
        self.labelMeasureSelected.grid(row = 0, column = self.nbTests + 4, padx = 10)
        self.measureSelectedVar = StringVar()
        self.measureSelectedVar.set('RMS')
        self.measureSelectedMenu = Menubutton(self.frameBOT, textvariable=self.measureSelectedVar, relief=RAISED, width = 6)
        self.measureSelectedMenu.menu  =  Menu ( self.measureSelectedMenu, tearoff = 0 )
        self.measureSelectedMenu["menu"]  =  self.measureSelectedMenu.menu
        self.measureSelectedMenu.menu.add_command(label = 'RMS', command = self.setRMS)
        self.measureSelectedMenu.menu.add_command(label = 'PERFS', command = self.setPERFS)
        self.measureSelectedMenu.menu.add_command(label = 'MAP', command = self.setMAP)
        self.measureSelectedMenu.menu.add_command(label = 'FOM', command = self.setFOM)
        self.measureSelectedMenu.grid(row = 1, column = self.nbTests + 4, padx = 10)
        
    def checkAll(self):
        for i in range (0, self.nbTests):
            self.checkBoxTrials[i].select()
    def uncheckAll(self):
        for i in range (0, self.nbTests):
            self.checkBoxTrials[i].deselect()     
            
    def setALL(self):
        self.trialsSelectedVar.set('ALL')       
    def setONE(self):
        self.trialsSelectedVar.set('ONE')  
    def setTWO(self):
        self.trialsSelectedVar.set('TWO')
    def setRMS(self):
        self.measureSelectedVar.set('RMS')
    def setPERFS(self):
        self.measureSelectedVar.set('PERFS') 
    def setMAP(self):
        self.measureSelectedVar.set('MAP') 
    def setFOM(self):
        self.measureSelectedVar.set('FOM') 
        
    def clearFigures(self):
        for i in range(0, self.nbFig):
            plt.close(i)
        self.nbFig = 0
        
    def show(self):
        plt.show(block=True)

    def processFiles(self):
        global HFOP, HFO, ALONE, HVP, KVP, ROBOT, SAME, ONE, OPPO, ALONE_SAME, ALONE_SAME, ALONE_ONE,ALONE_OPPO, HFO_SAME, HFO_ONE, HFO_OPPO, HFOP_SAME, HFOP_ONE, HFOP_OPPO, HVP_SAME, HVP_ONE, HVP_OPPO, KVP_SAME, KVP_ONE, KVP_OPPO, ROBOT_SAME, ROBOT_ONE, ROBOT_OPPO
        global SAME2, SAME3, ONE2, ONE3, OPPO2, OPPO3
        self.loadData()
        
        plt.ion()
        plt.show()

        #remove unwanted trials
        if self.trialsSelectedVar.get() == 'ONE':
            self.data = self.data[self.data['TRIAL_NUMBER'] == 1]
        elif self.trialsSelectedVar.get() == 'TWO':
            self.data = self.data[self.data['TRIAL_NUMBER'] == 2]
            
        #select studied measure
        measure = self.measureSelectedVar.get()
        
        #remove unwanted tests
        for i in range(0, self.nbTests):
            if self.checkBoxTrialsVar[i].get() == 0:
                self.data = self.data[self.data['TEST_NUMBER']!=i+1]        
        #Remove outliers in data (generally SAME trials where both subjects want the wrong way)
        self.data = self.data.drop(self.data[self.data['RMS']> np.mean(self.data['RMS'])+3.5*np.std(self.data['RMS'])].index)        
        self.data = self.data.drop(self.data[self.data['RMS']> 100].index) 
        self.data = self.data.drop(self.data[(self.data['TYPE']=='ALONE') & ((self.data['TRIAL_NUMBER']==1 )| (self.data['TRIAL_NUMBER']==2))].index)     
        
        self.data = self.data.reset_index(drop=True)
        print self.data        
        #Calculate performances and add them to the self.dataFrame
        N = len(self.data['RMS'])
        PERFS = [0]*N
        RMSmax = max(self.data['RMS'])
        for i in range(0, N):
            PERFS[i] = 1 - self.data['RMS'][i]/RMSmax
        
        self.data['PERFS'] = PERFS #pandas.Series(PERFS, index = self.data.index)
        
        print self.data
#        print "HFOP_mou :\t", np.mean(self.data[self.data['TYPE'] == 'HFOP_mou'][measure]) , "\t(" , np.std(self.data[self.data['TYPE'] == 'HFOP_mou'][measure]), ")"
        
        if measure == 'PERFS':
            pix_to_mm = 1
            roundVar = 0
        else:
            pix_to_mm = 0.0125/80.*2*3.14159*0.08*1000.
            roundVar = 1

        
        #Get RMS values for each subcategory (3 TYPES and 3 TRIALS)
        HFOP = self.data[self.data['TYPE'] == 'HFOP'][measure]*pix_to_mm
        HFO = self.data[self.data['TYPE'] == 'HFO'][measure]*pix_to_mm
        ALONE = self.data[self.data['TYPE'] == 'ALONE'][measure]*pix_to_mm
        HVP = self.data[self.data['TYPE'] == 'HVP'][measure]*pix_to_mm
        KVP = self.data[self.data['TYPE'] == 'KVP'][measure]*pix_to_mm
        ROBOT = self.data[self.data['TYPE'] == 'ROBOT'][measure]*pix_to_mm
#        HFOP_mou = self.data[self.data['TYPE'] == 'HFOP_mou'][measure]*pix_to_mm
        SAME = self.data[self.data['TRIAL'] == 'SAME'][measure]*pix_to_mm
        ONE = self.data[self.data['TRIAL'] == 'ONE'][measure]*pix_to_mm
        OPPO = self.data[self.data['TRIAL'] == 'OPPO'][measure]*pix_to_mm

        #Get PERFS values for each TYPE-TRIAL combination
        ALONE_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
        ALONE_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
        ALONE_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
        HFO_SAME =  self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
        HFO_ONE =  self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
        HFO_OPPO =  self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
        HFOP_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
        HFOP_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
        HFOP_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
        HVP_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='HVP')][measure]*pix_to_mm
        HVP_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='HVP')][measure]*pix_to_mm
        HVP_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='HVP')][measure]*pix_to_mm
        KVP_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='KVP')][measure]*pix_to_mm
        KVP_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='KVP')][measure]*pix_to_mm
        KVP_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='KVP')][measure]*pix_to_mm
        ROBOT_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='ROBOT')][measure]*pix_to_mm
        ROBOT_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='ROBOT')][measure]*pix_to_mm
        ROBOT_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='ROBOT')][measure]*pix_to_mm
 
 
        #Print RMS means and standard deviations for the different  conditions
        print "Factor\t",measure, "\t\tSt Dev"
        print " SAME :\t", np.mean(SAME) , "\t(" , np.std(SAME), ")"
        print "  ONE :\t", np.mean(ONE) , "\t(" , np.std(ONE), ")"
        print " OPPO :\t", np.mean(OPPO) , "\t(" , np.std(OPPO), ")"
        print "ALONE :\t", np.mean(ALONE) , "\t(" , np.std(ALONE), ")"
        print "  HFO :\t", np.mean(HFO) , "\t(" , np.std(HFO), ")"
        print " HFOP :\t", np.mean(HFOP) , "\t(" , np.std(HFOP), ")"
        print "  HVP :\t", np.mean(HVP) , "\t(" , np.std(HVP), ")"
        print "  KVP :\t", np.mean(KVP) , "\t(" , np.std(KVP), ")"
        print "  ROBOT :\t", np.mean(ROBOT) , "\t(" , np.std(ROBOT), ")"


#        print_ttest_results("HFOP", "HFO")# "HFOP vs HFO :\tt-value: " , stats.ttest_ind(HFOP, HFO)[0], "\tp-value :", stats.ttest_ind(HFOP, HFO)[1]
#        print_ttest_results("ALONE", "HFO")# :\tt-value: " , stats.ttest_ind(ALONE, HFO)[0], "\tp-value :", stats.ttest_ind(ALONE, HFO)[1]
#        print_ttest_results("ALONE", "HFOP")
#        print_ttest_results("ALONE", "HVP")
#        print_ttest_results("ALONE", "KVP")
#        print_ttest_results("HFOP", "HVP")
#        print_ttest_results("HFOP", "KVP")
#        print_ttest_results("HVP", "KVP")
        data2 = self.data[(self.data['TYPE']=='ALONE') | (self.data['TYPE']=='HFOP') | (self.data['TYPE']=='HFO')]
        data3 = self.data[(self.data['TYPE']=='ALONE') | (self.data['TYPE']=='HFOP') | (self.data['TYPE']=='HVP') | (self.data['TYPE']=='KVP')]
        print "EXPE1----------------------------------------------------------------"
        data_t = data2[data2['TYPE']=='ALONE']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING ALONE"
        print(aov_table)


        data_t = data2[data2['TYPE']=='HFO']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING HFO"
        print(aov_table)

        
        data_t = data2[data2['TYPE']=='HFOP']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING HFOP"
        print(aov_table)  
        
        print "EXPE2------------------------------------------------------------------"        
        
        data_t = data3[data3['TYPE']=='ALONE']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING ALONE"
        print(aov_table)        
 
        data_t = data3[data3['TYPE']=='HFOP']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING HFOP"
        print(aov_table)  
        
        data_t = data3[data3['TYPE']=='HVP']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING HVP"
        print(aov_table)

        data_t = data3[data3['TYPE']=='KVP']
        formula = measure + ' ~ C(TRIAL_NUMBER)'
        model = ols(formula, data_t).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS - LEARNING KVP"
        print(aov_table)

        print "-----------------------------------------------------------------------"        
        
        print "\n"
        #ANOVA on RMS values, factors are TYPE(ALONE, HFO, HFOP) and TRIAL(SAME, ONE, OPPO)
        formula = measure + ' ~ C(TRIAL) + C(TYPE) + C(TRIAL):C(TYPE)'
        model = ols(formula, self.data).fit()
        aov_table = anova_lm(model, typ = 2)
        eta_squared(aov_table)
        omega_squared(aov_table)
        print "ANOVA RESULTS"
        print(aov_table)
        print "\n"
#        res = model.resid
#        plt.figure()
#        fig = qqplot(res, line = 's')
#        plt.show()
        data2 = self.data[(self.data['TYPE']=='ALONE') | (self.data['TYPE']=='HFOP') | (self.data['TYPE']=='HFO')]
        data3 = self.data[(self.data['TYPE']=='ALONE') | (self.data['TYPE']=='HFOP') | (self.data['TYPE']=='HVP') | (self.data['TYPE']=='KVP')]
        
        SAME2 = data2[data2['TRIAL'] == 'SAME'][measure]*pix_to_mm
        ONE2 = data2[data2['TRIAL'] == 'ONE'][measure]*pix_to_mm
        OPPO2 = data2[data2['TRIAL'] == 'OPPO'][measure]*pix_to_mm
        SAME3 = data3[data3['TRIAL'] == 'SAME'][measure]*pix_to_mm
        ONE3 = data3[data3['TRIAL'] == 'ONE'][measure]*pix_to_mm
        OPPO3 = data3[data3['TRIAL'] == 'OPPO'][measure]*pix_to_mm   
        
        print ("-------------------------------------------------------------------\nHUMAN HUMAN")
        model2 = ols(formula, data2).fit()
        aov_table2 = anova_lm(model2, typ = 2)
        eta_squared(aov_table2)
        omega_squared(aov_table2)
        print "ANOVA RESULTS"
        print(aov_table2)
        print("\nt-tests trial type")
        print_ttest_results("SAME2", "ONE2")
        print_ttest_results("SAME2", "OPPO2")
        print_ttest_results("ONE2", "OPPO2")
        print_ttest_results("HFOP", "HFO")# "HFOP vs HFO :\tt-value: " , stats.ttest_ind(HFOP, HFO)[0], "\tp-value :", stats.ttest_ind(HFOP, HFO)[1]
        print_ttest_results("ALONE", "HFO")# :\tt-value: " , stats.ttest_ind(ALONE, HFO)[0], "\tp-value :", stats.ttest_ind(ALONE, HFO)[1]
        print_ttest_results("ALONE", "HFOP")#print "ALONE vs HFOP :\tt-value: " , stats.ttest_ind(ALONE, HFOP)[0], "\tp-value :", stats.ttest_ind(ALONE, HFOP)[1]
        print "\n"
        print_ttest_results("HFOP_SAME", "HFOP_ONE")        
        print_ttest_results("HFOP_SAME", "HFOP_OPPO")  
        print_ttest_results("HFOP_ONE", "HFOP_OPPO")  
        print_ttest_results("HFO_SAME", "HFO_ONE")        
        print_ttest_results("HFO_SAME", "HFO_OPPO")  
        print_ttest_results("HFO_ONE", "HFO_OPPO") 
        print_ttest_results("ALONE_SAME", "ALONE_ONE")        
        print_ttest_results("ALONE_SAME", "ALONE_OPPO")  
        print_ttest_results("ALONE_ONE", "ALONE_OPPO")         
        print "\n"
        print_ttest_results("HFOP_SAME", "HFO_SAME")#print "HFOP_SAME vs HFO_SAME :\tt-value: " , stats.ttest_ind(HFOP_SAME, HFO_SAME)[0], "\tp-value :", stats.ttest_ind(HFOP_SAME, HFO_SAME)[1]
        print_ttest_results("ALONE_SAME", "HFO_SAME")#print "ALONE_SAME vs HFO_SAME :\tt-value: " , stats.ttest_ind(ALONE_SAME, HFO_SAME)[0], "\tp-value :", stats.ttest_ind(ALONE_SAME, HFO_SAME)[1]
        print_ttest_results("ALONE_SAME", "HFOP_SAME")#print "ALONE_SAME vs HFOP_SAME :\tt-value: " , stats.ttest_ind(ALONE_SAME, HFOP_SAME)[0], "\tp-value :", stats.ttest_ind(ALONE_SAME, HFOP_SAME)[1]
        print_ttest_results("HFOP_ONE", "HFO_ONE")#print "HFOP_ONE vs HFO_ONE :\tt-value: " , stats.ttest_ind(HFOP_ONE, HFO_ONE)[0], "\tp-value :", stats.ttest_ind(HFOP_ONE, HFO_ONE)[1]
        print_ttest_results("ALONE_ONE", "HFO_ONE")#print "ALONE_ONE vs HFO_ONE :\tt-value: " , stats.ttest_ind(ALONE_ONE, HFO_ONE)[0], "\tp-value :", stats.ttest_ind(ALONE_ONE, HFO_ONE)[1]
        print_ttest_results("ALONE_ONE", "HFOP_ONE")#print "ALONE_ONE vs HFOP_ONE :\tt-value: " , stats.ttest_ind(ALONE_ONE, HFOP_ONE)[0], "\tp-value :", stats.ttest_ind(ALONE_ONE, HFOP_ONE)[1]
        print_ttest_results("HFOP_OPPO", "HFO_OPPO")#print "HFOP_OPPO vs HFO_OPPO :\tt-value: " , stats.ttest_ind(HFOP_OPPO, HFO_OPPO)[0], "\tp-value :", stats.ttest_ind(HFOP_OPPO, HFO_OPPO)[1]
        print_ttest_results("ALONE_OPPO", "HFO_OPPO")#print "ALONE_OPPO vs HFO_OPPO :\tt-value: " , stats.ttest_ind(ALONE_OPPO, HFO_OPPO)[0], "\tp-value :", stats.ttest_ind(ALONE_OPPO, HFO_OPPO)[1]
        print_ttest_results("ALONE_OPPO", "HFOP_OPPO")#print "ALONE_OPPO vs HFOP_OPPO :\tt-value: " , stats.ttest_ind(ALONE_OPPO, HFOP_OPPO)[0], "\tp-value :", stats.ttest_ind(ALONE_OPPO, HFOP_OPPO)[1]
        print "\n"
        
        print ("-----------------------------------------------------------------\nHUMAN ROBOT")
        model3 = ols(formula, data3).fit()
        aov_table3 = anova_lm(model3, typ = 2)
        eta_squared(aov_table3)
        omega_squared(aov_table3)
        print "ANOVA RESULTS"
        print(aov_table3)          
        print("\nt-tests trial type")
        print_ttest_results("SAME3", "ONE3")
        print_ttest_results("SAME3", "OPPO3")
        print_ttest_results("ONE3", "OPPO3")
        print_ttest_results("ALONE", "HFOP")
        print_ttest_results("ALONE", "HVP")
        print_ttest_results("ALONE", "KVP")
        print_ttest_results("HFOP", "HVP")
        print_ttest_results("HFOP", "KVP")
        print_ttest_results("HVP", "KVP")

        print "\n"
        
        print_ttest_results("ALONE_SAME", "HFOP_SAME")
        print_ttest_results("ALONE_SAME", "HVP_SAME")#print "ALONE_SAME vs HVP_SAME :\tt-value: " , stats.ttest_ind(ALONE_SAME, HVP_SAME)[0], "\tp-value :", stats.ttest_ind(ALONE_SAME, HVP_SAME)[1]
        print_ttest_results("ALONE_SAME", "KVP_SAME")#print "ALONE_SAME vs KVP_SAME :\tt-value: " , stats.ttest_ind(ALONE_SAME, KVP_SAME)[0], "\tp-value :", stats.ttest_ind(ALONE_SAME, KVP_SAME)[1]
        print_ttest_results("HFOP_SAME", "HVP_SAME")#print "HFOP_SAME vs HVP_SAME :\tt-value: " , stats.ttest_ind(HFOP_SAME, HVP_SAME)[0], "\tp-value :", stats.ttest_ind(HFOP_SAME, HVP_SAME)[1]
        print_ttest_results("HFOP_SAME", "KVP_SAME")#print "HFOP_SAME vs KVP_SAME :\tt-value: " , stats.ttest_ind(HFOP_SAME, KVP_SAME)[0], "\tp-value :", stats.ttest_ind(HFOP_SAME, KVP_SAME)[1]
        print_ttest_results("HVP_SAME", "KVP_SAME")#print "HVP_SAME vs KVP_SAME :\tt-value: " , stats.ttest_ind(HVP_SAME, KVP_SAME)[0], "\tp-value :", stats.ttest_ind(HVP_SAME, KVP_SAME)[1]  
        print ""
        print_ttest_results("ALONE_ONE", "HFOP_ONE")
        print_ttest_results("ALONE_ONE", "HVP_ONE")#print "ALONE_ONE vs HVP_ONE :\tt-value: " , stats.ttest_ind(ALONE_ONE, HVP_ONE)[0], "\tp-value :", stats.ttest_ind(ALONE_ONE, HVP_ONE)[1]
        print_ttest_results("ALONE_ONE", "KVP_ONE")#print "ALONE_ONE vs KVP_ONE :\tt-value: " , stats.ttest_ind(ALONE_ONE, KVP_ONE)[0], "\tp-value :", stats.ttest_ind(ALONE_ONE, KVP_ONE)[1]
        print_ttest_results("HFOP_ONE", "HVP_ONE")#print "HFOP_ONE vs HVP_ONE :\tt-value: " , stats.ttest_ind(HFOP_ONE, HVP_ONE)[0], "\tp-value :", stats.ttest_ind(HFOP_ONE, HVP_ONE)[1]
        print_ttest_results("HFOP_ONE", "KVP_ONE")#print "HFOP_ONE vs KVP_ONE :\tt-value: " , stats.ttest_ind(HFOP_ONE, KVP_ONE)[0], "\tp-value :", stats.ttest_ind(HFOP_ONE, KVP_ONE)[1]
        print_ttest_results("HVP_ONE", "KVP_ONE")#print "HVP_ONE vs KVP_ONE :\tt-value: " , stats.ttest_ind(HVP_ONE, KVP_ONE)[0], "\tp-value :", stats.ttest_ind(HVP_ONE, KVP_ONE)[1]       
        print ""
        print_ttest_results("ALONE_OPPO", "HFOP_OPPO")
        print_ttest_results("ALONE_OPPO", "HVP_OPPO")#print "ALONE_OPPO vs HVP_OPPO :\tt-value: " , stats.ttest_ind(ALONE_OPPO, HVP_OPPO)[0], "\tp-value :", stats.ttest_ind(ALONE_OPPO, HVP_OPPO)[1]
        print_ttest_results("ALONE_OPPO", "KVP_OPPO")#print "ALONE_OPPO vs KVP_OPPO :\tt-value: " , stats.ttest_ind(ALONE_OPPO, KVP_OPPO)[0], "\tp-value :", stats.ttest_ind(ALONE_OPPO, KVP_OPPO)[1]
        print_ttest_results("HFOP_OPPO", "HVP_OPPO")#print "HFOP_OPPO vs HVP_OPPO :\tt-value: " , stats.ttest_ind(HFOP_OPPO, HVP_OPPO)[0], "\tp-value :", stats.ttest_ind(HFOP_OPPO, HVP_OPPO)[1]
        print_ttest_results("HFOP_OPPO", "KVP_OPPO")#print "HFOP_OPPO vs KVP_OPPO :\tt-value: " , stats.ttest_ind(HFOP_OPPO, KVP_OPPO)[0], "\tp-value :", stats.ttest_ind(HFOP_OPPO, KVP_OPPO)[1]
        print_ttest_results("HVP_OPPO", "KVP_OPPO")#print "HVP_OPPO vs KVP_OPPO :\tt-value: " , stats.ttest_ind(HVP_OPPO, KVP_OPPO)[0], "\tp-value :", stats.ttest_ind(HVP_OPPO, KVP_OPPO)[1]        
        print "\n"
        print_ttest_results("HFOP_SAME", "HFOP_ONE")        
        print_ttest_results("HFOP_SAME", "HFOP_OPPO")  
        print_ttest_results("HFOP_ONE", "HFOP_OPPO")   
        print_ttest_results("ALONE_SAME", "ALONE_ONE")        
        print_ttest_results("ALONE_SAME", "ALONE_OPPO")  
        print_ttest_results("ALONE_ONE", "ALONE_OPPO")
        print_ttest_results("HVP_SAME", "HVP_ONE")        
        print_ttest_results("HVP_SAME", "HVP_OPPO")  
        print_ttest_results("HVP_ONE", "HVP_OPPO")
        print_ttest_results("KVP_SAME", "KVP_ONE")        
        print_ttest_results("KVP_SAME", "KVP_OPPO")  
        print_ttest_results("KVP_ONE", "KVP_OPPO")
        
        print ("\n-----------------------------------------------------------------\nROBOT ALONE")
        print("t-tests trial type")
        print_ttest_results("ALONE", "ROBOT")
        print_ttest_results("HFOP", "ROBOT")
        print_ttest_results("HFO", "ROBOT")
        print_ttest_results("HVP", "ROBOT")
        print_ttest_results("KVP", "ROBOT")
        print("\n")
        
        
        #Shapiro-Wilk test for normality of data, Levene test for homoscedasticity
        print 'Test de Shapiro-Wilk :' , stats.shapiro(self.data[measure])
        print 'Test de Levene : ', stats.levene(SAME, ONE, OPPO)
        print cohenns_d(HFOP, HFO), cohenns_d(HFOP, ALONE), cohenns_d(HFOP, HVP), cohenns_d(HFOP_SAME, HFO_SAME)
        
#        HFOP_test = self.data[self.data['TYPE'] == 'HFOP'].reset_index(drop=True)
#        HFOP_test.to_csv("~/temp.csv")
#        df_test = pt.DataFrame()
#        df_test.read_tbl("/home/lucas/temp.csv")
#        aov_test = df_test.anova('PERFS', sub='SUBJ_NAME', wfactors=['TYPE'])
#        print aov_test 
#        ALONE_test = self.data[self.data['TYPE'] == 'ALONE'].reset_index(drop=True)
#        ALONE_test.to_csv("~/temp.csv")
#        df_test = pt.DataFrame()
#        df_test.read_tbl("/home/lucas/temp.csv")
#        aov_test = df_test.anova1way('RMS', 'TRIAL_NUMBER')
#        print aov_test         
#        plt.figure(self.nbFig)
#        self.nbFig += 1
#        plt.hist(self.data[measure], 100)
        #plt.figure()
        #plt.hist(self.data['PERFS'], 100)
        #plt.show()

#        print "SAME_ALONE : \t", mean_confidence_interval(ALONE_SAME)
        
        #Bar graph with results for each factor combination
        tags = ('ALL TRIALS', 'SAME', 'ONE', 'OPPO')
        x_pos = np.arange(len(tags)-1)
        width = 0.120
        moyennes_ALONE = [np.mean(ALONE_SAME),np.mean(ALONE_ONE),np.mean(ALONE_OPPO)]
        moyennes_HFO = [np.mean(HFO_SAME),np.mean(HFO_ONE),np.mean(HFO_OPPO)]
        moyennes_HFOP = [np.mean(HFOP_SAME),np.mean(HFOP_ONE),np.mean(HFOP_OPPO)]
        moyennes_HVP = [np.mean(HVP_SAME),np.mean(HVP_ONE),np.mean(HVP_OPPO)]
        moyennes_KVP = [np.mean(KVP_SAME),np.mean(KVP_ONE),np.mean(KVP_OPPO)]
        moyennes_ROBOT = [np.mean(ROBOT_SAME),np.mean(ROBOT_ONE),np.mean(ROBOT_OPPO)]
        stdev_ALONE = [np.std(ALONE_SAME),np.std(ALONE_ONE),np.std(ALONE_OPPO)]
        stdev_HFO = [np.std(HFO_SAME),np.std(HFO_ONE),np.std(HFO_OPPO)]
        stdev_HFOP = [np.std(HFOP_SAME),np.std(HFOP_ONE),np.std(HFOP_OPPO)]
        stderr_ALONE = [stats.sem(ALONE_SAME),stats.sem(ALONE_ONE),stats.sem(ALONE_OPPO)]
        stderr_HFO = [stats.sem(HFO_SAME),stats.sem(HFO_ONE),stats.sem(HFO_OPPO)]
        stderr_HFOP = [stats.sem(HFOP_SAME),stats.sem(HFOP_ONE),stats.sem(HFOP_OPPO)]
        stderr_HVP = [stats.sem(HVP_SAME),stats.sem(HVP_ONE),stats.sem(HVP_OPPO)]
        stderr_KVP = [stats.sem(KVP_SAME),stats.sem(KVP_ONE),stats.sem(KVP_OPPO)]
        stderr_ROBOT = [stats.sem(ROBOT_SAME),stats.sem(ROBOT_ONE),stats.sem(ROBOT_OPPO)]
        
        plt.figure(self.nbFig)
        self.nbFig += 1
        y_inf = 0
#        if (measure=='RMS'):
#            y_sup=50
#        elif (measure=='PERFS'):
#            y_sup=1
#        elif(measure=='MAP'):
#            y_sup=250
#        elif(measure=='FOM'):
#            y_sup=250
        if measure == 'PERFS':
            y_label = 'PERFS'
        elif measure == 'RMS':
            y_label = 'RMS (m)'
        elif measure == 'MAP':
            y_label = 'MAP (J)'
        elif measure == 'FOM':
            y_label = 'FOM (N)'
        color_ALONE = (0.9, 0, 0)
        color_HFO = (0.5, 0.5, 1)
        color_HFOP = (0, 0, 0.5)
        color_HVP = (0.7, 0.2, 1)
        color_KVP = (0.5, 0, 0.6)
        color_ROBOT = (0, 1, 0)
        hatch_ALONE = ''
        hatch_HFO = ''
        hatch_HFOP = ''
        hatch_HVP = '/'
        hatch_KVP = '/'
        hatch_ROBOT = ''     
        y_sup = round(1.3*max(max(moyennes_ALONE), max(moyennes_HFO), max(moyennes_HFOP), max(moyennes_HVP), max(moyennes_KVP), max(moyennes_ROBOT)),roundVar)
        ax1 = plt.subplot(111)
        ax1.axis([ -1.6, 3, y_inf, y_sup])
        plt.bar([p for p in x_pos], moyennes_ALONE, align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar([p + width for p in x_pos], moyennes_HFO, align='center', width=width, color=color_HFO, hatch=hatch_HFO)
        plt.bar([p + 2*width for p in x_pos], moyennes_HFOP, align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.bar([p + 3*width for p in x_pos], moyennes_HVP, align='center', width=width, color=color_HVP, hatch=hatch_HVP)
        plt.bar([p + 4*width for p in x_pos], moyennes_KVP, align='center', width=width, color=color_KVP, hatch=hatch_KVP)
        plt.bar([p + 5*width for p in x_pos], moyennes_ROBOT, align='center', width=width, color=color_ROBOT, hatch=hatch_ROBOT)
        plt.errorbar([p for p in x_pos], moyennes_ALONE, yerr=stderr_ALONE, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + width for p in x_pos], moyennes_HFO, yerr=stderr_HFO, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 2*width for p in x_pos], moyennes_HFOP, yerr=stderr_HFOP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 3*width for p in x_pos], moyennes_HVP, yerr=stderr_HVP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 4*width for p in x_pos], moyennes_KVP, yerr=stderr_KVP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 5*width for p in x_pos], moyennes_ROBOT, yerr=stderr_ROBOT, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.bar(-1, np.mean(moyennes_ALONE), align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar(-1 + width, np.mean(moyennes_HFO), align='center', width=width, color=color_HFO, hatch=hatch_HFO)
        plt.bar(-1 + 2*width, np.mean(moyennes_HFOP), align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.bar(-1 + 3*width, np.mean(moyennes_HVP), align='center', width=width, color=color_HVP, hatch=hatch_HVP)
        plt.bar(-1 + 4*width, np.mean(moyennes_KVP), align='center', width=width, color=color_KVP, hatch=hatch_KVP)
        plt.bar(-1 + 5*width, np.mean(moyennes_ROBOT), align='center', width=width, color=color_ROBOT, hatch=hatch_ROBOT)
        plt.errorbar(-1, np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar(-1 + width, np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar(-1 + 2*width, np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.errorbar(-1 + 3*width, np.mean(moyennes_HVP), yerr=np.mean(stderr_HVP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.errorbar(-1 + 4*width, np.mean(moyennes_KVP), yerr=np.mean(stderr_KVP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.errorbar(-1 + 5*width, np.mean(moyennes_ROBOT), yerr=np.mean(stderr_ROBOT), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.xticks([-1 + 2.5*width] + [p + 2.5*width for p in x_pos], tags)
        plt.ylabel(y_label)
        plt.legend(['ALONE', 'HFO', 'HFOP', 'HVP', 'KVP', 'ROBOT'], loc=0)                  
   

        plt.figure(self.nbFig)
        self.nbFig += 1     
        ax1 = plt.subplot(111)
        width = 0.20
        ax1.axis([ -1.6, 3, y_inf, y_sup])
        plt.bar([p for p in x_pos], moyennes_ALONE, align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar([p + width for p in x_pos], moyennes_HFO, align='center', width=width, color=color_HFO, hatch=hatch_HFO)
        plt.bar([p + 2*width for p in x_pos], moyennes_HFOP, align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.errorbar([p for p in x_pos], moyennes_ALONE, yerr=stderr_ALONE, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + width for p in x_pos], moyennes_HFO, yerr=stderr_HFO, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 2*width for p in x_pos], moyennes_HFOP, yerr=stderr_HFOP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.bar(-1, np.mean(moyennes_ALONE), align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar(-1 + width, np.mean(moyennes_HFO), align='center', width=width, color=color_HFO, hatch=hatch_HFO)
        plt.bar(-1 + 2*width, np.mean(moyennes_HFOP), align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.errorbar(-1, np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar(-1 + width, np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar(-1 + 2*width, np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        

        plt.xticks([-1 + width] + [p + 1*width for p in x_pos], tags)
        plt.ylabel(y_label)
#        plt.legend(['ALONE', 'HFO', 'HFOP', 'HVP', 'KVP', 'ROBOT'], loc=0)        
        plt.legend(['ALONE', 'HFO', 'HFOP'], loc=0)  


        plt.figure(self.nbFig)
        self.nbFig += 1   
        ax1 = plt.subplot(111)
        width = 0.18
        ax1.axis([ -1.6, 3, y_inf, y_sup])
        plt.bar([p for p in x_pos], moyennes_ALONE, align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar([p + 1*width for p in x_pos], moyennes_HFOP, align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.bar([p + 2*width for p in x_pos], moyennes_HVP, align='center', width=width, color=color_HVP, hatch=hatch_HVP)
        plt.bar([p + 3*width for p in x_pos], moyennes_KVP, align='center', width=width, color=color_KVP, hatch=hatch_KVP)
        plt.errorbar([p for p in x_pos], moyennes_ALONE, yerr=stderr_ALONE, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 1*width for p in x_pos], moyennes_HFOP, yerr=stderr_HFOP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 2*width for p in x_pos], moyennes_HVP, yerr=stderr_HVP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar([p + 3*width for p in x_pos], moyennes_KVP, yerr=stderr_KVP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.bar(-1, np.mean(moyennes_ALONE), align='center', width=width, color=color_ALONE, hatch=hatch_ALONE)
        plt.bar(-1 + 1*width, np.mean(moyennes_HFOP), align='center', width=width, color=color_HFOP, hatch=hatch_HFOP)
        plt.bar(-1 + 2*width, np.mean(moyennes_HVP), align='center', width=width, color=color_HVP, hatch=hatch_HVP)
        plt.bar(-1 + 3*width, np.mean(moyennes_KVP), align='center', width=width, color=color_KVP, hatch=hatch_KVP)
        plt.errorbar(-1, np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
        plt.errorbar(-1 + 1*width, np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.errorbar(-1 + 2*width, np.mean(moyennes_HVP), yerr=np.mean(stderr_HVP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
        plt.errorbar(-1 + 3*width, np.mean(moyennes_KVP), yerr=np.mean(stderr_KVP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)              
        plt.xticks([-1 + 1.5*width] + [p + 1.5*width for p in x_pos], tags)
        plt.ylabel(y_label)
        plt.legend(['ALONE', 'HFOP', 'HVP', 'KVP'], loc=0)  
        
        plt.draw()
        plt.pause(0.001)
 
def main():
    global GUI
    root = Tk()
    root.title("STATS ANALYSIS")
    
    GUI = GUI_Class(root)

    root.mainloop() 
 
 
 
###############################################################################################################
def customMax(n):
    if not n:
        return 0
    else:
        return max(n)
        
def customMean(n):
    if not n:
        return 0
    else:
        return sum(n)/len(n)
        
def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    return aov
 
def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h
    
def cohenns_d(group1, group2):
    return (np.mean(group1)-np.mean(group2))/sqrt(0.5*(np.std(group1)+np.std(group2)))
    
def print_ttest_results(str_group1, str_group2):
    group1 = eval(str_group1)
    group2 = eval(str_group2)
    print str_group1+" vs "+str_group2+" :   \tt-value: " , round(stats.ttest_ind(group1, group2)[0], 5), "\tp-value :", round(stats.ttest_ind(group1, group2)[1],5), "\td-value :", round(cohenns_d(group1, group2),5)
      
def print_latex_table(conds):
    print '\\begin{tabular}{l*{' + str(2*(len(conds)-1)) + '}{x{1cm}}}'
    print '\\thickhline'
    temp = '\\multicolumn{1}{r}{Cond.1}'
    for i in range(0, len(conds)-1):
        temp += ' & \\multicolumn{2}{c}{' + conds[i] + '}'
    print temp + ' \\\\'
    print '\\cline{1-'+str(2*len(conds)-1)+'}'
    temp = 'Cond.2'
    for i in range(0, (len(conds)-1)):
        temp += ' & p & d '
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
