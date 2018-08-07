#!/usr/bin/env python

#Code written by Lucas Roche
#March 2015

import random
from generateObstacleFile import *

number_of_files = 100

for i in range(1, number_of_files + 1):
    scenario_number = i
    generateObstacleFile(scenario_number)

