# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:51:47 2023

@author: Nataly Chacon-Buitrago
"""

import numpy as np
from utils import load_list_json
from utils import load_array


#functions
def lobe_max_thickness(bathymetry_map_n_1, bathymetry_map_n):
    
    """Calculates maximum thickness for new lobe in bathymetry_map_n.
       
       Parameters
       ----------  
       bathymetry_map_n_1 : np.ndarray
       Bathymetry map generated for n-1 lobe.  
       bathymetry_map_n: np.ndarray
       Bathymetry map generated for n lobe.
       
       Returns
       -------
       max_thickness : max thickness for n+1 lobe. 
            

    """
    
    bathy_thickness_difference = bathymetry_map_n - bathymetry_map_n_1 
    max_thickness = np.max(bathy_thickness_difference)
    
    return(max_thickness)


#input
n_lobes = 40
n_test = 300

#Data prep
test_number = 0 #cambiar

#Load quadrants
quadrants = load_list_json("quadrants{}".format(test_number),"3d_grid_inputs")
#Load bathymetry maps
bathymetry_array =  load_array("bathy_array{}".format(test_number),"3d_grid_inputs")
#Remove the first bathymetry map from the bathymetry array as it doesn't contain any lobes (only zeros).
bathymetry_array = bathymetry_array[1:len(bathymetry_array),:,:]

#array for saving max thickness for each lobe on each realization
lobe_thickness_realizations = np.zeros((n_lobes, n_test))


for i in range(len(quadrants)): 
    if quadrants[i] != "HF":
        if i == 0:
            lobe_thickness_realizations[i,test_number] = np.max(bathymetry_array[0,:,:])
        else:
            lobe_thickness_realizations[i,test_number] = lobe_max_thickness(bathymetry_array[i-1,:,:],bathymetry_array[i,:,:])
            
            
            
    
       
     
    