#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:14:00 2020

@author: noelia
"""
###############################################################################
#     Este algoritmo es para calcular "Mean Bias (MB)", "Mean Error (ME)",    # 
#         "Root Mean Square Error (RMSE), Normalized Mean Bias (NMB)",        #
#         "Normalized Mean Error (NME)", "Mean Normalized Bias (MNB)",        #
#        "Mean Normalized Error (MNE)", "Correlation Coefficient (r)",        #
#                     "Index of Agreement (IOA)"                              #
###############################################################################

import numpy as np

def MB(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    MB (float): Mean Bias
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    mb = np.nanmean(diff)
    
    return mb

def NMB(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    NMB (float): Normalized Mean Bias
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    nmb = (np.nansum(diff)/np.nansum(data_obs))*100
    
    return nmb

def ME(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    ME (float): Mean Error
    '''
    
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    me = np.nanmean(diff)
    
    return me

def NME(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    NME (float): Normalized Mean Error
    '''
    
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    nme = (np.nansum(diff)/np.nansum(data_obs))*100
    
    return nme

def RMSE(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    RMSE (float): Root Mean Square Error
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = np.power((data_model - data_obs), 2)
    rmse = np.sqrt(np.nanmean(diff))
    
    return rmse

def ioa(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    IOA (float): Index of Agreement
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    obs_mean = np.nanmean(data_obs)
    diff = np.power((data_model - data_obs), 2)
    a = np.nansum(diff)
    b = np.power((abs(data_model-obs_mean)+abs(data_obs-obs_mean)),2)
    c = np.nansum(b)
    ioa = 1 - (a/c)
    
    return ioa

def pearson(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    Pearson (float): Correlation Coefficient (R)
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    model_mean = np.nanmean(data_model)
    obs_mean = np.nanmean(data_obs)
    rest_obs = data_obs - obs_mean
    rest_model = data_model - model_mean 
    a = np.nansum(rest_model*rest_obs) 
    b =(np.nansum(np.power(rest_model,2)))*(np.nansum(np.power(rest_obs,2)))
    r = a/(np.sqrt(b))
    
    return r
    
############# estadistica para vientos: angulos mayor a 180 grados ############

def MB_hg180(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    MB_hg180 (float): Mean Bias to degree > 180
    '''

    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = (data_model - data_obs)
    ab = abs(1-(360/(abs(diff))))
    mb_hg180 = np.nanmean(diff)*ab
    
    return mb_hg180


def ME_hg180(data_model,data_obs):
    '''
    Parameters
    ----------
    data_obs : TYPE (float)
        DESCRIPTION. Datos observados o in-situ
    data_model : TYPE (float)
        DESCRIPTION. datos modelados

    Returns
    -------
    ME_hg180 (float): Mean Error to degree > 180
    '''
    
    data_obs = np.array(data_obs)
    data_model = np.array(data_model)
    diff = abs(data_model - data_obs)
    ab = abs(1-(360/diff))
    me_hg180 = np.nanmean(diff)*ab
    
    return me_hg180
