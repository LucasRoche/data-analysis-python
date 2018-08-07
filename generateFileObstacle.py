# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 17:51:55 2017

@author: lucas
"""
import random
import matplotlib.pyplot as plt
import math

PATH_DURATION = 300
VITESSE = 120.0
PATH_LENGTH = int(PATH_DURATION*VITESSE)

PATH = [0]*PATH_LENGTH
TIME = [i/VITESSE for i in range(0, PATH_LENGTH)]
    
def main():
    for i in range(0,100):
        f_name = '../../lucas/scenarios/obstacle/SCENARIO_OBST_' + str(i+1)
        f = open(f_name, 'w')
        
        node_pos = 0
        next_node_pos = 0
        node_time = 0
        next_node_time = 0
        connec_type = 0
        while True:
            if node_time==0:
                next_node_pos = 0
                next_node_time = 2.0
                connec_type = 0
            else:
                while True:
                    next_node_pos = node_pos + random.sample([-30, -20, -10, 0, 10, 20, 30], 1)[0]
                    if(next_node_pos > -40 and next_node_pos < 40):
                        break
                next_node_time = node_time + random.sample([0.5, 1.5, 2.], 1)[0]
                if(next_node_time*VITESSE >= PATH_LENGTH):
                    break        
                connec_type = random.sample([0, 1, 2], 1)[0]     
            line = str(node_pos) + '\t' + str(next_node_pos) + '\t' + str(node_time) + '\t' + str(next_node_time) + '\t' + str(connec_type) + '\n'
            f.write(line)
            node_pos = next_node_pos
            node_time = next_node_time
        f.close()


        


def generate_ramp(p_start, p_stop, t_start, t_stop):
    pix_start = int(t_start*VITESSE)
    pix_stop = int(t_stop*VITESSE)
    for i in range(pix_start, pix_stop):
        PATH[i] = (p_start + float(p_stop - p_start)/float(pix_stop-pix_start)*float(i - pix_start))

def generate_sin(p_start, p_stop, t_start, t_stop):
    pix_start = t_start*VITESSE
    pix_stop = t_stop*VITESSE
    for i in range(int(pix_start), int(pix_stop)):
        PATH[i] = p_start + float(p_stop-p_start)*(1-math.cos(math.pi*float(i - pix_start)/float(pix_stop-pix_start)))/2
                
if __name__ == '__main__':
    main()