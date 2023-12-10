# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:21:17 2023

@author: Nataly Chacon-buitrago 

Function to find the population variance of each surface and plot the results.


"""

import numpy as np
import matplotlib.pyplot as plt

#Calculate variance for each bathymetry map - thickness

variance_bathymetry = []    
    
for arr in Bathymetry_maps:
    
    # calculate mean
    mean_array = np.mean(arr)
    # calculate squared differences
    squared_diff = (arr - mean_array)**2
    #calculate variance
    variance_array = np.mean(squared_diff)
    #append variance to the bathymetry map
    variance_bathymetry.append(variance_array)
    
 
#### plot variance vs surface

bathy_lenght = list(range(0,len(Bathymetry_maps)))

# set the title of a plot 
plt.title("Surface Variance") 
  
# plot scatter plot with x and y data 
plt.scatter(bathy_lenght,variance_bathymetry) 
  
# plot with x and y data 
plt.plot(bathy_lenght, variance_bathymetry) 

