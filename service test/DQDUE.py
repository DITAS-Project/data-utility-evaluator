#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 18:18:03 2020

@author: cappiello
"""

#from zipfile import ZipFile
import json
import csv

#import requests, zipfile, StringIO
#r = requests.get(zip_file_url, stream=True)
#z = zipfile.ZipFile(StringIO.StringIO(r.content))
#z.extractall()
def main():
   # method="nutrional-data-ibm"
    
   # with ZipFile('dataset/nutritional.zip', 'r') as ZipObj: 
   #     ZipObj.extractall('dataset')
    
    data = json.load(open('dataset/getNutritionalData.json'))
    sample_data = open('dataset/getNutritionalData.csv', 'w')
    csvwriter = csv.writer(sample_data)
    count=0
    
    for item in data:
        if count == 0:
            header=item.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(item.values())
    sample_data.close()
    
#    csv_file = csv.writer(open('dataset/nutritional-data-ibm.csv', 'w', newline=''))
#    for item in data():
#        csv_file.writerow([item].values())

#    print(csv_file)
if __name__ == '__main__':
   main()