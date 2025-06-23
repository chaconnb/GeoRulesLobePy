# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago  

"""

import numpy as np
import math


def  drop_geometry(wmax,lenght,tmax,x,y_interval, a1 =0.66, a2 =0.33):

    """
    Generates a new lobe geometry array with x, y coordinates and corresponding thickness values.

    This function creates a 2D representation of a lobe's thickness distribution using equations 
    from Zhang et al. (2009), with a modification to the equation used for calculating the width (w_x).
    
    Parameters
    ----------
    wmax : int
        Maximum width of the lobe.
    length : int
        Maximum length of the lobe.
    tmax : int
        Maximum thickness of the lobe.
    x : list or ndarray
        List of x-coordinates at which to compute lobe thickness (length-wise).
    y_interval : float
        Spatial resolution or interval along the y-direction.
    a1 : float, optional
        Relative position along the length where the maximum width occurs. Default is 0.66.
    a2 : float, optional
        Relative position along the length where the maximum thickness occurs. Default is 0.33.

    Returns
    -------
    lobe_thick : ndarray
        2D array representing thickness values.

    Notes
    -----
    - Changing the values of `a1` and `a2` affects the centroid of the lobe geometry. If modified, 
      the `S_RotatePaste` function must also be updated to ensure consistent spatial alignment.
    """
    
    b1 = -np.log(2)/np.log(1-a1)
    
    
    w_x_ = [ 2 * wmax *(1-i/lenght)**b1 *(1-(1-i/lenght)**b1) for i in x] 
    w_x_ = np.array(w_x_)

    b2 = -np.log(2)/np.log(1-a2)
    t_x_ = [4* tmax *(1 -i/lenght)**b2 *(1 - (1- i/lenght)**b2) for i in x] 
    t_x_ = np.array(t_x_)
    
    
    
    t_y_ = []
    lobe_thick = np.zeros([int(wmax/y_interval), len(x)])
    
    
    for i in range(len(x)):
    
        y = [i for i in range(0,int(np.round(2*w_x_[i])),y_interval)]       
        ty = []
        
        if w_x_[i] != 0:
    
            
            for j in  range(len(y)):
                a = 0.5
                b = -np.log(2)/np.log(1-a)
                
                t = 4 * t_x_[i] * (y[j]/(2*w_x_[i]))**b *(1-(y[j]/(2*w_x_[i]))**b)
                ty.append(t)
           
            ty = np.array(ty)
            t_y_.append(ty)
            
        else:
            ty = np.zeros(int(wmax/y_interval))
            t_y_.append(ty)
            
        #move all y coordinates to align with the centroid and add zeros
        
        if len(ty) < wmax/y_interval:
        
            dif = wmax- y_interval #subtract to get index starting from zero
            dif = dif - max(y)
            dif = dif/y_interval
            
            if dif%2 == 0:
                limit = np.zeros(int(dif/2))
                thick = np.concatenate((limit,ty))
                thick = np.concatenate((thick,limit))
                thick = np.array(thick)
                thick = np.transpose(thick)
                lobe_thick[:,i] = thick
                
            else:
                upper_limit = np.zeros(math.floor(dif/2))
                lower_limit = np.zeros(math.ceil(dif/2))
                thick = np.concatenate((upper_limit,ty))
                thick = np.concatenate((thick,lower_limit))
                thick = np.array(thick)
                thick = np.transpose(thick)
                lobe_thick[:,i] = thick
            
                
        else:
                lobe_thick[:,i] = ty
         
    return(lobe_thick)












