# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:23:20 2015

@author: roche
"""

from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    global force_F, force_L
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '../results')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    
    file_names_HFO = [x for x in file_names if x.find('_s_')!=-1]
    file_names_HFOP = [x for x in file_names if x.find('_a_')!=-1]
    
    file_names = file_names_HFO + file_names_HFOP

    date = time.gmtime(None)
    date = str(date.tm_mday) + "-" + str(date.tm_mon) + "-" +  str(date.tm_hour+2) + "-" +  str(date.tm_min)
    directory_name = "../post-traitement/PT_Forces_" + date
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)       

    results_file = directory_name + "/PT_Forces.txt"
        
    f = open(results_file, 'w')
    
    f.write("Fichier de resultats pour les tests type \"GROTEN\" \n")
    f.write("\n")
#    f.write("Sujets : " + str(SUBJECT_NAME1) + " + " + str(SUBJECT_NAME2) + "\n")
    f.write("\n")
    f.write("Donnees obetnues a partir des fichiers : \n")
    for x in file_names:
        f.write(x + "\n")
    f.write("\n")
    

    force_F_HFOP = []
    force_L_HFOP = []
    force_F_HFO  = []
    force_L_HFO  = []      
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        DataClass.extractForces()
        
        if DataClass.fileType == 'HFOP':
            force_L_HFOP.append(DataClass.forceIntLeader)
            force_F_HFOP.append(DataClass.forceIntFollower)
        elif DataClass.fileType == 'HFO':
            force_L_HFO.append(DataClass.forceIntLeader)
            force_F_HFO.append(DataClass.forceIntFollower)
            
        print " File " + str(DataClass.fileName) + " treated ..."
        
        writeInFile(DataClass, f)
    
    force_F = force_F_HFOP + force_F_HFO
    force_L = force_L_HFOP + force_L_HFO
        
    writeInFileFinal(force_F, force_L, f)
    
#    print force_L, force_F

# T-test 
#    N_L = len(force_L)
#    N_F = len(force_F)
#    moy_L = sum(force_L)/N_L
#    moy_F = sum(force_F)/N_F
#    var_L = 0
#    var_F = 0
#
#    for i in range (0, N_L)  :  
#        var_L += (force_L[i] - moy_L)**2
#    var_L /= N_L
#    for i in range (0, N_F)  :  
#        var_F += (force_F[i] - moy_F)**2
#    var_F /= N_F
#
    diff_HFOP = []
    diff_HFO = []
    
    for i in range (0, len(force_F_HFOP)):
        for j in range (0, len(force_F_HFOP[i])):
            diff_HFOP.append(abs(force_L_HFOP[i][j]) - abs(force_F_HFOP[i][j]))
#            diff_HFOP.append(force_L_HFOP[i][j] - force_F_HFOP[i][j])
       
    M_HFOP = sum(diff_HFOP)/len(diff_HFOP)
    var_HFOP = 0
    for i in range (0, len(diff_HFOP))  :  
        var_HFOP += (diff_HFOP[i] - M_HFOP)**2
    var_HFOP /= len(diff_HFOP)
    
    t_HFOP = M_HFOP/(sqrt(var_HFOP/len(diff_HFOP)))

    for i in range (0, len(force_F_HFO)):
        for j in range (0, len(force_F_HFO[i])):
            diff_HFO.append(abs(force_L_HFO[i][j]) - abs(force_F_HFO[i][j]))
#            diff_HFO.append(force_L_HFO[i][j] - force_F_HFO[i][j])
            
    M_HFO = sum(diff_HFO)/len(diff_HFO)
    var_HFO = 0
    for i in range (0, len(diff_HFO))  :  
        var_HFO += (diff_HFO[i] - M_HFO)**2
    var_HFO /= len(diff_HFO)
    
    t_HFO = M_HFO/(sqrt(var_HFO/len(diff_HFO)))
  
    print  t_HFOP, t_HFO, len(diff_HFOP)-2,  len(diff_HFO)-2
    
    f.close()

def writeInFile(DataClass, f):    
    f.write("\n")
    f.write("Fichier : " + DataClass.fileName)
    f.write('\n')
    f.write("Integral of Forces Leader :\n")
    for e in DataClass.forceIntLeader:
        f.write(str(e) + '\t')
    f.write('\n')
    f.write('\n')
    f.write("Integral of Forces Follower :\n")
    for e in DataClass.forceIntFollower:
        f.write(str(e) + '\t')
    f.write('\n')
    f.write('\n')

def writeInFileFinal(force_F, force_L, f):
    f.write('\n')
    f.write('Integrales des efforts :\n') 
    f.write('Leader\tFollower\n')
    for i in range (0, len(force_F)):
        for j in range (0, len(force_F[i])):
            f.write(str(force_L[i][j]) + '\t' + str(force_F[i][j]) + '\n')
    
    
    
if __name__ == '__main__':
    main()