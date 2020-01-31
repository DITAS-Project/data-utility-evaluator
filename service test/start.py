#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 08:26:16 2020

@author: cappiello
"""
import DQEvaluator
import DUEunzip
import json
import pandas as pd
import os
import requests
import csv

def start(BLUEPRINT_PATH):

#BLUEPRINT_PATH = 'blueprint.json'

        CONCRETE_ID = '_id'
        CONCRETE_ABSTRACT_PROPERTIES = 'DATA_MANAGEMENT'
        INT_STRUCT = 'INTERNAL_STRUCTURE'
        OUT_DATA = 'Testing_Output_Data'
        METHOD_ID = 'method_id'
        ZIP_Data = 'zip_data'


#with open(BLUEPRINT_PATH) as bp_file:
        bp = json.loads(BLUEPRINT_PATH)
        #bp=BLUEPRINT_PATH
        methodnames = []
        zipdata=[]
        for method in bp[INT_STRUCT][OUT_DATA]:
                methodnames.append(method[METHOD_ID])
                zipdata.append(method[ZIP_Data])
    
        c=methodnames[1]
        url = zipdata[1]
      #  print(url)

        method2=DUEunzip.DUEunzip(url)
        dimensions = DQEvaluator.DQEvaluator(method2) #, attribute_list=attributes)
#dimensions["URL"] = method


        return(dimensions)
