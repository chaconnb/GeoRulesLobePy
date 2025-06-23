# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

"""
import math
import random
import numpy as np


def rot_angle(location,channel):
    """
    Computes the rotation angle between a horizontal line and the line formed by a source and a centroid.

    This function calculates the angle (in degrees) between a horizontal line and the line segment 
    connecting the sediment source (`channel`) and the lobe centroid (`location`). It simulates 
    uncertainty by sampling from a normal distribution centered on the calculated angle.

    Parameters
    ----------
    location : tuple or list of float
        Coordinates (x, y) of the lobe centroid.
    channel : tuple or list of float
        Coordinates (x, y) of the sediment source (e.g., feeder channel).

    Returns
    -------
    random_rotation_angle : float
        A random angle (in degrees) sampled from a normal distribution centered on the angle 
        formed between the centroid-source line and the horizontal axis.

    Notes
    -----
    - The calculated angle uses the arctangent of the vertical and horizontal differences.
    - A small epsilon (0.00001) is added to avoid division by zero when the x-difference is 0.
    - The sign of the vertical component (`c2`) is adjusted to reflect directionality.
    - The function samples from a normal distribution (mean = true angle, std = 1 degree)
      to introduce variability in lobe orientation, mimicking natural processes.

    """
    
    #Find rotation angle
    c1 = abs(location[0]-channel[0]) + 0.00001
    c2 = abs(location[1]-channel[1])
    
    if channel[1]<location[1]:
        c2 = -c2
    rotation_angle = math.degrees(math.atan(c2/c1))
    angle_nomal_distri = np.random.normal(rotation_angle,1,500) # generate normal distribution for the rotation_angle
    random_rotation_angle = random.choice(angle_nomal_distri)
    return (random_rotation_angle)
