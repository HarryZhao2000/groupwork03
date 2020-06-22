#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

__author__ = "Group03"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Group03"]
__version__ = "3"
__maintainer__ = "Linux maintainer"
__email__ = "zhaohr18@lzu.edu.com"
__status__ = "Experimental"


import csv
with open('/home/liuyz/桌面/test2(4).csv', encoding='gb18030') as f:

    f_csv = csv.reader(f)
    au={}
    ca={}
    for row in f_csv:
        if row[0] != None:
            if row[2] in au.keys():
                l=au.get(row[2])
                l.append(row[0])
                au[row[2]]=l
            else:
                l=[]
                l.append(row[0])
                au[row[2]]=l
            
            
    for key in au:
        l=[]
        v=au.get(key)
        l.append(len(v))
        l.append(len(set(v)))
        ca[key]=l
print('作者：[此人总共commit的次数，此人commit过的种类数]'+'\n',ca)


headers=['作者','commit总数','commit种类数']
rows=[]
for key in au:
    r=[]
    v=au.get(key)
    r.append(key)
    r.append(len(v))
    r.append(len(set(v)))
    rows.append(r)
with open('/home/liuyz/桌面/data3.csv','a+',encoding='gb18030') as d:
    f_csv = csv.writer(d)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    
