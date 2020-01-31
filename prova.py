#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 23:40:12 2020

@author: cappiello
"""

import csv

c="dataset/getNutritionalData.csv"

#df=pd.read_csv(c)
count=0
with open(c, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        count=count+1

print(count)