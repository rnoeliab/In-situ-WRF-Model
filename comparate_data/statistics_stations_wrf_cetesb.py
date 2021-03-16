#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:06:09 2020

@author: noelia
"""
##############################################################################
#    This algorithm calculates the statistics for each CETESB station        #
#         For this you need to run the statistics_basic.py script            #
#                          before running this script                        #
##############################################################################

import numpy as np
import pandas as pd
import os
import statistics_basic as stat_basic
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

# If the output folder is not created, then it will be created 
def path(ouput):
    if not os.path.exists(ouput):
        os.makedirs(ouput)
    return ouput

cetesb_stations = pd.read_csv("/media/noelia/TOSHIBA EXT/doctorado/usp/in-situ/cetesb/DADOS_CETESB/point_station_cetesb/cetesb_station_2017_codes_qualr_fil.csv", encoding='utf-8')

INPUT ='path where the pollutants data was saved by station'
OUTPUT = path("output path to save created files")

#### Creating the statistics table of the CETESB stations 
stat = pd.DataFrame({"name":[]})

##### list of excel files 
listdir = os.listdir(INPUT+'/')

variables = ['rh','tc','wd','ws','press']
poluentes = ['co','no','no2','o3','pm25','pm10']
var_swd = ['rh','tc','ws','press']
 
for index,i in enumerate(cetesb_stations.code):
    print(strip_accents(cetesb_stations["name"][index]), i)   
    name_station = strip_accents(cetesb_stations["name"][index]).replace('.','_').replace('-','_').replace(' ','_')
    stat.loc[index,"name"] = name_station
    
 ######################################################## reading the wrf model files ##################################################################
    station_wrf = str(i)+"_wrfout4.dat"
    if str(station_wrf) in listdir:
        by_wrf = pd.read_csv(INPUT+'/'+str(station_wrf))      
        by_wrf = by_wrf.loc[3:len(by_wrf)].reset_index(drop=True)
        by_wrf[by_wrf == 0.0] = np.nan
        
        start = by_wrf['local_date'][0][0:10] + " 00:00:00"       
        end = by_wrf['local_date'][len(by_wrf)-1][0:8]+str(int(by_wrf['local_date'][len(by_wrf)-1][8:10])-1) + " 23:00:00"
        end1 = by_wrf['local_date'][len(by_wrf)-1][0:10] + " 00:00:00"
        
        by_wrf = by_wrf.loc[(by_wrf['local_date']>=start) & (by_wrf['local_date']<=end1)]      
        
        serie_time = pd.date_range(start=start, end=end, freq="H")
        serie_time = pd.DataFrame(serie_time, columns=["date"])
        serie_time["date"] = serie_time["date"].dt.strftime("%Y-%m-%d")

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
        cetestb_pol = pd.read_csv(INPUT+'/'+str(station_pol_cetesb))
        by_cetestb_pol = cetestb_pol.loc[(cetestb_pol['date']>=start) & (cetestb_pol['date']<=end)]
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
        cetestb = pd.read_csv(INPUT+'/'+str(station_cetesb))
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
############################################## CALCULATION OF THE STATISTICS USED  ##########################################################################
    print("Calculando la estadistica")
    
    for v in var_swd:
        stat.loc[index,"M0_"+str(v)] = np.nanmean(serie_time[str(v)])   
        stat.loc[index,"P0_"+str(v)] = np.nanmean(serie_time["wrf_"+str(v)])
        stat.loc[index,"MB_"+str(v)] = stat_basic.MB(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"NMB_"+str(v)] = stat_basic.NMB(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"ME_"+str(v)] = stat_basic.ME(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"NME_"+str(v)] = stat_basic.NME(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"IOA_"+str(v)] =stat_basic.ioa(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"corr_"+str(v)] = stat_basic.pearson(serie_time[str(v)],serie_time["wrf_"+str(v)])
        stat.loc[index,"RMSE_"+str(v)] = stat_basic.RMSE(serie_time[str(v)],serie_time["wrf_"+str(v)])

    for p in poluentes:        
        stat.loc[index,"M0_"+str(p)] = np.nanmean(serie_time[str(p)])   
        stat.loc[index,"P0_"+str(p)] = np.nanmean(serie_time["wrf_"+str(p)])
        stat.loc[index,"MB_"+str(p)] = stat_basic.MB(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"NMB_"+str(p)] = stat_basic.NMB(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"ME_"+str(p)] = stat_basic.ME(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"NME_"+str(p)] = stat_basic.NME(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"IOA_"+str(p)] =stat_basic.ioa(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"corr_"+str(p)] = stat_basic.pearson(serie_time[str(p)],serie_time["wrf_"+str(p)])
        stat.loc[index,"RMSE_"+str(p)] = stat_basic.RMSE(serie_time[str(p)],serie_time["wrf_"+str(p)])
    
print("finishhhhh!!!!!!!!!!!")
stat.to_csv(OUTPUT+"statistics_cetesb_by_station.csv",index = False)
