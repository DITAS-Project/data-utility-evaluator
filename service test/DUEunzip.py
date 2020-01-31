#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 19:19:07 2020

@author: cappiello
"""

import json
import requests
from zipfile import ZipFile
import csv

#BLUEPRINT_PATH = 'blueprint.json'

#CONCRETE_ID = '_id'
#CONCRETE_ABSTRACT_PROPERTIES = 'DATA_MANAGEMENT'
#INT_STRUCT = 'INTERNAL_STRUCTURE'
#OUT_DATA = 'Testing_Output_Data'
#METHOD_ID = 'method_id'
#ZIP_Data = 'zip_data'

def DUEunzip(methodURL):
#with open(BLUEPRINT_PATH) as bp_file:
#        bp = json.load(bp_file)
#methodnames = []
#zipdata=[]
#for method in bp[INT_STRUCT][OUT_DATA]:
#        methodnames.append(method[METHOD_ID])
#        zipdata.append(method[ZIP_Data])
    
    c='getNutritionalData'
    
    #methodURL="https://github.com/DITAS-Project/data-utility-evaluator/blob/master/dataset/getNutritionalData.zip?raw=true"
    
    url = methodURL
    r= requests.get(url)
    
    open('dataset/'+c+'.zip','wb').write(r.content)
      #  DQDUE.openzipfile('dataset/'+c+'.zip')
    
    with ZipFile('dataset/'+c+'.zip', 'r') as ZipObj: 
        ZipObj.extractall('dataset')
    
    data = json.load(open('dataset/'+c+'.json'))
    sample_data = open('dataset/'+c+'.csv', 'w')
    csvwriter = csv.writer(sample_data)
    count=0
    
    for item in data:
        if count == 0:
            header=item.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(item.values())
    sample_data.close()
    c='dataset/'+c+'.csv'
    return c

#return data
  #  datacsv = convertJSON(data)

    
    
    