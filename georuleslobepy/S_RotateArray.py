# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:59:56 2023

@author: Nataly Chacon-Buitrago
Function taken from: https://stackoverflow.com/questions/46657423/rotated-image-coordinates-after-scipy-ndimage-interpolation-rotate
input:
    image =array with image we want to rotate
    xy = array with x and y coordinates in image of centroid - np.array([x0,y0])
    angle = angle that we want to rotate the image  
    
output: 
    im_rot = new rotated image
    new+rot_center = new coordinates for centroid when the array is rotated (x1,y1)

"""
import numpy as np
from scipy.ndimage import rotate

def rot(image, xy, angle):
    im_rot = rotate(image,angle) 
    org_center = (np.array(image.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org = xy-org_center
    a = np.deg2rad(angle)
    new = np.array([org[0]*np.cos(a) + org[1]*np.sin(a),
            -org[0]*np.sin(a) + org[1]*np.cos(a) ])
    return im_rot, new+rot_center

