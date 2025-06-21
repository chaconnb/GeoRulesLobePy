# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:53:38 2023

@author: Nataly Chacon-Buitrago
Function to find the angle formed by a horrizontal line and the line formed using source and centroid.
input:
 location= centroid
 channel = source of sediment
 
output :
    random rotation angle = Angle formed by a horrizontal line and the line formed using source and centroid

"""
import math
import random
import numpy as np


def rot_angle(location,channel):
    
    #Find rotation angel --  Hacer esto una funcion
    c1 = abs(location[0]-channel[0]) + 0.00001
    c2 = abs(location[1]-channel[1])
    
    if channel[1]<location[1]:
        c2 = -c2
    rotation_angle = math.degrees(math.atan(c2/c1))
    angle_nomal_distri = np.random.normal(rotation_angle,1,500) # generate normal distribution for the rotation_angle
    random_rotation_angle = random.choice(angle_nomal_distri)
    return (random_rotation_angle)
