# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

Function to rasterize input properties and mud top of single lobe. 
    
return:
    lobe_grid = 3d array with lobe and lobe properties    
"""
import numpy as np

from georules.S_MapPropXY import PropXY
from georules.S_MapPropZX import PropXZ

###Input example:
#lobe_thi = lobe_image
#length = Value_4_lenght[0]
#wmax = Value_2_wmax[0]
#cellsize_z = Value_19_cellsize_z[0]
#cell_size = Value_6_cellsize[0]
#tmax = 2 #m
#global_property = 0.15 #global percentage of the property
#mud_prop = 0.10
#n_cell_mud = 2
#a1 =  Value_13_a1[0]
#a2 = Value_14_a2[0]


def grid_lobe(lobe_thi,length,wmax,cellsize_z,cell_size,tmax,global_property,mud_prop,n_cell_mud,mud_layer,a1,a2):
    
    ## Find max value of thickness
    max_element = np.max(lobe_thi)

    ## create numpy array of dimensions nx by ny by nz
    column = int(length/cell_size) #nx
    row = int(wmax/cell_size) #ny
    nz = round(round(max_element,2)/cellsize_z)
    

    ## lobe_grid
    lobe_grid = np.zeros((column,row,nz))

    ## lobe gridding + property
    # thickness values 
    nz_values = np.linspace(0, max_element-cellsize_z, nz)
    # properties
    mapXY = PropXY(length,wmax,cell_size,a1,a2)
    mapZX = PropXZ(cellsize_z,tmax,length,cell_size)


    for i in range(column):
        for j in range(row):
            element1 = lobe_thi[j][i]  #  2D array with thickness
            for k in range(nz):
                if element1>nz_values[k]:
                    elementXY = mapXY[j][i]
                    elementZX = mapZX[k][i]
                    lobe_grid[i][j][k] = elementZX/global_property * elementXY +2 # I added 2 for visual purposes 
                
    # lobe + mud layer

    original_lobe_grid = lobe_grid.copy()
    
    if mud_layer == 1:
        
        for i in range (column):
            for j in range(row):
                for k in range(nz-1):
                    element1 = original_lobe_grid[i][j][k]
                    element2 = original_lobe_grid[i][j][k+1]
                    
                    if element1 != 0 and element2 ==0:
                        for n in range(0,n_cell_mud):
                            z_value = k+n
                            lobe_grid[i][j][z_value]= mud_prop +2

                    if k == nz-2:
                        element1 = original_lobe_grid[i][j][k]
                        element2 = original_lobe_grid[i][j][k+1]
                        
                        if element1 != 0 and element2 != 0:
                            for n in range(0,n_cell_mud):
                                z_value = k+n
                                lobe_grid[i][j][z_value]= mud_prop +2
                                
                        
    return(lobe_grid)
 