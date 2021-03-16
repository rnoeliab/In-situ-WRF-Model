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

def path(ouput):
    if not os.path.exists(ouput):
        os.makedirs(ouput)
    return ouput

inputt ='/media/noelia/TOSHIBA EXT/doctorado/usp/modelo/analisis_wrf/analisis_cada_estacion/'
dominio = str(input("1_dominio ou 2_dominio: "))
#name_out = str(input("write cetesb_wrf_[mecanismo]_[regional/local]: "))
name_out = str(input("qualar wrf files: "))
month = str(input("june or sep???: "))

INPUT = inputt+dominio+'/cetesb_wrf_cbmz_iag_ysu_2017/'+name_out+'/'+month+'/'
OUTPUT = path("/media/noelia/TOSHIBA EXT/doctorado/usp/modelo/figures/plot_cetesb_wrf/"+str(dominio)+'/cetesb_wrf_cbmz_iag_ysu_2017/plot_por_estacion/'+str(name_out)+"/"+str(month)+"/")

listdir = os.listdir(INPUT)

################################# Leyendo los datos ###########################
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
################################### humedad ###################################
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
################################## Temperatura ################################    
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
############################# velocidad de viento #############################
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

fig = plt.figure(figsize=(21,15))
for n,i in enumerate(sta_vento):
    data = pd.read_csv(INPUT+i+'.csv')
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################# direccion de viento #############################
    ax = fig.add_subplot(5,2,n+1)
    data.plot(x = 'date', y ='wd', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_wd', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,10])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("Wind Speed ($m/s$)",fontsize=19)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i.replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.25, 3.5), fontsize=20)
#plt.savefig(OUTPUT+'stations_direccion.png',bbox_inches='tight')
plt.show()
