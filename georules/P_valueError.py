# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:21:57 2023

@author: nc25884
"""

import numpy as np

Bathymetry_ = Bathymetry_maps[2]
power = 5
n_x = 250
n_y = 250


#Find Probabilities
elevation_s = (Bathymetry_ - np.min(Bathymetry_))/(np.max(Bathymetry_)+0.0001)+0.0001
prob_s_b = (1/np.transpose(elevation_s))**power ## compensational power  ###Sera necesario tenerlo que trasponer???\
#prob_s_b is the probability map before  the mask 
prob_s = prob_s_b.copy() #create deep copy

prob_sum = np.sum(prob_s) #prob_s has to be positive
norm_prob_s = prob_s/prob_sum
# Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
#np.random.seed(351023)
index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
        
# Convert the flattened index to a row and column index
a, b = divmod(index, elevation_s.shape[1])

Location_ = [a,b] #location of the centroid