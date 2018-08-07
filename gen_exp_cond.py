# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 11:34:34 2018

@author: lucas
"""

from __future__ import print_function
import numpy as np
import random

packageNames = ('afex', 'lsmeans')

def balanced_latin_squares(n):
	l = [[((j/2+1 if j%2 else n-j/2) + i) % n + 1 for j in range(n)] for i in range(n)]
	if n % 2:  # Repeat reversed for odd n
		l += [seq[::-1] for seq in l]
	return l


def replace_conditions(A,cond):
    for i in range(len(A)):
        A[i]=cond[A[i]-1]
    return A


s = balanced_latin_squares(6)
Fth_val = [1.00, 2.5, 6.25]
Tth_val = [0.2, 0.5]
conditions = ["F:"+str(Fth_val[i])+"_T:"+str(Tth_val[j]) for i in range(len(Fth_val)) for j in range(len(Tth_val))]
conditions.append("HFOP")
conditions.extend(conditions)
conditions = range(1,7)
for e in s:
    print(e)
for e in s:
    A = replace_conditions(e,conditions)
    for i in range(len(A)):
        print(A[i]+";", end='')
    print("")
