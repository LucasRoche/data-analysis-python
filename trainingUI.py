#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

############################################################################################################################################
#IMPORTS 
############################################################################################################################################
import pygame, sys, math, os
from pygame.locals import *
import random
import socket
import threading
import time

from params import *


#Define the destination screen (for subject 1 or 2)
SUJET = int(sys.argv[2])


#Define position of the window on the screen
if SUJET == 1:
    position = SCREEN_POSITION_1
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
elif SUJET == 2:
    position = SCREEN_POSITION_2
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])


#Initialisation of pygame, creation of the main window
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF= pygame.display.set_mode((WINDOW_WIDTH, WINDOW_LENGTH))
DISPLAYSURF.fill(GREY)
TITLE = 'UI v7 - Sujet ' + str(SUJET)
pygame.display.set_caption(TITLE)
pygame.display.update()



if SUJET ==1:
    sock1 = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock1.bind((UDP_IP, UDP_PORT1))

    sock_envoi = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock_envoi.bind((UDP_IP, UDP_PORT3))

    sock2 = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock2.bind((UDP_IP, UDP_PORT2))

if SUJET ==2:
    sock1 = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock1.bind((UDP_IP, UDP_PORT4))

    sock2 = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock2.bind((UDP_IP, UDP_PORT5))


############################################################################################################################################
#FUNCTIONS 
############################################################################################################################################


############################################################################################################################################
#Thread used to recover data from the robot
def receive_data():
    global pos1, pos2, thread_alive
    while thread_alive:
        #Read socket to get info about cursor
        data1, addr = sock1.recvfrom(1024)
        data1 = float(data1[0:data1.find("\n")])
        pos1 = (data1-POSITION_OFFSET)/POSITION_OFFSET*SENSIBILITY
        data2, addr = sock2.recvfrom(1024)
        data2 = float(data2[0:data2.find("\n")])
        pos2 = (data2-POSITION_OFFSET)/POSITION_OFFSET*SENSIBILITY

############################################################################################################################################


############################################################################################################################################
# MAIN
###############
def main():
    global PATH, FPSCLOCK, DISPLAYSURF, CURSOR, results_file, pos1, pos2, thread_alive, START, sock_envoi
    results_str=""
    file_name=""
    pos1=0.0
    pos2=0.0
        
    t = threading.Thread(group=None, target=receive_data, args = ())
    t.start()

    #Starting positions of cursor and path
    Y_PATH= -PATH_LENGTH_TRAINING
    X_POS_CURSOR = WINDOW_WIDTH/2



    # Generate the cursor and path objects
    generatePATH()
    generateCURSOR(CURSOR_WIDTH, CURSOR_LENGTH)



    #Synchronization of the 2 subjects
    while START == False:
        if time.time() >= float(sys.argv[3]):
            START = True

    #Sending signal to start registering data on the robot
    if SUJET==1:
	sock_envoi.sendto("START\0", ("10.0.0.2", UDP_PORT3))


    while True: #main loop

        #Refresh the base display
        DISPLAYSURF.fill(GREY)

        #Refresh the path position
        DISPLAYSURF.blit(PATH, (0,Y_PATH))
	#DISPLAYSURF.blit(OBSTACLE_SURF, (0, Y_PATH))
        Y_PATH += DEPL
        
        if Y_PATH >= WINDOW_LENGTH: #Stops the program when the path is finished
            terminate()
            
        checkForQuit()


        #Update cursor position

        OLD_X_POS_CURSOR = X_POS_CURSOR

	pos_moy = (pos1 + pos2 )/2

        try:
            X_POS_CURSOR = WINDOW_WIDTH/2*(1 - pos_moy)
        except:
            X_POS_CURSOR = OLD_X_POS_CURSOR	

	#print X_POS_CURSOR
        DISPLAYSURF.blit(CURSOR, (X_POS_CURSOR-CURSOR_WIDTH/2, Y_POS_CURSOR-CURSOR_LENGTH/2))
        

        #Refresh 
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    return 0;
############################################################################################################################################


############################################################################################################################################
#TERMINATE
##########
def terminate():
    global thread_alive
    if SUJET==1:
	sock_envoi.sendto("STOP\0", ("10.0.0.2", UDP_PORT3))
	sock_envoi.close()
    thread_alive = False
    pygame.quit()
    sys.exit()
############################################################################################################################################


############################################################################################################################################
#CHECK FOR QUIT
###############
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
############################################################################################################################################


############################################################################################################################################
#GENERATE PATH
##############
def generatePATH():
    global PATH
    PATH=pygame.Surface((PATH_WIDTH, PATH_LENGTH_TRAINING))
    PATH.fill(WHITE)

    #Generate the path assembling predefined subparts, and update the reference vector
    TYPE = 0
    SUBTYPE = 0
    scenario_number= sys.argv[1]
    scenario_file_name = "../scenarios/SCENARIO_" + scenario_number + ".txt"
    scenarioFile = open(scenario_file_name,'r')
    Y_POS = PATH_LENGTH_TRAINING
    limite = PART_LENGTH_FORK
    partLength = 0 
    partWithObstacle = 0  

    # The loop is reversed to start at the bottom of the path's surface ( = at the start)
