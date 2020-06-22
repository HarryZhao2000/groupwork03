#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

__author__ = "Group03"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Group03"]
__version__ = "3"
__maintainer__ = "Linux maintainer"
__email__ = "zhaohr18@lzu.edu.com"
__status__ = "Experimental"


import xlrd
import matplotlib.pyplot as plt
import numpy as np
book = xlrd.open_workbook('data_final.xlsx')
sheet = book.sheet_by_index(0)
rows = sheet.nrows
cols = sheet.ncols

i=1
areal=[]
alll=[]
averagel=[]
areatext=sheet.cell(i,9).value
alltext=sheet.cell(i,10).value
averagetext=sheet.cell(i,11).value
while areatext!="":
    print(areatext,"i:",i)
    areal.append(areatext)
    alll.append(alltext)
    averagel.append(averagetext)
    i+=1
    areatext=sheet.cell(i,9).value
    alltext=sheet.cell(i,10).value
    averagetext=sheet.cell(i,11).value

areadata=np.array(areal)
alldata=np.array(alll)
aaveragedata=np.array(averagel)

plt.plot(areadata, alldata,label='all')#, 'r--',
plt.legend()
plt.title("all")
plt.show()

plt.plot(areadata, aaveragedata,label='average')#, 'bs',label=''
plt.legend()
plt.title("average")
plt.show()