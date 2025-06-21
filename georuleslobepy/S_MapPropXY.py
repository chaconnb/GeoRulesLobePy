# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 22:06:17 2023

@author: Nataly Chacon-Buitrago 
This function builds the facies trend in the XY axis. Best quality in the axis. 
"""

import numpy as np

from georuleslobepy.S_Lobegeom import drop_geometry
from georuleslobepy.S_PasteArray import paste
from georuleslobepy.S_nonzero_one import convert_nonzero_to_one


#length = Value_4_lenght[0]
#wmax = Value_2_wmax[0]
#cell_size = Value_6_cellsize[0]
#a1 = Value_13_a1[0]
#a2 = Value_14_a2[0]
#y_interval = 100




def PropXY(length,wmax,cell_size,a1,a2):
    
    wmax_list =  [i for i in range(cell_size*2,wmax, cell_size)]
    lenght_list =  [i for i in range(int(length/len(wmax_list)),length,int(length/len(wmax_list )))]
    
    #create an array of zeros
    lobe_XY = np.zeros((int(wmax/cell_size),int(length/cell_size)))
    y_interval = cell_size
    
    ###
    for i in range(10, len(wmax_list)): 
    
        x_interval =  [i for i in range(0,lenght_list[i], cell_size)]
        lobe1 =  drop_geometry(wmax_list[i],lenght_list[i],1,x_interval,cell_size,a1,a2)

        #convert nonzero to one
        lobe1 = convert_nonzero_to_one(lobe1)

        #Paste lobe1 in lobeXY
        coor = int((wmax - wmax_list[i])/(y_interval*2))
        lobeXY_f =  paste(lobe_XY.copy(),lobe1.copy(),(coor,0))
        lobe_XY = lobe_XY +  lobeXY_f
        
    # Create a copy of the array to store the normalized values
    lobe_XY_norm = lobe_XY.copy()

    # Find the non-zero elements
    nonzero_elements = lobe_XY_norm[lobe_XY_norm != 0]

    ### normalize lobe 
    min_value = np.min(lobe_XY[lobe_XY != 0])
    max_value = np.max(lobe_XY)

    ## normalize the array to the range [0,1]
    lobe_XY_norm[lobe_XY != 0] = (nonzero_elements - min_value) / (max_value - min_value)
        
    return(lobe_XY_norm)
        
        
        
        
    