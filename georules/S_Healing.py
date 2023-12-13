# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:32:02 2023

@author: Nataly Chacon-Buitrago 
This function helps smooth the lobes when there is overlaping
"""

import numpy as np

def Healing_Factor(nx, ny, thick_update, bathymetry):
   
    bt = []  
    
    for i in range(0,nx):
        for j in range(0,ny):
            if thick_update[i,j]>0:
                bt.append(bathymetry[i,j]) 
                
    H_max  = np.max(bt)-np.min(bt)
    bt = np.array(bt)
    
    n = 0             
    Healing_1 = np.ones((nx,ny))
    if H_max != 0:
        healing_val = (1 -((bt - np.min(bt))/H_max)**(1.2))
        
        while n < len(bt):
            for i in range(0,nx):
                for j in range(0,ny):
                    if thick_update[i,j]>0:
                        Healing_1[i,j] = healing_val[n] 
                        n = n+1
                        
                        
    temp_sum = np.sum(thick_update)
    thick_updated_ = thick_update * Healing_1
    temp_sum_ = np.sum(thick_updated_)
    
    ratio_ = (temp_sum/temp_sum_)
    thick_updated_ = ratio_*thick_updated_
    bathymetry_updated = bathymetry+ thick_updated_

    
    return(bathymetry_updated)