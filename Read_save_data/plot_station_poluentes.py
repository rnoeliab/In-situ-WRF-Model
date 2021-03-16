#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:30:22 2020

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

INPUT ='path where the pollutants data was saved by station'
OUTPUT = path("output path to save created files")

listdir = os.listdir(INPUT)

############################################## reading the data ############################################
new_list_o3 = [i for n,i in enumerate(listdir) if i not in ['Congonhas.csv','Marg_Tiete_Pte_Remedios.csv']]
a = ['Cubatao_Vale_do_Mogi.csv','Capao_Redondo.csv','Santana.csv','Pico_do_Jaragua.csv','Cid_Universitaria_USP_Ipen.csv','Santos_Ponta_da_Praia.csv']
new_list_co = [i for n,i in enumerate(listdir) if i not in a]
new_list_no = [i for n,i in enumerate(listdir) if i not in ['Santo_Amaro.csv','Santana.csv']]

################################### creating the figures ########################################
fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_o3):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
#################################### Ozone ####################################    
    ax = fig.add_subplot(5,3,n+1)
    data.plot(x = 'date', y ='o3', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_o3', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,210])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("$O_{3}$ ($\mu g/m^{3}$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 3.5), fontsize=25)
plt.savefig(OUTPUT+'stations_ozono.png',bbox_inches='tight')
plt.show()

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_co):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################# carbon monoxide  #############################    
    ax = fig.add_subplot(4,3,n+1)
    data.plot(x = 'date', y ='co', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_co', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,4.0])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("CO ($ppmv$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 0.5), fontsize=25)
plt.savefig(OUTPUT+'stations_co.png',bbox_inches='tight')
plt.show()


fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_no):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################# nitrogen oxides ##############################    
    ax = fig.add_subplot(5,3,n+1)
    data.plot(x = 'date', y ='no', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_no', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,450])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("NO ($\mu g/m^{3}$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 3.5), fontsize=25)
plt.savefig(OUTPUT+'stations_no.png',bbox_inches='tight')
plt.show()

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_no):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################ nitrogen dioxide #############################    
    ax = fig.add_subplot(5,3,n+1)
    data.plot(x = 'date', y ='no2', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_no2', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,150])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("$NO_{2}$ ($\mu g/m^{3}$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 3.5), fontsize=25)
plt.savefig(OUTPUT+'stations_no2.png',bbox_inches='tight')
plt.show()

fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_no):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    data['nox'] = data['no'] + data['no2']
    data['wrf_nox'] = data['wrf_no'] + data['wrf_no2']
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################# nox #############################
    ax = fig.add_subplot(5,3,n+1)
    data.plot(x = 'date', y ='nox', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_nox', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,600])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("$NO_{x}$ ($\mu g/m^{3}$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 3.5), fontsize=25)
plt.savefig(OUTPUT+'stations_nox.png',bbox_inches='tight')
plt.show()


  
fig = plt.figure(figsize=(30,21))
for n,i in enumerate(new_list_no):
    data = pd.read_csv(INPUT+i)
#    data = data.loc[0:311]
    day = []
    for t in range(len(data['date'])//24):
        day.append(data["date"][t*24][5:10])
############################# Fine Particulate Material  ###########################  
    ax = fig.add_subplot(5,3,n+1)
    data.plot(x = 'date', y ='pm25', color = 'black', marker = '*', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'CETESB')
    data.plot(x = 'date', y = 'wrf_pm25', color = 'red', marker = 'v', markersize = 5, linewidth  = 1.5, ax=ax, sharey=True, sharex=True, legend = False, label = 'WRF')
    ax.axis([-1,len(data),0,80])
    ax.set_xticks(np.linspace(0,len(data)-1,int(len(data['date'])/24)+1))
    ax.set_xticklabels(day)
    ax.set_ylabel("$PM_{2.5}$ ($\mu g/m^{3}$)",fontsize=25)
    ax.set_xlabel("Time (Days)", fontsize=25)
    ax.set_title(i[:-4].replace('_',' ')+" Station",fontsize=25)
    plt.yticks(size = 20)
    plt.xticks(size = 20,rotation=45)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3.0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.legend(bbox_to_anchor=(1.4, 3.5), fontsize=25)
plt.savefig(OUTPUT+'stations_pm25.png',bbox_inches='tight')
plt.show()

