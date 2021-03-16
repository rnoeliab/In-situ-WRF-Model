#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:51:03 2020

@author: noelia
"""

import numpy as np
import pandas as pd
import os
import unicodedata
  
##### remove accents 
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

def path(ouput):
    if not os.path.exists(ouput):
        os.makedirs(ouput)
    return ouput

cetesb_stations = pd.read_csv("path of the excel file where the coordinates of the CETESB stations are found", encoding='utf-8')

inputt ='path where the extracted WRF-CETESB data is located'
name_out = str(input("cetesb_wrf files [mecanismo]_[regional/local]: ")) ### only if is necessary!! you can delete this line
INPUT = inputt+name_out+'/'
OUTPUT = path("output path to save created files")

# get a list
listdir = os.listdir(INPUT)

variables = ['rh','tc','wd','ws','press']
poluentes = ['co','no','no2','o3','pm25','pm10']
var_swd = ['rh','tc','ws','press']

for index,i in enumerate(cetesb_stations.code):
    print(strip_accents(cetesb_stations["name"][index]), i)   
    name_station = strip_accents(cetesb_stations["name"][index]).replace('.','_').replace('-','_').replace(' ','_')

 ######################################################## reading the wrf model files ##################################################################
    station_wrf = str(i)+"_wrfout4.dat"
    if str(station_wrf) in listdir:
        by_wrf = pd.read_csv(INPUT+str(station_wrf))
    #    by_wrf = by_wrf.loc[3:len(by_wrf)-23].reset_index(drop=True)
        by_wrf[by_wrf == 0.0] = np.nan
        start = by_wrf['local_date'][3][0:19]
        end = by_wrf['local_date'][len(by_wrf)-1][0:8]+str(int(by_wrf['local_date'][len(by_wrf)-1][8:10])-1) + " 23:00:00"
        
        serie_time = pd.date_range(start=start, end=end, freq="H")
        serie_time = pd.DataFrame(serie_time, columns=["date"])
        serie_time["date"] = serie_time["date"].dt.strftime("%Y-%m-%d")

        end1 = by_wrf['local_date'][len(by_wrf)-1][0:10] + " 00:00:00"
        by_wrf = by_wrf.loc[(by_wrf['local_date']>=start) & (by_wrf['local_date']<=end1)]
        by_wrf = by_wrf.reset_index(drop=True)
        for v in range(len(variables)):
            serie_time["wrf_"+str(variables[v])] = by_wrf[str(variables[v])]            
        for p in range(len(poluentes)):
#                print(by_wrf[v][count],by_wrf[str(poluentes[p])][count])
            serie_time["wrf_"+str(poluentes[p])] = by_wrf[str(poluentes[p])]
    else:
        pass

######################################################## reading pollutants data from cetesb  ##################################################################
    station_pol_cetesb = "all_photo_"+str(i)+".csv"
    if str(station_pol_cetesb) in listdir:
        by_cetestb_pol = pd.read_csv(INPUT+str(station_pol_cetesb))
        by_cetestb_pol = by_cetestb_pol.loc[(by_cetestb_pol['date']>=start) & (by_cetestb_pol['date']<=end)]
        by_cetestb_pol = by_cetestb_pol.reset_index(drop=True)
        by_cetestb_pol[by_cetestb_pol == 0.0] = np.nan
        for p in range(len(poluentes)):
#                print(by_cetestb[str(variables[v])][count])
            serie_time[str(poluentes[p])] = by_cetestb_pol[str(poluentes[p])]
    else:
        pass               
#################################################### reading meteorological  data from cetesb  ##################################################################
    station_cetesb = "all_met_"+str(i)+".csv"
    if str(station_cetesb) in listdir:
#        print(i, station_cetesb)
        cetestb = pd.read_csv(INPUT+str(station_cetesb))
        by_cetestb = cetestb.loc[(cetestb['date']>=start) & (cetestb['date']<=end)]
        by_cetestb = by_cetestb.reset_index(drop=True)
        by_cetestb["wd"][by_cetestb["wd"] == 888] = np.nan       
        by_cetestb["wd"][by_cetestb["wd"] == 777] = np.nan 
        by_cetestb["ws"][by_cetestb["ws"] == 0.0] = np.nan
        for v in variables:
            serie_time[str(v)] = by_cetestb[str(v)]
#            print(by_cetestb[str(variables[v])])
    else:
        pass
############################################################### saving the data by each station ##################################################################
    print("saving the data")
    serie_time.to_csv(OUTPUT+str(name_station)+".csv",index = False)

