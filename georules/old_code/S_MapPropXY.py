# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
This function builds the facies trend in the XY axis. Best quality in the axis. 
"""
import numpy as np

## example input: 
# length = Value_4_lenght[0]
# wmax = Value_2_wmax[0]
# cell_size = Value_6_cellsize[0]
# a1 = Value_13_a1[0]
# a2 = Value_14_a2[0]
# Rx = length
# Ry = wmax/2


def PropXY(length,wmax,cell_size):
    
    Rx = length 
    Ry = wmax/2

    ## built the array and the lobe shape
    #x-axis
    x_interval = [i for i in range(0,length, cell_size)]
 
    #y-axis
    y_interval = [i for i in range(0,int(wmax/2), cell_size)]
    y_interval_neg = [ i*-1 for i in y_interval]


    y_coord_inv = y_interval[::-1]
    y_coord_total = y_coord_inv + y_interval_neg

    # create a grid of x and y values
    X_coord,Y_coord = np.meshgrid(x_interval,y_coord_total)

    # calculate the values of p for each (x,y) pair
    p = ((X_coord/Rx)**2 + (Y_coord/Ry)**2)**(1/2)
    p = np.absolute(1-p) #this is done if we want the property to be  high towards  the axis and low towards the margin! 

    return(p)



#### Returns lobe shape
#lobe_XY =  drop_geometry(wmax,length,1,x_interval,cell_size,a1,a2) 
#let's change  all the non-zero elements to 1
#lobe_XY = np.where(lobe_XY != 0,1,0)
#lobe_XY = np.absolute(p*lobe_XY)
 










