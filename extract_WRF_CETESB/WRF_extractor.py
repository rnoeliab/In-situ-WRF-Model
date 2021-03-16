#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:05:08 2020

@author: noelia
"""
import wrf
from netCDF4 import Dataset
import glob
import pandas as pd
import qualar_py as qr

path_cetesb = 'path of the excel file where the coordinates of the CETESB stations are found'
path_input = 'wrfout files path'
### only if is necessary!! you can delete this line
name_file= str(input("wrfout file [mechanism]_[region/local]_[CLP]: " )) 

INPUT = path_input+name_file

path_out = 'output path to save created files'
OUTPUT_CETESB = qr.path(path_out+name_file)

# reading each wrfout
wrflist = [Dataset(i) for i in sorted(glob.glob(INPUT+"/wrfout_d01*"))]

# Extracting meteorological variables
print('extracting the data')
tc = wrf.getvar(wrflist, 'T2', timeidx=wrf.ALL_TIMES, method='cat')

print('moisture')
rh = wrf.getvar(wrflist, 'rh2', timeidx=wrf.ALL_TIMES, method='cat')

print('wind')
wind = wrf.getvar(wrflist, 'uvmet10_wspd_wdir', timeidx=wrf.ALL_TIMES, method='cat')
ws = wind.sel(wspd_wdir='wspd')
wd = wind.sel(wspd_wdir='wdir')

print('pressure')
psfc = wrf.getvar(wrflist, 'PSFC', timeidx=wrf.ALL_TIMES, method='cat')
hgt = wrf.getvar(wrflist, 'HGT', timeidx=wrf.ALL_TIMES, method='cat')

# Extracting polutants vvariabls
print('gases')
o3 = wrf.getvar(wrflist, 'o3', timeidx=wrf.ALL_TIMES, method='cat')
no = wrf.getvar(wrflist, 'no', timeidx=wrf.ALL_TIMES, method='cat')
no2 = wrf.getvar(wrflist, 'no2', timeidx=wrf.ALL_TIMES, method='cat')
co = wrf.getvar(wrflist, 'co', timeidx=wrf.ALL_TIMES, method='cat')

print('PM')
pm25 = wrf.getvar(wrflist, 'PM2_5_DRY', timeidx=wrf.ALL_TIMES, method='cat')
pm10 = wrf.getvar(wrflist, 'PM10', timeidx=wrf.ALL_TIMES, method='cat')

# Retrieving values from surface
print('extracting data for the surface')
o3_s = o3.isel(bottom_top=0)
no_s = no.isel(bottom_top=0)
no2_s = no2.isel(bottom_top=0)
co_s = co.isel(bottom_top=0)
pm25_s = pm25.isel(bottom_top=0)
pm10_s = pm10.isel(bottom_top=0)

# Changing ppm to ug/m3
# [ug/m3] = [ppm] * P * M_i / (R * T) 
# R = 8.3143 J/K mol
# P in Pa
# T in K
# WRF-Chem gas units in ppmv
print('converting units')
R = 8.3143
o3_u = o3_s * psfc * (16 * 3) / (R * tc)
no_u = no_s * psfc * (14 + 16) / (R * tc)
no2_u = no2_s * psfc * (14 + 2*16) / (R * tc)

# Reading file with station location points
cetesb_stations = pd.read_csv(path_cetesb+'cetesb_station_2017_codes_qualr.csv', encoding='utf-8')

# Locating stations in west_east (x) and north_south (y) coordinates
stations_xy = wrf.ll_to_xy(wrflist, latitude=cetesb_stations.lat, longitude=cetesb_stations.lon)

cetesb_stations['x'] = stations_xy[0]
cetesb_stations['y'] = stations_xy[1]

# Filter stations inside WRF domain
filter_dom = (cetesb_stations.x > 0) & (cetesb_stations.x < tc.shape[2]) & (cetesb_stations.y > 0) & (cetesb_stations.y < tc.shape[1])
cetesb_dom = cetesb_stations[filter_dom]

cetesb_dom.to_csv(path_cetesb+"/cetesb_wrf_position.csv",  index = False, encoding='utf-8')

# Downloading data from Cetesb

# Function to retrieve varaibles from WRF-Chem
def cetesb_from_wrf(i, to_local=True):
    wrf_est = pd.DataFrame({
    'date': tc.Time.values,
    'tc': tc.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values - 273.15,
    'rh': rh.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'ws': ws.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'wd': wd.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'press': psfc.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values/100,
    'hgt': hgt.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,                 
    'o3': o3_u.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'no': no_u.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'no2': no2_u.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'co': co_s.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'pm25': pm25_s.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'pm10': pm10_s.sel(south_north=cetesb_dom.y.values[i],
       west_east=cetesb_dom.x.values[i]).values,
    'code': cetesb_dom.code.values[i],
    'name': cetesb_dom.name.values[i]})
    if to_local:
        wrf_est['local_date'] = wrf_est['date'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    return(wrf_est)

# Extracting data and saving it in a dictionary
wrf_cetesb = {}

for i in range(0, len(cetesb_dom)):
    wrf_cetesb[cetesb_dom.name.iloc[i]] = cetesb_from_wrf(i)


# Exporting to csv
def cetesb_write_wrf(df):
    file_name = str(df.code[0]) + '_wrfout4.dat'
    df.to_csv(OUTPUT_CETESB+file_name, index=False, encoding='utf-8-sig')


for k, v in wrf_cetesb.items():
    print(v)
    cetesb_write_wrf(v)


wrf_dates = pd.DataFrame({
    'date': tc.Time.values
})

wrf_dates['date_local'] = wrf_dates['date'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
wrf_dates['date_qualar'] = wrf_dates['date_local'].dt.strftime('%d/%m/%Y')
wrf_dates.head()

cetesb_login = 'username CETESB'
cetesb_password = 'passwpord CETESB'
start_date = wrf_dates.date_qualar.values[0]    # %d/%m/%Y
end_date = wrf_dates.date_qualar.values[-1]

start_date

for i in cetesb_dom.code:
    print('Downloading pol ' + cetesb_dom.name[cetesb_dom.code == i].values + ' Station')
    qr.all_photo(OUTPUT_CETESB,cetesb_login, cetesb_password,
                        start_date, end_date, i, csv_photo=True)
    print('Downloading met ' + cetesb_dom.name[cetesb_dom.code == i].values + ' Station')
    qr.all_met(OUTPUT_CETESB,cetesb_login, cetesb_password,
                        start_date, end_date, i, csv_met=True)
      
