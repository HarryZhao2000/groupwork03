#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:07:47 2020

@author: hurryzhao
"""

import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_excel('/Users/hurryzhao/Downloads/version-fixes.xlsx')
y=data['fix'][40:45]
x=data['version'][40:45]


# 线性回归拟合
x_n = sm.add_constant(x) #statsmodels进行回归时，一定要添加此常数项
model = sm.OLS(y, x_n) #model是回归分析模型
results = model.fit() #results是回归分析后的结果
 
#输出回归分析的结果
logfile = open(r'/Users/hurryzhao/summary.txt', 'w+')
print(results.summary(),file=logfile)
print('Parameters: ', results.params)
print('R2: ', results.rsquared)
logfile.close()

plt.figure()
plt.rcParams['font.sans-serif'] = ['Kaiti']  # 指定默认字体
plt.title(u"fixs-version")
plt.xlabel(u"version")
plt.ylabel(u"fix_num")
plt.axis([4, 6, 20000, 40000])
plt.scatter(x, y, marker="o",color="b", s=50)
plt.plot(x_n, y, linewidth=3, color="r")
plt.show()
