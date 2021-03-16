#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 09:02:19 2020

@author: noelia
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# If the output folder is not created, then it will be created 
def path(ouput):
    if not os.path.exists(ouput):
        os.makedirs(ouput)
    return ouput

INPUT ='path where the meteorological data was saved by station'
OUTPUT = path("output path to save created files")

listdir = os.listdir(INPUT)

############################################## reading the data ############################################
sta_hu = ['Guarulhos_Pimentas','Capao_Redondo','Pico_do_Jaragua','S_Bernardo_Centro',
          'Santos_Ponta_da_Praia','Marg_Tiete_Pte_Remedios','Carapicuiba',
          'Pinheiros','Parque_D_Pedro_II','Cubatao_Vale_do_Mogi']

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(sta_hu):
    data = pd.read_csv(INPUT+i+'.csv')
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
################################### humidy ###################################
    ax = fig.add_subplot(5,2,n+1)
    data.plot(x = 'date', y ='rh', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_rh', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,110])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("Humidy ($\%$)",fontsize=30)
    ax.set_xlabel("Time (Days)", fontsize=30)
    ax.set_title(i.replace('_',' ')+" Station",fontsize=30)
    plt.yticks(size = 25)
    plt.xticks(size = 25,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.33, 3.5), fontsize=30)
plt.savefig(OUTPUT+'stations_humedad.png',bbox_inches='tight')
plt.show()

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(sta_hu):
    data = pd.read_csv(INPUT+i+'.csv')
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
################################## Temperature ################################    
    ax = fig.add_subplot(5,2,n+1)
    data.plot(x = 'date', y ='tc', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_tc', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),5,35])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("Temperature ($^\circ C$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=30)
    ax.set_title(i.replace('_',' ')+" Station",fontsize=30)
    plt.yticks(size = 25)
    plt.xticks(size = 25,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.33, 3.5), fontsize=30)
plt.savefig(OUTPUT+'stations_temperatura.png',bbox_inches='tight')
plt.show()

sta_vento = ['Guarulhos_Pimentas','Capao_Redondo','Pico_do_Jaragua','S_Bernardo_Centro',
          'Santos_Ponta_da_Praia','Marg_Tiete_Pte_Remedios','Carapicuiba',
          'Santana','Pinheiros','Parque_D_Pedro_II']

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(sta_vento):
    data = pd.read_csv(INPUT+i+'.csv')
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
#############################  wind speed #############################
    ax = fig.add_subplot(5,2,n+1)
    data.plot(x = 'date', y ='ws', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_ws', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,10])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("Wind Speed ($m/s$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=30)
    ax.set_title(i.replace('_',' ')+" Station",fontsize=30)
    plt.yticks(size = 25)
    plt.xticks(size = 25,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.33, 3.5), fontsize=30)
plt.savefig(OUTPUT+'stations_velocidad.png',bbox_inches='tight')
plt.show()
