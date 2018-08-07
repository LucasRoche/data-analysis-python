#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

import random
LINE_WIDTH=4
LINE_WIDTH_BOLD=LINE_WIDTH*10
WINDOW_WIDTH = 800
PATH_WIDTH=WINDOW_WIDTH
PATH_DURATION = 300
VITESSE = 120.0
PATH_LENGTH = int(PATH_DURATION*VITESSE)
#Creating the vector containing the obstacles positions
OBSTACLE=[0]*PATH_LENGTH
OBSTACLE_RADIUS_MIN = LINE_WIDTH_BOLD/2
OBSTACLE_RADIUS_MAX = 2*LINE_WIDTH_BOLD
GRILLE_OBST_X = PATH_WIDTH/10
GRILLE_OBST_Y = PATH_WIDTH/10
CHANCE_OBST=0.1
DUREE_COURTE = 2
DUREE_LONGUE = 4


def main():
    #Creation of an empty file
    try:
        scenario_number= input("Entrez un numero de scenario\n")
        if (scenario_number == ""):
            scenario_number = 1
    except:
        print "Error while entering scenario number - generating default scenario 1000\n"
        scenario_number = 1000

    generateObstacleFile(scenario_number)


def generateObstacleFile(scenario_number):
    
    file_name="../../lucas/scenarios/obstacle/OBSTACLES_" + str(scenario_number) + ".txt"

    scenarioFile= open(file_name, 'w')
    
    i=1
    x_obst = 0
    y_obst = 0
    while i < PATH_LENGTH:
	j=1
	while j < PATH_WIDTH:
	    x = random.randint(0,100)
	    if x < CHANCE_OBST*100:
		x_obst = random.randint(j, j + GRILLE_OBST_X)
		y_obst = i
		radius_obst = random.randint(OBSTACLE_RADIUS_MIN, OBSTACLE_RADIUS_MAX)
		line = str(x_obst) + "\t" + str(y_obst) + "\t" + str(radius_obst) + "\n"
		scenarioFile.write(line)    
	    j += GRILLE_OBST_X
        
	i += GRILLE_OBST_Y
        
    scenarioFile.close()


if __name__ == '__main__':
    main()
