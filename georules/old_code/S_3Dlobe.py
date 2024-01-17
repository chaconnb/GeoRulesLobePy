#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

Function to rasterize input properties and mud top of single lobe
Input:
    lobe_thi = array with lobe thickness
    lobe_prop = array with lobe properties
    n_cell_mud = the number of mud cells on the top of the lobe.
    mup_prop = property of the mud layer
    grid_cellsize = cell size of the grid
    n_column = this is equivalent to lenght_new in code S_ProbMap (number of columns of the lobe- x direction)
    n_row = this is quivalent to wmax_new in code S_ProbMap (number of rows of the lobre - y direction)
    mud_layer = if mud_layer == 1, it means the lobe output has mud layer if mud layer != 1 it means lobe output doesn't have mud layer
    
return:
    lb = 3d array with lobe and lobe properties

"""
import numpy as np 



def grid_1lobe(lobe_thi,lobe_prop,n_cell_mud,mud_prop,grid_cellsize,n_column, n_row, mud_layer):
    
    ## find max value of thickness
    max_element = np.max(lobe_thi)


    ## create numpy array of dimensions nx by ny by nz
    column = int(n_column) #nx
    row = int(n_row)  #ny
    cellsize_z =grid_cellsize
    nz = int(round(max_element,2)/cellsize_z)
    
    lobe_grid = np.zeros((column,row,nz))
    
    #lobe gridding + property 

    #nz_values = np.linspace(cellsize_z,max_element,nz).tolist()
    nz_values = np.linspace(0, max_element-cellsize_z, nz)

    

    for i in range(column):
        for j in range(row):
            element1 = lobe_thi[j][i]  #  2D array with thickness
            element2 = lobe_prop[j][i] #  2D array with properties
            for k in range(nz):
                if element1>nz_values[k]:
                    lobe_grid[i][j][k] = element2
                    
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
                    
                            if z_value < nz:
                                lobe_grid[i][j][z_value]=mud_prop
                   
    return(lobe_grid)
    
               