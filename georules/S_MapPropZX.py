# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
This function builds the facies trend in the XZ axis. Best quality - rocks below. 
"""
import numpy as np

#example input
#cellsize_z = Value_19_cellsize_z[0]
#tmax = 2 #m
#length = Value_4_lenght[0]
#cell_size = Value_6_cellsize[0]



def PropXZ(cellsize_z,tmax,length,cell_size): 

    #z-axis
    #create list of z values:
    z_values = [0]
    i=cellsize_z

    while i < (tmax):
        i = i + cellsize_z
    
        z_values.append(i)
    
    # x-axis
    x_interval = [i for i in range(0,length, cell_size)]

    # create a grid of x and z values
    X_coord,Z_coord = np.meshgrid(x_interval,z_values)

    p = (Z_coord - np.min(Z_coord))/(np.max(Z_coord)- np.min(Z_coord))
    p = 1-p #best quality of the rock below
    
    return(p)