#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 20:08:19 2020

@author: noelia
"""

import requests
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
import os

def path(OUTPUT_CETESB):
    if not os.path.exists(OUTPUT_CETESB):
        os.makedirs(OUTPUT_CETESB)
    return OUTPUT_CETESB        


def my_to_datetime(date_str):
    if date_str[11:13] != '24':
        return pd.to_datetime(date_str, format='%d/%m/%Y_%H:%M')

    date_str = date_str[0:11] + '00' + date_str[13:]
    return pd.to_datetime(date_str, format='%d/%m/%Y_%H:%M') + \
           dt.timedelta(days=1)


def cetesb_data_download(OUTPUT_CETESB,cetesb_login, cetesb_password, 
                        start_date, end_date, 
                        parameter, station, csv=False):     
  
    login_data = {
        'cetesb_login': cetesb_login,
        'cetesb_password': cetesb_password
    }
    
    search_data = {
        'irede': 'A',
        'dataInicialStr':start_date,
        'dataFinalStr':end_date,
        'iTipoDado': 'P',
        'estacaoVO.nestcaMonto':station,
        'parametroVO.nparmt':parameter
    }
    
    with requests.Session() as s:
        url = "https://qualar.cetesb.sp.gov.br/qualar/autenticador"
        r = s.post(url, data=login_data)
        url2 = "https://qualar.cetesb.sp.gov.br/qualar/exportaDados.do?method=pesquisar"
        r = s.post(url2, data=search_data)
        soup = BeautifulSoup(r.content, 'lxml')
        
    data = []
    table = soup.find('table', attrs={'id':'tbl'})
    rows = table.find_all('tr')
    row_data = rows[2:]
    for row in row_data:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])    
        
    dat = pd.DataFrame(data)
           
    # Creating a complete df with all dates
    day1 = pd.to_datetime(start_date, format='%d/%m/%Y')
    day2 = pd.to_datetime(end_date, format='%d/%m/%Y') + dt.timedelta(days=1)
    all_date = pd.DataFrame(index=pd.date_range(day1.strftime('%m/%d/%Y'), 
                                                day2.strftime('%m/%d/%Y'),
                                                freq='H'))
    if len(dat) <= 1:
        dat = pd.DataFrame(columns=['day', 'hour', 'name', 'pol_name', 'units', 'val'])        
    else:    
        dat = dat[[3, 4, 6, 7, 8, 9]]
        dat.columns = ['day', 'hour', 'name', 'pol_name', 'units', 'val']
        dat['date'] = dat.day + '_' + dat.hour

        # Changing date type to string to datestamp
        dat['date'] = dat.date.apply(my_to_datetime)

        # Changing val type from string/object to numeric
        dat['val'] = dat.val.str.replace(',', '.').astype(float)

        # Filling empy dates
        dat.set_index('date', inplace=True)
       
    
    dat_complete = all_date.join(dat)
    file_name = str(parameter) + '_' + str(station) +' .csv'
    if csv:
        dat_complete.to_csv(OUTPUT_CETESB+file_name, index_label='date')
    else:
        return dat_complete

    
def all_met(OUTPUT_CETESB,cetesb_login, cetesb_password, start_date, end_date, station, csv_met=False):
    press = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 29, station)    
    tc = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 25, station)
    rh = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 28, station)
    ws = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 24, station)
    wd = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 23, station)
    radg = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 26, station)
    raduv = cetesb_data_download(OUTPUT_CETESB, cetesb_login, cetesb_password, start_date, end_date, 56, station)
    
    all_met_df = pd.DataFrame({
        'press':press.val,
        'tc': tc.val,
        'rh': rh.val,
        'ws': ws.val,
        'wd': wd.val,
        'radg':radg.val,
        'raduv':raduv.val
    }, index=tc.index)
    
    if csv_met:
        all_met_df.to_csv(OUTPUT_CETESB+'all_met_' + str(station) + '.csv',
                            index_label='date')
    else:
        return all_met_df    
