#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 19:03:15 2020

Simple program to read the time to fix data and calculate the euclidean distance, cosin distance,
manhattan distance, pearson index, jaccard index, KL divergence and JS divergence.

@author: harryzhao
"""

__author__ = "Group 03, CS 212, Lanzhou University"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "ZhaoHaoran"
__email__ = "zhaohr18@lzu.edu.cn"
__status__ = "Experimental"

import pandas as pd
import numpy as np
import random
import scipy.stats


def clean_data(data):
    """
    Clean the dirty data(NaN)
    """
    data.fillna(0) # clean the wrong data


def euclidean(p,q):
    """
    Calculate the euclidean distance
    """
    same = 0
    for i in p:
        if i in q:
            same +=1
    e = sum([(p[i] - q[i])**2 for i in range(same)])
    return 1/(1+e**.5)


def cosin_distance(vector1, vector2):
    """
    Calculate the cosin distance
    """
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


def manhattan(p,q):
    """
    Calculate the manhattan distance
    """
    same = 0
    for i in p:
        if i in q:
            same += 1
    n = same
    vals = range(n)
    distance = sum(abs(p[i] - q[i]) for i in vals)
    return distance


def pearson(p,q):
    """
    Calculate the pearson index
    """
    x=np.array(p)
    y=np.array(q)
    x_=x-np.mean(x)
    y_=y-np.mean(y)
    d=np.dot(x_,y_)/(np.linalg.norm(x_)*np.linalg.norm(y_))
    return d


def jaccard(p,q):
    """
    Calculate the jaccard index
    """
    x=np.array(p)
    y=np.array(q)
    up=np.double(np.bitwise_and((x != y),np.bitwise_or(x != 0, y != 0)).sum())
    down=np.double(np.bitwise_or(x != 0, y != 0).sum())
    d=(up/down)
    return d
    

def KL(p,q):
    """
    Calculate the KL distance
    """
    x=np.array(p)
    y=np.array(q)
    return scipy.stats.entropy(x, y)


def JS_divergence(p,q):
    """
    Calculate the JS divergence
    """
    x=np.array(p)
    y=np.array(q)
    M=(x+y)/2
    return 0.5*scipy.stats.entropy(x, M)+0.5*scipy.stats.entropy(y, M)


def main():
    file_path1 = input("data1 path>>> ")
    data1 = pd.read_csv(file_path1, header=None, index_col = [0])
    file_path2 = input("data2 path>>> ")
    data2 = pd.read_csv(file_path2, header=None, index_col = [0])
    
    clean_data(data1)
    clean_data(data2)
    d1 = data1[1].tolist()
    d2 = data2[1].tolist()
    for i in d1:
        if i == 0:
            d1.remove(i)
    for i in d2:
        if i == 0:
            d2.remove(i)        

    if len(d1) > len(d2):
        d1 = random.sample(d1, len(d2))
    else:
        d2 = random.sample(d2, len(d1))

    d3 = sorted(d1)
    d4 = sorted(d2)

    print("jaccard: " + str(jaccard(d3, d4)))
    print("euclidean: " + str(euclidean(d3, d4)))
    print("cosin distance: " + str(cosin_distance(d3, d4)))
    print("manhattan distance: " + str(manhattan(d3, d4)))
    print("pearson: " + str(pearson(d3, d4)))
    print("KL: " + str(KL(d3, d4)))
    print("JS_divergence: " + str(JS_divergence(d3, d4)))


if __name__ == "__main__":
    main()
      