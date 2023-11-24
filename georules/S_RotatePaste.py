# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:51:23 2023

@author: Nataly Chacon-Buitrago
Rotate+Paste
"""
import numpy as np
from S_PasteArray import paste
from S_RotateArray import rot




def rot_paste(lenght,wmax,lobe,angle,Location,bathymetry_ini):
    
    
    
    x0,y0 =  np.round(lenght/3)+2,np.round(wmax/2)
    lobe_rot,(x1,y1) = rot (lobe, np.array([x0,y0]),angle) 

    column = Location[0] - x1 
    row = Location[1] - y1

    #Embed a small numpy array (lobearr) into a predifined block of a large numpy array
    thick_updated = paste(bathymetry_ini.copy(),lobe_rot,(int(row),int(column)))
    
    return(thick_updated,column,row)