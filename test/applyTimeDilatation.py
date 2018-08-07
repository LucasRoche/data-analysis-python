# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:56:55 2015

@author: roche
"""
file_name = []
file_name_modified = []

for file in os.listdir("/home/roche/MANIP_v7/expe"):
    if file.endswith(".txt"):
        file_name.append("/home/roche/MANIP_v7/expe/" + file)
        file_name_modified.append("/home/roche/MANIP_v7/test/" + file)
    else:
        print "Fichier" + file + "non supporte"


#file_name = "/home/roche/MANIP_v7/expe/RESULTS_scenario_11_trial_1_s_1-4-14-51.txt"


for i in range (0, len(file_name)):
    file_name_reduit = file_name[i][file_name[i].find("expe/")+5:]
    file_name_modified = "/home/roche/MANIP_v7/test/" + file_name_reduit
    
    print file_name[i]
    
    scenario_number = file_name_reduit[file_name_reduit.find("_scenario_")+10 : file_name_reduit.find("_trial_")]
    
    path_file_name_1 = "/home/roche/MANIP_v7/path/PATH_scenario_" + scenario_number + "_subject_" + "1" + ".txt"
    path_file_name_2 = "/home/roche/MANIP_v7/path/PATH_scenario_" + scenario_number + "_subject_" + "2" + ".txt"
    
    
    PATH_POS1 = [None]*PATH_LENGTH
    PATH_POS2 = [None]*PATH_LENGTH
    
    fPos1 = open(path_file_name_1, 'r')
    for line in fPos1: #Creation d'un vecteur contenant les positions du path du sujet 1
        lineReadPosition1 = line
        lineReadPosition1 = lineReadPosition1[ 0 : lineReadPosition1.find("\n")]
        posList1 = lineReadPosition1.split('\t')
        pixel = int(posList1[0])
        PATH_POS1[pixel] = posList1[1]
    fPos1.close()
    
    
    fPos2 = open(path_file_name_2, 'r')
    for line in fPos2: #Creation d'un vecteur contenant les positions du path du sujet 2
        lineReadPosition2 = line
        lineReadPosition2 = lineReadPosition2[ 0 : lineReadPosition2.find("\n")]
        posList2 = lineReadPosition2.split('\t')
        pixel = int(posList2[0])
        PATH_POS2[pixel] = posList2[1]
    fPos2.close()
    
    
    file_to_modify = open(file_name[i], 'r')
    file_modified = open(file_name_modified, 'w')
    
    
    for line in file_to_modify:
        lineReadData = line[ 0 : line.find("\n")]
        finalTime = lineReadData.split('\t')[0]
    file_to_modify.close()
    
    file_to_modify = open(file_name[i], 'r')
    
    time_offset = float(Y_POS_CURSOR)/float(VITESSE)
    facteurDilatation = (PATH_DURATION + float(WINDOW_LENGTH)/VITESSE)/float(finalTime)
    i=0
    for line in file_to_modify:
        if i<15:
            file_modified.write(line)
            
        elif i>=15:
            lineReadData = line
            lineReadData = lineReadData[ 0 : lineReadData.find("\n")]
            dataList=lineReadData.split('\t')
            timePaddle = float(dataList[0])
            timePaddleModified = timePaddle * facteurDilatation
            if (timePaddleModified <= time_offset or int(timePaddleModified-time_offset) >= PATH_DURATION):
                dataList[1] = -1
                dataList[2] = -1
            else:
                dataList[1] = PATH_POS1[int((timePaddleModified-time_offset)*VITESSE)]
                dataList[2] = PATH_POS2[int((timePaddleModified-time_offset)*VITESSE)]
                
            file_modified.write(str(dataList[0]) + "\t" + str(dataList[1]) + "\t" + str(dataList[2]) + "\t" + str(dataList[3]) + "\t" + str(dataList[4]) + "\t" + str(dataList[5]) + "\t" + str(dataList[6]) + "\t" + str(dataList[7]) + "\t" + str(dataList[8]) + "\t" + str(dataList[9]) + "\n")
    
            
        i+=1
        
    file_to_modify.close()
    file_modified.close()