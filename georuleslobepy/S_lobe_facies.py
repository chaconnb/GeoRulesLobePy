# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
  
"""
import numpy as np

from georuleslobepy.S_MapPropXY import PropXY
from georuleslobepy.S_MapPropZX import PropXZ


def grid_lobe(lobe_thi,length,wmax,cellsize_z,cell_size,tmax,global_property,mud_prop,n_cell_mud,mud_layer,a1,a2):

    """
    Rasterizes lobe thickness and property trends into a 3D grid, including mud layers on top.

    This function generates a 3D grid representation of a single lobe, incorporating facies properties, 
    vertical resolution, and mud deposition. It converts the thickness and property maps into 
    a voxel-based volume.

    Parameters
    ----------
    lobe_thi : ndarray
        2D array of lobe thickness values (XY plane).
    length : int
        Maximum lobe length in meters.
    wmax : int
        Maximum lobe width in meters.
    cellsize_z : float
        Vertical resolution (grid cell size along the Z-axis).
    cell_size : float
        Horizontal resolution (grid cell size in both X and Y directions).
    tmax : int
        Maximum lobe thickness in meters.
    global_property : float
        Target global proportion of the modeled facies (as a decimal, e.g., 0.6 for 60%).
    mud_prop : float
        Proportion of mud facies within the mud layer.
    n_cell_mud : int
        Number of vertical mud cells to place on top of each lobe element.
    mud_layer : bool
        Whether to include a mud layer on top of the lobe (True or False).
    a1 : float
        Relative position of maximum lobe width along the length (used for facies trend alignment).
    a2 : float
        Relative position of maximum lobe thickness along the length (used for facies trend alignment).

    Returns
    -------
    lobe_grid : ndarray
        3D array representing the voxelized lobe with assigned facies properties and mud layers.

    """
    
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
 