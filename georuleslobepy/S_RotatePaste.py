# -*- coding: utf-8 -*-
"""
@author: Nataly Chacon-Buitrago

"""
import numpy as np
from georuleslobepy.S_PasteArray import paste
from georuleslobepy.S_RotateArray import rot




def rot_paste(lenght,wmax,lobe,angle,Location,bathymetry_ini):
    
    """
    Rotates a lobe array and pastes it into a larger bathymetry array at a specified location.

    This function performs two main operations:
    1. Rotates the input lobe array around its centroid using a specified angle.
    2. Pastes the rotated lobe into the `bathymetry_ini` array at the target `Location`.

    The rotation is centered approximately at (length / 3 + 2, wmax / 2), which represents 
    a typical lobe centroid. The final pasting position is computed by offsetting the 
    rotated centroid from the desired global `Location`.

    Parameters
    ----------
    length : int
        Maximum length of the lobe.
    wmax : int
        Maximum width of the lobe.
    lobe : ndarray
        2D array representing the lobe geometry (e.g., thickness map).
    angle : float
        Rotation angle in degrees (counterclockwise).
    Location : tuple of int
        Target coordinates (column, row) where the lobe centroid should be placed 
        in the `bathymetry_ini` array.
    bathymetry_ini : ndarray
        2D array representing the background bathymetry or model grid.

    Returns
    -------
    thick_updated : ndarray
        Updated bathymetry array with the rotated lobe pasted in.
    column : float
        Column index in the bathymetry where the top-left corner of the rotated lobe was pasted.
    row : float
        Row index in the bathymetry where the top-left corner of the rotated lobe was pasted.

    Notes
    -----
    - This function uses the `rot` function for image rotation and the `paste` function to 
      embed the rotated lobe into the larger bathymetry grid.
    - The computed `column` and `row` offsets can be used to later retrieve or track the 
      pasted lobe's position in the larger domain.

    """
    
    x0,y0 =  np.round(lenght/3)+2,np.round(wmax/2)
    lobe_rot,(x1,y1) = rot (lobe, np.array([x0,y0]),angle) 

    column = Location[0] - x1 
    row = Location[1] - y1

    #Embed a small numpy array (lobearr) into a predifined block of a large numpy array
    thick_updated = paste(bathymetry_ini.copy(),lobe_rot,(int(row),int(column)))
    
    return(thick_updated,column,row)