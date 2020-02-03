#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 12:07:51 2020

@author: cappiello
"""

#from zipfile import ZipFile
import json
#import requests
#import csv

BLUEPRINT_PATH = 'blueprint.json'

CONCRETE_ID = '_id'
CONCRETE_ABSTRACT_PROPERTIES = 'DATA_MANAGEMENT'
#INT_STRUCT = 'INTERNAL_STRUCTURE'
#OUT_DATA = 'Testing_Output_Data'
METHOD_ID = 'method_id'
att='attributes'
du='dataUtility'
T='type'
P='properties'
U='unit'
#ZIP_Data = 'zip_data'

name = ["volume", "accuracy", "completeness", "timeliness"]
with open(BLUEPRINT_PATH) as bp_file:
        bp = json.load(bp_file)
        bp_file.close()
dimensionnames = []
zipdata=[]
for d in bp[CONCRETE_ABSTRACT_PROPERTIES]:
    if (d[METHOD_ID] == "getNutritionalData"):
        for d1 in d[att][du]:
            for d3 in d1[P]:
                if (d3 == 'volume'):
                    tmp=d1[P][d3]['value']
                    print(tmp)
                    d1[P][d3]['value']=2000
                    bp_file=open(BLUEPRINT_PATH, "w+") 
                    bp_file.write(json.dumps(bp))
                    bp_file.close()
                   # print (d1[P][d3]['value'])
               # print (d3.keys())
                #if (d3==name[0]):
                #    
              # # for d4 in d1[P][d3]:
              #      print (d4)
              # if (d3 == 'volume'):
               #     print (d3[0])
          #      print(d1['properties']['volume'])
           # for d2 in d1[P]['timeliness']:
            #    print (d2)
                   
           
            
             #   dimensionnames.append(d1[att])
 #       zipdata.append(method[ZIP_Data])
    

print(dimensionnames)

#url = zipdata[1]
#r= requests.get(url)

#open('dataset/'+c+'.zip','wb').write(r.content)
#DQDUE.openzipfile('dataset/'+c+'.zip')

#with ZipFile('dataset/'+c+'.zip', 'r') as ZipObj: 
#        ZipObj.extractall('dataset')
    
#data = json.load(open('dataset/'+c+'.json'))

#print(data)