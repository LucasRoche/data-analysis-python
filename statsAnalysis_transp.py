# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:04:46 2017

@author: lucas
"""

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

class bcolors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m" 
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 

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
        
        self.labelSelectFigures = Label(self.frameMIDDLE, text = 'Fig').grid(row=0, column = 6)
        self.checkSelectFiguresVar = IntVar()
        self.checkBoxSelectFigures=Checkbutton(self.frameMIDDLE, variable = self.checkSelectFiguresVar)
        self.checkBoxSelectFigures.grid(row=0, column = 5)
        self.checkBoxSelectFigures.select()
        
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
        self.data = pandas.read_csv(self.file)
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
        self.trialsSelectedMenu.menu.add_command(label = 'ONE', command = self.setONE)
        self.trialsSelectedMenu.menu.add_command(label = 'TWO', command = self.setTWO)
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
        self.measureSelectedMenu.menu.add_command(label = 'ERR', command = self.setERR)
        self.measureSelectedMenu.menu.add_command(label = 'SCORE', command = self.setSCORE)
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
    def setERR(self):
        self.measureSelectedVar.set('ERR')
    def setSCORE(self):
        self.measureSelectedVar.set('SCORE')        
        
    def clearFigures(self):
        for i in range(0, self.nbFig):
            plt.close(i)
        self.nbFig = 0
        
    def show(self):
        plt.show(block=True)

    def processFiles(self):
        global HFOP, HFO, ALONE, PPSOFT, PPHARD, NOISY, SAME, ONE, OPPO, ALONE_SAME, ALONE_SAME, ALONE_ONE,ALONE_OPPO, HFO_SAME, HFO_ONE, HFO_OPPO, HFOP_SAME, HFOP_ONE, HFOP_OPPO, PPSOFT_SAME, PPSOFT_ONE, PPSOFT_OPPO, PPHARD_SAME, PPHARD_ONE, PPHARD_OPPO, NOISY_SAME, NOISY_ONE, NOISY_OPPO, DELAYED_SAME, DELAYED_ONE, DELAYED_OPPO
        global SAME2, SAME3, ONE2, ONE3, OPPO2, OPPO3, PPSOFT, PPHARD, NOISY, DELAYED
        global RAMP, SINUS, JUMP, ALONE_RAMP, ALONE_RAMP, ALONE_SINUS,ALONE_JUMP, HFO_RAMP, HFO_SINUS, HFO_JUMP, HFOP_RAMP, HFOP_SINUS, HFOP_JUMP, PPSOFT_RAMP, PPSOFT_SINUS, PPSOFT_JUMP, PPHARD_RAMP, PPHARD_SINUS, PPHARD_JUMP, NOISY_RAMP, NOISY_SINUS, NOISY_JUMP, DELAYED_RAMP, DELAYED_SINUS, DELAYED_JUMP
        self.loadData()
        
        plt.ion()
        plt.show()


        #remove unwanted trials
        if (self.trialsSelectedVar.get() == 'ONE'):
            self.data = self.data[(self.data['SCENARIO'] == 1) | (self.data['SCENARIO'] == 101)]
        elif (self.trialsSelectedVar.get() == 'TWO'):
            print self.trialsSelectedVar.get()            
            self.data = self.data[(self.data['SCENARIO'] == 2) | (self.data['SCENARIO'] == 99)]           
            
        #select studied measure
        measure = self.measureSelectedVar.get()
        
        #remove unwanted tests
        for i in range(0, self.nbTests):
            if self.checkBoxTrialsVar[i].get() == 0:
                self.data = self.data[self.data['TEST_NUMBER']!=i+1]        
        #Remove outliers in data (generally SAME trials where both subjects want the wrong way)
        self.data = self.data.drop(self.data[self.data['RMS']> np.mean(self.data['RMS'])+3*np.std(self.data['RMS'])].index)        
#        self.data = self.data.drop(self.data[self.data['RMS']> 100].index) 
#        self.data = self.data.drop(self.data[(self.data['TYPE']=='ALONE') & ((self.data['TRIAL_NUMBER']==1 )| (self.data['TRIAL_NUMBER']==2))].index)     
#        
        self.data = self.data.reset_index()
        
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
            
            
        HFOP = self.data[self.data['TYPE'] == 'HFOP'][measure]*pix_to_mm
        HFO = self.data[self.data['TYPE'] == 'HFO'][measure]*pix_to_mm
        ALONE = self.data[self.data['TYPE'] == 'ALONE'][measure]*pix_to_mm
        PPSOFT = self.data[self.data['TYPE'] == 'PPSOFT'][measure]*pix_to_mm
        PPHARD = self.data[self.data['TYPE'] == 'PPHARD'][measure]*pix_to_mm
        NOISY = self.data[self.data['TYPE'] == 'NOISY'][measure]*pix_to_mm
        DELAYED = self.data[self.data['TYPE'] == 'DELAYED'][measure]*pix_to_mm
        
        if measure == "FOM" or measure == "MAP":  
            conds = [ "HFOP" , "PPSOFT", "PPHARD", "NOISY"]
        else:
            conds = ["ALONE", "HFO", "HFOP" , "PPSOFT", "PPHARD", "NOISY"]
        
        print_latex_table(conds)
        print "\n"         
        #Get RMS values for each subcategory (3 TYPES and 3 TRIALS)
        
        for i in range(0, len(conds)):
            for j in range(0, len(conds)):
                if i < j:
                    print_ttest_results(conds[i], conds[j])
                    

        print "\n"      

       
#        #Shapiro-Wilk test for normality of data, Levene test for homoscedasticity
#        print 'Test de Shapiro-Wilk :' , stats.shapiro(self.data[measure])        

#########################################################################################################
        if( 'OPPO' in self.data['TRIAL'].values.tolist() ): 
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
            PPSOFT_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPSOFT_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPSOFT_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPHARD_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            PPHARD_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            PPHARD_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            NOISY_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            NOISY_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            NOISY_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            DELAYED_SAME = self.data[(self.data['TRIAL'] == 'SAME') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
            DELAYED_ONE = self.data[(self.data['TRIAL'] == 'ONE') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
            DELAYED_OPPO = self.data[(self.data['TRIAL'] == 'OPPO') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
     
            #Print RMS means and standard deviations for the different  conditions
            print "Factor\t",measure, "\t\tSt Dev"
            print " SAME :\t", np.mean(SAME) , "\t(" , np.std(SAME), ")"
            print "  ONE :\t", np.mean(ONE) , "\t(" , np.std(ONE), ")"
            print " OPPO :\t", np.mean(OPPO) , "\t(" , np.std(OPPO), ")"
            print "ALONE :\t", np.mean(ALONE) , "\t(" , np.std(ALONE), ")"
            print "  HFO :\t", np.mean(HFO) , "\t(" , np.std(HFO), ")"
            print " HFOP :\t", np.mean(HFOP) , "\t(" , np.std(HFOP), ")"
            print " PPSOFT :\t", np.mean(PPSOFT) , "\t(" , np.std(PPSOFT), ")"
            print " PPHARD :\t", np.mean(PPHARD) , "\t(" , np.std(PPHARD), ")"
            print " NOISY :\t", np.mean(NOISY) , "\t(" , np.std(NOISY), ")"
            print " DELAYED :\t", np.mean(DELAYED) , "\t(" , np.std(DELAYED), ")"
            
            print ""
            conds = ["ALONE_OPPO", "HFO_OPPO", "HFOP_OPPO" , "PPSOFT_OPPO", "PPHARD_OPPO", "NOISY_OPPO"]
            
            for i in range(0, len(conds)):
                for j in range(0, len(conds)):
                    if i < j:
                        print_ttest_results(conds[i], conds[j])  
                    
            #ANOVA on RMS values, factors are TYPE(ALONE? HFO, HFOP) and TRIAL(SAME, ONE, OPPO)
            formula = measure + ' ~ C(TRIAL) + C(TYPE) + C(TRIAL):C(TYPE)'
            model = ols(formula, self.data).fit()
            aov_table = anova_lm(model, typ = 2)
            eta_squared(aov_table)
            omega_squared(aov_table)
            print "ANOVA RESULTS"
            print(aov_table)
            print "\n"
            formula = measure + ' ~TYPE'
            model = ols(formula, self.data).fit()
            aov_table = anova_lm(model, typ = 2)
            eta_squared(aov_table)
            omega_squared(aov_table)
            print "ANOVA RESULTS"
            print(aov_table)                 
            
            if(self.checkSelectFiguresVar.get()==1):
                #Bar graph with results for each factor combination
                tags = ('ALL TRIALS', 'SAME', 'ONE', 'OPPO')
                x_pos = np.arange(len(tags)-1)
                width = 0.120
                moyennes_ALONE = [np.mean(ALONE_SAME),np.mean(ALONE_ONE),np.mean(ALONE_OPPO)]
                moyennes_HFO = [np.mean(HFO_SAME),np.mean(HFO_ONE),np.mean(HFO_OPPO)]
                moyennes_HFOP = [np.mean(HFOP_SAME),np.mean(HFOP_ONE),np.mean(HFOP_OPPO)]
                moyennes_PPSOFT = [np.mean(PPSOFT_SAME),np.mean(PPSOFT_ONE),np.mean(PPSOFT_OPPO)]
                moyennes_PPHARD = [np.mean(PPHARD_SAME),np.mean(PPHARD_ONE),np.mean(PPHARD_OPPO)]
                moyennes_NOISY = [np.mean(NOISY_SAME),np.mean(NOISY_ONE),np.mean(NOISY_OPPO)]
                moyennes_DELAYED = [np.mean(DELAYED_SAME),np.mean(DELAYED_ONE),np.mean(DELAYED_OPPO)]        
                stderr_ALONE = [stats.sem(ALONE_SAME),stats.sem(ALONE_ONE),stats.sem(ALONE_OPPO)]
                stderr_HFO = [stats.sem(HFO_SAME),stats.sem(HFO_ONE),stats.sem(HFO_OPPO)]
                stderr_HFOP = [stats.sem(HFOP_SAME),stats.sem(HFOP_ONE),stats.sem(HFOP_OPPO)]
                stderr_PPSOFT = [stats.sem(PPSOFT_SAME),stats.sem(PPSOFT_ONE),stats.sem(PPSOFT_OPPO)]
                stderr_PPHARD = [stats.sem(PPHARD_SAME),stats.sem(PPHARD_ONE),stats.sem(PPHARD_OPPO)]
                stderr_NOISY = [stats.sem(NOISY_SAME),stats.sem(NOISY_ONE),stats.sem(NOISY_OPPO)]
                stderr_DELAYED = [stats.sem(DELAYED_SAME),stats.sem(DELAYED_ONE),stats.sem(DELAYED_OPPO)]
                
                plt.figure(self.nbFig)
                self.nbFig += 1
                y_inf = 0
                if measure == 'PERFS':
                    y_label = 'PERFS'
                elif measure == 'RMS':
                    y_label = 'RMS (mm)'
                elif measure == 'MAP':
                    y_label = 'MAP (J)'
                elif measure == 'FOM':
                    y_label = 'FOM (N)'
                elif measure == 'ERR':
                    y_label = 'MAE (mm)' 
                elif measure == 'SCORE':
                    y_label = 'SCORE'                 
                y_sup = round(1.3*max(max(moyennes_ALONE), max(moyennes_HFO), max(moyennes_HFOP), max(moyennes_PPSOFT), max(moyennes_PPHARD), max(moyennes_NOISY), max(moyennes_DELAYED)),roundVar)
                ax1 = plt.subplot(111)
                ax1.axis([ -1.6, 3, y_inf, y_sup])
                plt.bar([p for p in x_pos], moyennes_ALONE, align='center', width=width, color='red')
                plt.bar([p + width for p in x_pos], moyennes_HFO, align='center', width=width, color='blue')
                plt.bar([p + 2*width for p in x_pos], moyennes_HFOP, align='center', width=width, color='green')
                plt.bar([p + 3*width for p in x_pos], moyennes_PPSOFT, align='center', width=width, color='purple')
                plt.bar([p + 4*width for p in x_pos], moyennes_PPHARD, align='center', width=width, color='orange')
                plt.bar([p + 5*width for p in x_pos], moyennes_NOISY, align='center', width=width, color='pink')
                plt.bar([p + 6*width for p in x_pos], moyennes_DELAYED, align='center', width=width, color='yellow')
                plt.errorbar([p for p in x_pos], moyennes_ALONE, yerr=stderr_ALONE, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + width for p in x_pos], moyennes_HFO, yerr=stderr_HFO, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 2*width for p in x_pos], moyennes_HFOP, yerr=stderr_HFOP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 3*width for p in x_pos], moyennes_PPSOFT, yerr=stderr_PPSOFT, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 4*width for p in x_pos], moyennes_PPHARD, yerr=stderr_PPHARD, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 5*width for p in x_pos], moyennes_NOISY, yerr=stderr_NOISY, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 6*width for p in x_pos], moyennes_DELAYED, yerr=stderr_DELAYED, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.bar(-1, np.mean(moyennes_ALONE), align='center', width=width, color='red')
                plt.bar(-1 + width, np.mean(moyennes_HFO), align='center', width=width, color='blue')
                plt.bar(-1 + 2*width, np.mean(moyennes_HFOP), align='center', width=width, color='green')
                plt.bar(-1 + 3*width, np.mean(moyennes_PPSOFT), align='center', width=width, color='purple')
                plt.bar(-1 + 4*width, np.mean(moyennes_PPHARD), align='center', width=width, color='orange')
                plt.bar(-1 + 5*width, np.mean(moyennes_NOISY), align='center', width=width, color='pink')
                plt.bar(-1 + 6*width, np.mean(moyennes_DELAYED), align='center', width=width, color='yellow')
                plt.errorbar(-1, np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(-1 + width, np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(-1 + 2*width, np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 3*width, np.mean(moyennes_PPSOFT), yerr=np.mean(stderr_PPSOFT), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 4*width, np.mean(moyennes_PPHARD), yerr=np.mean(stderr_PPHARD), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 5*width, np.mean(moyennes_NOISY), yerr=np.mean(stderr_NOISY), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    
                plt.errorbar(-1 + 6*width, np.mean(moyennes_DELAYED), yerr=np.mean(stderr_DELAYED), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    
                plt.xticks([-1 + 2.5*width] + [p + 2.5*width for p in x_pos], tags)
                plt.ylabel(y_label)
                plt.legend(['ALONE', 'HFO', '4C', 'PPSOFT', 'PPHARD', 'NOISY', 'DELAYED'], loc=0)                  


                plt.figure(self.nbFig)
                self.nbFig += 1
                ax2 = plt.subplot(111)
                tags = ['ALONE', 'HFO', '4C', 'PPSOFT', 'PPHARD', 'NOISY']    
                width = 0.8                
                x_pos = range(0, len(tags))
                colors = [
                    (1.0, 0.0, 0.0), 
                    (0.7, 0.0, 0.0),
                    (0.7, 0.0, 0.4),
                    (0.4, 0.0, 0.7),
                    (0.0, 0.0, 0.7),
                    (0.0, 0.0, 1.0),]
                plt.bar(x_pos[0], np.mean(moyennes_ALONE), align='center', width=width, color=colors[0])
                plt.bar(x_pos[1], np.mean(moyennes_HFO), align='center', width=width, color=colors[1])
                plt.bar(x_pos[2], np.mean(moyennes_HFOP), align='center', width=width, color=colors[2])
                plt.bar(x_pos[3], np.mean(moyennes_PPSOFT), align='center', width=width, color=colors[3])
                plt.bar(x_pos[4], np.mean(moyennes_PPHARD), align='center', width=width, color=colors[4])
                plt.bar(x_pos[5], np.mean(moyennes_NOISY), align='center', width=width, color=colors[5])
                plt.errorbar(x_pos[0], np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(x_pos[1], np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(x_pos[2], np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[3], np.mean(moyennes_PPSOFT), yerr=np.mean(stderr_PPSOFT), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[4], np.mean(moyennes_PPHARD), yerr=np.mean(stderr_PPHARD), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[5], np.mean(moyennes_NOISY), yerr=np.mean(stderr_NOISY), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    

                plt.xticks(x_pos, tags)
                plt.ylabel(y_label)
#                plt.legend(['ALONE', 'HFO', 'HFOP', 'PPSOFT', 'PPHARD', 'NOISY'], loc=0) 

                          
                plt.draw()
                plt.pause(0.001)

#########################################################################################################
        else:
#        HFOP_mou = self.data[self.data['TYPE'] == 'HFOP_mou'][measure]*pix_to_mm
            RAMP = self.data[self.data['TRIAL'] == 'RAMP'][measure]*pix_to_mm
            SINUS = self.data[self.data['TRIAL'] == 'SINUS'][measure]*pix_to_mm
            JUMP = self.data[self.data['TRIAL'] == 'JUMP'][measure]*pix_to_mm            
                #Get PERFS values for each TYPE-TRIAL combination
            ALONE_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
            ALONE_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
            ALONE_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='ALONE')][measure]*pix_to_mm
            HFO_RAMP =  self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
            HFO_SINUS =  self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
            HFO_JUMP =  self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='HFO')][measure]*pix_to_mm
            HFOP_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
            HFOP_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
            HFOP_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='HFOP')][measure]*pix_to_mm
            PPSOFT_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPSOFT_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPSOFT_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='PPSOFT')][measure]*pix_to_mm
            PPHARD_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            PPHARD_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            PPHARD_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='PPHARD')][measure]*pix_to_mm
            NOISY_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            NOISY_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            NOISY_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='NOISY')][measure]*pix_to_mm
            DELAYED_RAMP = self.data[(self.data['TRIAL'] == 'RAMP') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
            DELAYED_SINUS = self.data[(self.data['TRIAL'] == 'SINUS') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
            DELAYED_JUMP = self.data[(self.data['TRIAL'] == 'JUMP') & (self.data['TYPE']=='DELAYED')][measure]*pix_to_mm
     
            #Print RMS means and standard deviations for the different  conditions
            print "Factor\t",measure, "\t\tSt Dev"
            print " RAMP :\t", np.mean(RAMP) , "\t(" , np.std(RAMP), ")"
            print "SINUS :\t", np.mean(SINUS) , "\t(" , np.std(SINUS), ")"
            print " JUMP :\t", np.mean(JUMP) , "\t(" , np.std(JUMP), ")"
            print "ALONE :\t", np.mean(ALONE) , "\t(" , np.std(ALONE), ")"
            print "  HFO :\t", np.mean(HFO) , "\t(" , np.std(HFO), ")"
            print " HFOP :\t", np.mean(HFOP) , "\t(" , np.std(HFOP), ")"
            print " PPSOFT :\t", np.mean(PPSOFT) , "\t(" , np.std(PPSOFT), ")"
            print " PPHARD :\t", np.mean(PPHARD) , "\t(" , np.std(PPHARD), ")"
            print "  NOISY :\t", np.mean(NOISY) , "\t(" , np.std(NOISY), ")"
            print "DELAYED :\t", np.mean(DELAYED) , "\t(" , np.std(DELAYED), ")"
            
            print ""
#            conds = ["ALONE_JUMP", "HFO_JUMP", "HFOP_JUMP" , "PPSOFT_JUMP", "PPHARD_JUMP", "NOISY_JUMP"]
#            
#            for i in range(0, len(conds)):
#                for j in range(0, len(conds)):
#                    if i < j:
#                        print_ttest_results(conds[i], conds[j])  
                    
            #ANOVA on RMS values, factors are TYPE(ALONE? HFO, HFOP) and TRIAL(RAMP, SINUS, JUMP)
            formula = measure + ' ~ C(TRIAL) + C(TYPE) + C(TRIAL):C(TYPE)'
            model = ols(formula, self.data).fit()
            aov_table = anova_lm(model, typ = 2)
            eta_squared(aov_table)
            omega_squared(aov_table)
            print "ANOVA RESULTS"
            print(aov_table)
            
            formula = measure + ' ~TYPE'
            model = ols(formula, self.data).fit()
            aov_table = anova_lm(model, typ = 2)
            eta_squared(aov_table)
            omega_squared(aov_table)
            print "ANOVA RESULTS"
            print(aov_table)            
            
            
            
            if(self.checkSelectFiguresVar.get()==1):
                #Bar graph with results for each factor combination
                tags = ('ALL TRIALS', 'RAMP', 'SINUS', 'JUMP')
                x_pos = np.arange(len(tags)-1)
                width = 0.120
                moyennes_ALONE = [np.mean(ALONE_RAMP),np.mean(ALONE_SINUS),np.mean(ALONE_JUMP)]
                moyennes_HFO = [np.mean(HFO_RAMP),np.mean(HFO_SINUS),np.mean(HFO_JUMP)]
                moyennes_HFOP = [np.mean(HFOP_RAMP),np.mean(HFOP_SINUS),np.mean(HFOP_JUMP)]
                moyennes_PPSOFT = [np.mean(PPSOFT_RAMP),np.mean(PPSOFT_SINUS),np.mean(PPSOFT_JUMP)]
                moyennes_PPHARD = [np.mean(PPHARD_RAMP),np.mean(PPHARD_SINUS),np.mean(PPHARD_JUMP)]
                moyennes_NOISY = [np.mean(NOISY_RAMP),np.mean(NOISY_SINUS),np.mean(NOISY_JUMP)]
                moyennes_DELAYED = [np.mean(DELAYED_RAMP),np.mean(DELAYED_SINUS),np.mean(DELAYED_JUMP)]        
                stderr_ALONE = [stats.sem(ALONE_RAMP),stats.sem(ALONE_SINUS),stats.sem(ALONE_JUMP)]
                stderr_HFO = [stats.sem(HFO_RAMP),stats.sem(HFO_SINUS),stats.sem(HFO_JUMP)]
                stderr_HFOP = [stats.sem(HFOP_RAMP),stats.sem(HFOP_SINUS),stats.sem(HFOP_JUMP)]
                stderr_PPSOFT = [stats.sem(PPSOFT_RAMP),stats.sem(PPSOFT_SINUS),stats.sem(PPSOFT_JUMP)]
                stderr_PPHARD = [stats.sem(PPHARD_RAMP),stats.sem(PPHARD_SINUS),stats.sem(PPHARD_JUMP)]
                stderr_NOISY = [stats.sem(NOISY_RAMP),stats.sem(NOISY_SINUS),stats.sem(NOISY_JUMP)]
                stderr_DELAYED = [stats.sem(DELAYED_RAMP),stats.sem(DELAYED_SINUS),stats.sem(DELAYED_JUMP)]
                
                
                plt.figure(self.nbFig)
                self.nbFig += 1
                y_inf = 0
                if measure == 'PERFS':
                    y_label = 'PERFS'
                elif measure == 'RMS':
                    y_label = 'RMS (mm)'
                elif measure == 'MAP':
                    y_label = 'MAP (J)'
                elif measure == 'FOM':
                    y_label = 'FOM (N)'
                elif measure == 'ERR':
                    y_label = 'MAE (mm)' 
                elif measure == 'SCORE':
                    y_label = 'SCORE'                 
                y_sup = round(1.3*max(max(moyennes_ALONE), max(moyennes_HFO), max(moyennes_HFOP), max(moyennes_PPSOFT), max(moyennes_PPHARD), max(moyennes_NOISY), max(moyennes_DELAYED)),roundVar)
                ax1 = plt.subplot(111)
                ax1.axis([ -1.6, 3, y_inf, y_sup])
                plt.bar([p for p in x_pos], moyennes_ALONE, align='center', width=width, color='red')
                plt.bar([p + width for p in x_pos], moyennes_HFO, align='center', width=width, color='blue')
                plt.bar([p + 2*width for p in x_pos], moyennes_HFOP, align='center', width=width, color='green')
                plt.bar([p + 3*width for p in x_pos], moyennes_PPSOFT, align='center', width=width, color='purple')
                plt.bar([p + 4*width for p in x_pos], moyennes_PPHARD, align='center', width=width, color='orange')
                plt.bar([p + 5*width for p in x_pos], moyennes_NOISY, align='center', width=width, color='pink')
                plt.bar([p + 6*width for p in x_pos], moyennes_DELAYED, align='center', width=width, color='yellow')
                plt.errorbar([p for p in x_pos], moyennes_ALONE, yerr=stderr_ALONE, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + width for p in x_pos], moyennes_HFO, yerr=stderr_HFO, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 2*width for p in x_pos], moyennes_HFOP, yerr=stderr_HFOP, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 3*width for p in x_pos], moyennes_PPSOFT, yerr=stderr_PPSOFT, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 4*width for p in x_pos], moyennes_PPHARD, yerr=stderr_PPHARD, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 5*width for p in x_pos], moyennes_NOISY, yerr=stderr_NOISY, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar([p + 6*width for p in x_pos], moyennes_DELAYED, yerr=stderr_DELAYED, fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.bar(-1, np.mean(moyennes_ALONE), align='center', width=width, color='red')
                plt.bar(-1 + width, np.mean(moyennes_HFO), align='center', width=width, color='blue')
                plt.bar(-1 + 2*width, np.mean(moyennes_HFOP), align='center', width=width, color='green')
                plt.bar(-1 + 3*width, np.mean(moyennes_PPSOFT), align='center', width=width, color='purple')
                plt.bar(-1 + 4*width, np.mean(moyennes_PPHARD), align='center', width=width, color='orange')
                plt.bar(-1 + 5*width, np.mean(moyennes_NOISY), align='center', width=width, color='pink')
                plt.bar(-1 + 6*width, np.mean(moyennes_DELAYED), align='center', width=width, color='yellow')
                plt.errorbar(-1, np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(-1 + width, np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(-1 + 2*width, np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 3*width, np.mean(moyennes_PPSOFT), yerr=np.mean(stderr_PPSOFT), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 4*width, np.mean(moyennes_PPHARD), yerr=np.mean(stderr_PPHARD), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(-1 + 5*width, np.mean(moyennes_NOISY), yerr=np.mean(stderr_NOISY), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    
                plt.errorbar(-1 + 6*width, np.mean(moyennes_DELAYED), yerr=np.mean(stderr_DELAYED), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    
                plt.xticks([-1 + 2.5*width] + [p + 2.5*width for p in x_pos], tags)
                plt.ylabel(y_label)
                plt.legend(['ALONE', 'HFO', '4C', 'PPSOFT', 'PPHARD', 'NOISY', 'DELAYED'], loc=0)             

                plt.figure(self.nbFig)
                self.nbFig += 1
                ax2 = plt.subplot(111)
                tags = ['ALONE', 'HFO', '4C', 'PPSOFT', 'PPHARD', 'NOISY']    
                width = 0.8                
                x_pos = range(0, len(tags))
                colors = [
                    (1.0, 0.1, 0.1), 
                    (0.7, 0.0, 0.0),
                    (0.7, 0.0, 0.4),
                    (0.4, 0.0, 0.7),
                    (0.0, 0.0, 0.7),
                    (0.0, 0.0, 1.0),]
                plt.bar(x_pos[0], np.mean(moyennes_ALONE), align='center', width=width, color=colors[0])
                plt.bar(x_pos[1], np.mean(moyennes_HFO), align='center', width=width, color=colors[3])
                plt.bar(x_pos[2], np.mean(moyennes_HFOP), align='center', width=width, color=colors[4])
                plt.bar(x_pos[3], np.mean(moyennes_PPSOFT), align='center', width=width, color=colors[0], hatch="/")
                plt.bar(x_pos[4], np.mean(moyennes_PPHARD), align='center', width=width, color=colors[3], hatch="/")
                plt.bar(x_pos[5], np.mean(moyennes_NOISY), align='center', width=width, color=colors[5], hatch="/")
                plt.errorbar(x_pos[0], np.mean(moyennes_ALONE), yerr=np.mean(stderr_ALONE), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(x_pos[1], np.mean(moyennes_HFO), yerr=np.mean(stderr_HFO), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)
                plt.errorbar(x_pos[2], np.mean(moyennes_HFOP), yerr=np.mean(stderr_HFOP), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[3], np.mean(moyennes_PPSOFT), yerr=np.mean(stderr_PPSOFT), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[4], np.mean(moyennes_PPHARD), yerr=np.mean(stderr_PPHARD), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)        
                plt.errorbar(x_pos[5], np.mean(moyennes_NOISY), yerr=np.mean(stderr_NOISY), fmt=None, ecolor='k', elinewidth=2, markeredgewidth = 2)    

                plt.xticks(x_pos, tags)
                plt.ylabel(y_label)    
                         
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
    if abs(stats.ttest_ind(group1, group2)[1]) < 0.015:
        color = bcolors.GREEN
    else:
        color = bcolors.ENDC
    print color +  str_group1+" vs "+str_group2+" :   \tt-value: " , round(stats.ttest_ind(group1, group2)[0], 5), "\tp-value :", round(stats.ttest_ind(group1, group2)[1],5), "\td-value :", round(cohenns_d(group1, group2),5) ,bcolors.ENDC

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
