# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
Function taken from: https://stackoverflow.com/questions/46657423/rotated-image-coordinates-after-scipy-ndimage-interpolation-rotate

"""
import numpy as np
from scipy.ndimage import rotate

def rot(image, xy, angle):
    """
        Rotates an image around its center and calculates the new location of a given point.

        This function rotates a 2D image by a specified angle around its center using bilinear 
        interpolation. It also computes the new coordinates of a specified point (e.g., a centroid) 
        after the rotation.

        Parameters
        ----------
        image : ndarray
            2D array representing the input image to be rotated.
        xy : ndarray or list or tuple
            Coordinates of a point (e.g., the centroid) in the original image, 
            given as a NumPy array or list in the form [x, y].
        angle : float
            Angle in degrees by which to rotate the image counterclockwise.

        Returns
        -------
        im_rot : ndarray
            Rotated image as a 2D array.
        new_rot_center : ndarray
            Coordinates [x1, y1] of the original point after rotation, 
            adjusted to the rotated image frame.

        Notes
        -----
        - The rotation is performed around the center of the image.
        - Coordinate transformations assume standard image indexing: origin at top-left,
        x increasing to the right, y increasing downward.
        - Uses `scipy.ndimage.rotate`, which may alter image dimensions depending on the angle.
    """
    im_rot = rotate(image,angle) 
    org_center = (np.array(image.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org = xy-org_center
    a = np.deg2rad(angle)
    new = np.array([org[0]*np.cos(a) + org[1]*np.sin(a),
            -org[0]*np.sin(a) + org[1]*np.cos(a) ])
    
    return im_rot, new+rot_center

