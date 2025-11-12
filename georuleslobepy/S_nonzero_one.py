#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

"""

import numpy as np

def convert_nonzero_to_one(arr):
    """
    Converts all non-zero values in an array to 1, and zeros remain unchanged.

    This function is useful for binarizing an array, preserving the location 
    of non-zero elements while removing their original values.

    Parameters
    ----------
    arr : ndarray
        Input NumPy array of any shape and numeric type.

    Returns
    -------
    new_arr : ndarray
        Array of the same shape as `arr`, where all non-zero values are set to 1,
        and all zero values remain 0.

    Examples
    --------
    >>> import numpy as np
    >>> convert_nonzero_to_one(np.array([[0, 2], [3, 0]]))
    array([[0, 1],
           [1, 0]])
    """
    new_arr = np.where(arr != 0, 1, 0)
    
    return new_arr