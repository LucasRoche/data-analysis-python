# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:06:48 2015

@author: Lucas
"""

import numpy, pickle


def main():
            
    fileName = '../results/2eme MANIP/ALL/RESULTS_scenario_12_trial_1_a_3-6-10-39.txt'    

    if fileName.find('_a_') != -1:
        fileType = 'HFOP'
    elif fileName.find('_s_') != -1:
        fileType = 'HFO' 
    elif fileName.find('_w_') != -1:
        fileType = 'ALONE'
    elif fileName.find('_u_') != -1:
        fileType = 'ULTRON'
    elif fileName.find('_r_') != -1:
        fileType = 'ROBOT'

    Time      = []
    Path_pos1 = []
    Path_pos2 = []
    Curs_pos  = []
    Subj_pos1 = []
    Subj_pos2 = []
    Subj_for1 = []
    Subj_for2 = []
    if fileType == 'ALONE' or fileType == 'ULTRON' or fileType == 'ROBOT':
        Curs_pos1 = []
        Curs_pos2 = []
        Robot_pos1 = []
        Robot_pos2 = []

    
    f = open(fileName,'r')
    for line in f:
        if line.find('SUBJECT NAME1')!=-1:
            SUBJECT_NAME1 = line[line.find(' : ')+3 : line.find("\n")]
        elif line.find('SUBJECT NAME2')!=-1:
            SUBJECT_NAME2 = line[line.find(' : ')+3 : line.find("\n")] 
        elif line.find('PATH_DURATION')!=-1:
            PATH_DURATION = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('VITESSE')!=-1:
            VITESSE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('Y_POS_CURSOR')!=-1:
            Y_POS_CURSOR = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_BODY')!=-1:
            PART_DURATION_BODY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_CHOICE')!=-1:
            PART_DURATION_CHOICE = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_FORK')!=-1:
            PART_DURATION_FORK = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_REGRP')!=-1:
            PART_DURATION_REGRP = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('PART_DURATION_START')!=-1:
            PART_DURATION_START = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('POSITION_OFFSET')!=-1:
            POSITION_OFFSET = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('SENSIBILITY')!=-1:
            SENSIBILITY = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_WIDTH')!=-1:
            WINDOW_WIDTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find('WINDOW_LENGTH')!=-1:
            WINDOW_LENGTH = float(line[line.find(' : ')+3 : line.find("\n")])
        elif line.find("RESULTS") != -1:
            break
    f.close()    
    
    
    
    f=open(fileName,'r')
    
    for line in f:
        lineReadData = line[ 0 : line.find("\n")]
        finalTime = lineReadData.split('\t')[0]
    f.close()

    timeOffset = float(Y_POS_CURSOR)/float(VITESSE)
    facteurDilatation = float(finalTime)/(PATH_DURATION + float(WINDOW_LENGTH)/VITESSE)
    
    f = open(fileName, 'r')
    i=0
    k = 0
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
            Time.append(float(dataList[0]))
            Path_pos1.append(float(dataList[1]))
            Path_pos2.append(float(dataList[2]))
            Subj_pos1.append(WINDOW_WIDTH/2*(1 - (float(dataList[3]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Subj_pos2.append(WINDOW_WIDTH/2*(1 - (float(dataList[4]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            Subj_for1.append(float(dataList[5]))
            Subj_for2.append(float(dataList[6]))
            if fileType == 'HFOP' or fileType == 'HFO':
                Curs_pos.append(WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[4]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            elif fileType == 'ALONE':
                Curs_pos1.append(WINDOW_WIDTH/2*(1 - (float(dataList[3]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
                Curs_pos2.append(WINDOW_WIDTH/2*(1 - (float(dataList[4]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
            elif fileType == 'ULTRON' or fileType == 'ROBOT':
                Curs_pos1.append(WINDOW_WIDTH/2*(1 - ((float(dataList[3])+float(dataList[7]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
                Curs_pos2.append(WINDOW_WIDTH/2*(1 - ((float(dataList[4])+float(dataList[8]))/2 - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
                Robot_pos1.append(WINDOW_WIDTH/2*(1 - (float(dataList[7]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
                Robot_pos2.append(WINDOW_WIDTH/2*(1 - (float(dataList[8]) - POSITION_OFFSET) / POSITION_OFFSET * SENSIBILITY))
        i+=1
    
    f.close()    

    DataDict = {}
    DataDict['SUBJECT_NAME1'] = SUBJECT_NAME1
    DataDict['SUBJECT_NAME2'] = SUBJECT_NAME2
    DataDict['PATH_DURATION'] = PATH_DURATION
    DataDict['VITESSE'] = VITESSE
    DataDict['Y_POS_CURSOR'] = Y_POS_CURSOR
    DataDict['PART_DURATION_BODY'] = PART_DURATION_BODY
    DataDict['PART_DURATION_CHOICE'] = PART_DURATION_CHOICE
    DataDict['PART_DURATION_FORK'] = PART_DURATION_FORK
    DataDict['PART_DURATION_REGRP'] = PART_DURATION_REGRP
    DataDict['PART_DURATION_START'] = PART_DURATION_START
    DataDict['POSITION_OFFSET'] = POSITION_OFFSET
    DataDict['SENSIBILITY'] = SENSIBILITY
    DataDict['WINDOW_WIDTH'] = WINDOW_WIDTH
    DataDict['WINDOW_LENGTH'] = WINDOW_LENGTH
    DataDict['timeOffset'] = timeOffset
    DataDict['facteurDilatation'] = facteurDilatation
    DataDict['Time'] = Time
    DataDict['Path_pos1'] = Path_pos1
    DataDict['Path_pos2'] = Path_pos2
    DataDict['Subj_pos1'] = Subj_pos1
    DataDict['Subj_pos2'] = Subj_pos2
    DataDict['Subj_for1'] = Subj_for1
    DataDict['Subj_for2'] = Subj_for2
    if fileType == 'HFOP' or fileType == 'HFO':
        DataDict['Curs_pos'] = Curs_pos
    elif fileType == 'ALONE':
        DataDict['Curs_pos1'] = Curs_pos1
        DataDict['Curs_pos2'] = Curs_pos2
    elif fileType == 'ULTRON' or fileType == 'ROBOT':
        DataDict['Curs_pos1'] = Curs_pos1
        DataDict['Curs_pos2'] = Curs_pos2
        DataDict['Robot_pos1'] = Robot_pos1
        DataDict['Robot_pos2'] = Robot_pos2
        

    picklefile = open('DataPickle', 'w')
    
    pickle.dump(DataDict, picklefile)


if __name__ == "__main__":
    main()