#------------------------------------  
    if  (100 <= int(scenario_number) and int(scenario_number) < 300): #Scenarii 101-300 : Trials with obstacles
        while Y_POS > 0:
            if Y_POS == PATH_LENGTH_TRAINING: #Impose 2 sec of straight line at the start of the path
                TYPE = 0
                SUBTYPE = 0
                partLength = PART_DURATION_START*VITESSE 
            elif Y_POS <= limite: #Impose a straight line at the end of the path
                TYPE = 0
                SUBTYPE = 0
                partLength = Y_POS
            else:   #Read the scenario file to build the path according to the predetermined sequency
                line = scenarioFile.readline()
                TYPE     = int( line[ line.find("_TYPE") + 6 ])
                SUBTYPE  = int( line[ line.find("_SUBTYPE") + 9  ]) 
                partLength = PART_LENGTH_BODY           
                if (TYPE == 1 or TYPE == 2) :
                    partLength = DUREE_COURTE*VITESSE
                elif (TYPE == 3 or TYPE == 4):
                    partLength = DUREE_LONGUE*VITESSE

            try:
                generate_PART_Obstacles(PATH, partLength, Y_POS - partLength, TYPE, SUBTYPE)
            except:
                print "Failed to generate the path"
 #           try:
 #               generatePositionVector_Obstacles(partLength, Y_POS - partLength, TYPE, SUBTYPE)
 #           except:
#                print "Failed to generate the position vector"
                
            Y_POS = Y_POS - partLength #Decrement

    else:
	print "Wrong scenario - please use scenario 101 to 300 for training"
	terminate()
             

    scenarioFile.close() #Close the scenario file at the end of the while loop


    #Create file with path position, synchronised for aquisition frequency"
    path_file_name = "../path/PATH_TRAINING_scenario_" + scenario_number + "_subject_" + str(SUJET) + ".txt"
    path_file = open(path_file_name, 'w')
    
	

    for i in range(0, len(PATH_POS_TRAINING)):
	line = str(i) + "\t" + str(PATH_POS_TRAINING[len(PATH_POS_TRAINING)-i-1]) + "\n"
	path_file.write(line)
            

    path_file.close()


############################################################################################################################################


############################################################################################################################################
# GENERATE CURSOR
#################
def generateCURSOR(CURSOR_WIDTH, CURSOR_LENGTH): #generate the cursor shape
    global CURSOR
    CURSOR = pygame.Surface((CURSOR_WIDTH,CURSOR_LENGTH), pygame.SRCALPHA)
    CURSOR.fill((0,0,0,0))
    pygame.draw.ellipse(CURSOR, GREEN, (0,0,CURSOR_WIDTH,CURSOR_LENGTH))
############################################################################################################################################


############################################################################################################################################
# FUNCTIONS - TRIAL : OBSTACLES
############################################################################################################################################


############################################################################################################################################
#GENERATE PART - OBSTACLES
##########################
def generate_PART_Obstacles(SURFACE, partLength, Y_POS, TYPE, SUBTYPE): #generate the different kind of subparts
    MILIEU= PART_WIDTH/2
    GAUCHE= MILIEU - SUBTYPE*PART_WIDTH/20
    DROITE= MILIEU + SUBTYPE*PART_WIDTH/20
    marge = 4*LINE_WIDTH_BOLD
    milieu = float(MILIEU)
    gauche= float(GAUCHE)
    droite = float(DROITE)


#------------------------------------- #
    
    if TYPE == 0: #Ligne droite
	#pygame.draw.line(SURFACE, LIGHTGREY, (MILIEU, 0+ Y_POS), (MILIEU, partLength + Y_POS), LINE_WIDTH_BOLD)
	pygame.draw.line(SURFACE, BLACK    , (MILIEU, 0+ Y_POS), (MILIEU, partLength + Y_POS), LINE_WIDTH)
	for i in range(Y_POS, Y_POS + partLength):
	    PATH_POS_TRAINING[i]=milieu
          
      
    elif (TYPE == 1 or TYPE == 3):  #sinusoide gauche (1 : courte, 3: longue)
	for i in range(0 + Y_POS, partLength + Y_POS):
	    X = MILIEU + (MILIEU-GAUCHE)*(math.cos(float((i - Y_POS))/float(partLength)*2.0*3.14159) - 1)/2
	    Y = i
	    #pygame.draw.line(SURFACE, LIGHTGREY , (X,Y), (X,Y), LINE_WIDTH_BOLD)
	    pygame.draw.line(SURFACE, BLACK     , (X,Y), (X,Y), LINE_WIDTH)
	    PATH_POS_TRAINING[i]=milieu + (milieu-gauche)*(math.cos(float((i - Y_POS))/float(partLength)*2.0*3.14159) - 1)/2
               

    elif (TYPE == 2 or TYPE == 4):  #sinusoide droite (2 : courte, 4: longue)
	for i in range(0 + Y_POS, partLength + Y_POS):
	    X = MILIEU - (MILIEU-GAUCHE)*(math.cos(float((i - Y_POS))/float(partLength)*2.0*3.14159) - 1)/2
	    Y = i
	    #pygame.draw.line(SURFACE, LIGHTGREY , (X,Y), (X,Y), LINE_WIDTH_BOLD)
	    pygame.draw.line(SURFACE, BLACK     , (X,Y), (X,Y), LINE_WIDTH)
	    PATH_POS_TRAINING[i]=milieu - (milieu-gauche)*(math.cos(float((i - Y_POS))/float(partLength)*2.0*3.14159) - 1)/2


############################################################################################################################################


if __name__ == '__main__':
    main()


