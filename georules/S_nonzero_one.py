#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
Convert all non-zero elements in a 2D array into 1
Input:
    arr: the array in which we want to convert all non-zero elements of the array to ones
    
"""


import numpy as np

def convert_nonzero_to_one(arr):
    new_arr = np.where(arr != 0, 1, 0)
    return new_arr