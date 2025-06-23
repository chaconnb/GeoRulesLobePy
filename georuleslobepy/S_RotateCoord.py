#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nataly Chacon-Buitrago

"""

import numpy as np
from scipy.ndimage import rotate


def rotate_coord(coord,angle,image, column_corner,row_corner):
    """
    Computes the new coordinates of lobe points after rotating an image by a given angle.

    This function rotates the input image around its center using `scipy.ndimage.rotate`, 
    and calculates the new position of each point (coordinate) in `coord` after rotation. 
    It also accounts for the translation required to align the rotated image within a 
    larger array based on `column_corner` and `row_corner`.

    Modified from:
    https://stackoverflow.com/questions/46657423/rotated-image-coordinates-after-scipy-ndimage-interpolation-rotate

    Parameters
    ----------
    coord : array-like of shape (n, 2)
        Array of coordinates [x, y] corresponding to lobe points before rotation.
        Typically in the local coordinate system of the lobe image (length, width).
    angle : float
        Rotation angle in degrees (counterclockwise).
    image : ndarray
        2D array representing the unrotated lobe image (e.g., binary mask of the lobe).
    column_corner : float
        Offset in the x-direction to map the rotated image back into the global domain (Location[0] - x1).
    row_corner : float
        Offset in the y-direction to map the rotated image back into the global domain (Location[1] - y1).

    Returns
    -------
    new_coord : ndarray of shape (n, 2)
        New coordinates of the lobe points after rotation and global alignment.

    
    Notes
    -----
    - The image is rotated around its center, and coordinate transformations are done accordingly.
    - Offsets (`column_corner`, `row_corner`) are used to translate coordinates into a larger reference frame.
    - This is useful for tracking lobe geometry in composite sandbox models.
    """
    
    coord = np.array(coord)
    im_rot = rotate(image,angle)
    org_center = (np.array(image.shape[:2][::-1])-1)/2
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org_prueba = coord - org_center
    a = np.deg2rad(angle)
    new = np.array([org_prueba[:,0]*np.cos(a)+ org_prueba[:,1]*np.sin(a), -org_prueba[:,0]*np.sin(a)+ org_prueba[:,1]*np.cos(a)]).T
    new_coord = new+rot_center

    new_coord[:,0] = new_coord[:,0] + column_corner
    new_coord[:,1] = new_coord[:,1] + row_corner
    
    return(new_coord)