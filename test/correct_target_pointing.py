# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:45:57 2017

@author: lucas
"""
from Tkinter import *
from tkFileDialog import *

root = Tk()
root.withdraw()
file_names = askopenfilenames(initialdir = '~/Documents/Manip')
file_names = root.tk.splitlist(file_names)
root.destroy()
for file in file_names:
    scenario = file[file.find("_scenario_") + 10: file.find("_scenario_") + 13]
    
    scenario_file = "/home/lucas/phri/lucas/scenarios/pointing/SCENARIO_POINTING_"+scenario+".txt"
    
    output_file = "/home/lucas/Documents/TEST/modified/"+file[file.find("RESULTS"):]
    
    f_in = open(file, 'r')
    f_sc = open(scenario_file, 'r')
    f_out = open(output_file, 'w')
    
    i=0
    for line_in in f_in:
        if i < 23:
            f_out.write(line_in)            
        else:
            line_sc = f_sc.readline()
            line_sc = line_sc[0:line_sc.find("\n")]
            line_sc = line_sc.split("\t")
            
            line_in = line_in.split("\t")
            
            print line_sc
            
            sc_type = line_sc[3]
            if(sc_type=="0" or sc_type=="1"):
                f_out.write(line_in[0]+'\t'+line_in[1]+'\t'+line_in[2]+'\t'+line_in[3]+'\t'+line_in[4]+'\t'+line_in[5]+'\t'+line_in[6]+'\t'+line_in[7]+line_in[8] )
            elif(sc_type=="2"):
                f_out.write(line_in[0]+'\t'+line_in[1]+'\t'+line_in[2]+'\t'+line_in[3]+'\t'+"0"+'\t'+"1"+'\t'+line_in[6]+'\t'+line_in[7]+line_in[8] )
            elif(sc_type=="3"):
                f_out.write(line_in[0]+'\t'+line_in[1]+'\t'+line_in[2]+'\t'+line_in[3]+'\t'+"0"+'\t'+"2"+'\t'+line_in[6]+'\t'+line_in[7]+line_in[8] )
            elif(sc_type=="4"):
                f_out.write(line_in[0]+'\t'+line_in[1]+'\t'+line_in[2]+'\t'+line_in[3]+'\t'+"1"+'\t'+"0"+'\t'+line_in[6]+'\t'+line_in[7]+line_in[8] )
            elif(sc_type=="5"):
                f_out.write(line_in[0]+'\t'+line_in[1]+'\t'+line_in[2]+'\t'+line_in[3]+'\t'+"2"+'\t'+"0"+'\t'+line_in[6]+'\t'+line_in[7]+line_in[8] )
          
        i+=1
        
    f_in.close()
    f_out.close()
    f_sc.close()