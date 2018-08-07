#!/usr/bin/python

import sys
from math import *
from params import *


def isInObstacle(X,Y,obstacles_file_number):
    OBST_LIST = []
    X = int(X)
    Y = int(Y)
    obst_file_name = "./obstacles/OBSTACLES_" + str(obstacles_file_number) + ".txt"
    obstFile = open(obst_file_name, 'r')
    for line in obstFile:
	lineR = line[0:line.find("\n")]
	obstList=lineR.split("\t")
	OBST_LIST.append(obstList)
    
    for obst in OBST_LIST:
	x_obst = int(obst[0])
	y_obst = int(obst[1])
	radius_obst = int(obst[2])
	if sqrt((X - x_obst)**2 + (Y - y_obst)**2) <= radius_obst+CURSOR_WIDTH:
	    return True

    return False


def main():
    PATH_POS1 = [0]*PATH_LENGTH
    path_file_name_1 = "./path/PATH_scenario_" + sys.argv[1] + "_subject_" + "1" + ".txt"
    fPos1 = open(path_file_name_1, 'r')
    for line in fPos1: #Creation d'un vecteur contenant les positions du path du sujet 1
        lineReadPosition1 = line
        lineReadPosition1 = lineReadPosition1[ 0 : lineReadPosition1.find("\n")]
        posList1 = lineReadPosition1.split('\t')
        pixel = int(posList1[0])
        PATH_POS1[pixel] = int(float(posList1[1]))
    fPos1.close()

    for i in range(0, PATH_LENGTH):
    	n = isInObstacle(PATH_POS1[i],i, sys.argv[2])
        #print i, PATH_POS1[i], n


if __name__ == '__main__':
    main()
