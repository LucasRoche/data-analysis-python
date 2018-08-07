# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:08:47 2017

@author: lucas
"""
from postTrait_Module import *
from Tkinter import *
from tkFileDialog import *

def main():
    root = Tk()
    root.withdraw()
    file_names = askopenfilenames(initialdir = '~/Documents/Manip')
    file_names = root.tk.splitlist(file_names)
    root.destroy()
    for file in file_names:
        DataClass = FileData(file)
        DataClass.getDataFromFile()
        DataClass.toCSV()
        

if __name__ == '__main__':
    main()