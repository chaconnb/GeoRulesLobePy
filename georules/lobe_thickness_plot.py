# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:51:47 2023

@author: Nataly Chacon-Buitrago
Calculates and plots maximum thickness of lobes for every lobe in every test realization.
"""

import numpy as np
import matplotlib.pyplot as plt
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


#array for saving max thickness for each lobe on each realization
lobe_thickness_realizations = np.zeros((n_lobes, n_test))

#Data prep
for n in range(n_test):
    #Load quadrants
    quadrants = load_list_json("quadrants{}".format(n),"3d_grid_inputs")
    #Load bathymetry maps
    bathymetry_array =  load_array("bathy_array{}".format(n),"3d_grid_inputs")
    #Remove the first bathymetry map from the bathymetry array as it doesn't contain any lobes (only zeros).
    bathymetry_array = bathymetry_array[1:len(bathymetry_array),:,:]
    
    
    for i in range(len(quadrants)): 
        if quadrants[i] != "HF":
            if i == 0:
                lobe_thickness_realizations[i,n] = np.max(bathymetry_array[0,:,:])
            else:
                lobe_thickness_realizations[i,n] = lobe_max_thickness(bathymetry_array[i-1,:,:],bathymetry_array[i,:,:])
                

# Replace zeros with nan
lobe_thickness_nan = np.where(lobe_thickness_realizations == 0, np.nan, lobe_thickness_realizations)
#create a list of lists with the thickneses for the  n_lobes for the n_test realizations.
lobe_thickness_list = [row.tolist() for row in lobe_thickness_nan]
                
#boxplot

labels = list(map(str, range(1, n_lobes+1)))

# MultipleBoxplots
# Set the figure size
plt.figure(figsize=(12, 6)) # Adjust the values (width, height) as needed

#boxplot
plt.boxplot(lobe_thickness_list, vert=True, patch_artist=True, labels=labels) 
plt.ylabel('Thickness')
plt.xticks(rotation=90)
# plt.title('Multiple Box Plot : Vertical Version')
plt.savefig("lobe_thickness_plot.png", format="png", dpi=1200)
plt.show()


             
    
       
     
    