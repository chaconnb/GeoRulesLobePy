#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:39:27 2023

@author: Nataly Chacon-Buitrago
Function that gives new lobe's coordinates when rotated an angle
coord = array of coordinates [x, y ](lenght,wmax) of the lobe with no rotation
image = lobe arrary that with no rotation (lobe_image ->MAIN)
column_corner = Location[0] - x1  in S_rotateArray
row_corner = Location[1] - y1  in S_rotateArray
Modified from: https://stackoverflow.com/questions/46657423/rotated-image-coordinates-after-scipy-ndimage-interpolation-rotate

"""

import numpy as np
from scipy.ndimage import rotate


def rotate_coord(coord,angle,image, column_corner,row_corner):
    
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