# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

"""
import numpy as np


def PropXZ(cellsize_z,tmax,length,cell_size): 

    """
    Builds a 2D facies trend array in the XZ (length–thickness) plane.

    This function generates a facies quality distribution along the X (length) and Z (thickness) 
    directions of the lobe. The trend typically assumes that the best facies quality is centered 
    in the middle of the lobe thickness and length.

    Parameters
    ----------
    cellsize_z : float
        Vertical resolution (cell size in the Z direction).
    tmax : int
        Maximum thickness of the lobe (in meters).
    length : int
        Total length of the lobe (in meters).
    cell_size : float
        Horizontal resolution (cell size in the X direction).

    Returns
    -------
    p : ndarray
        2D array representing facies trend 
        in the XZ plane.

    """

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