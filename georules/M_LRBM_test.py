# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:50:19 2023

@author: Nataly Chacon-Buitrago
"""


import numpy as np
from S_ProbMap import Lobe_map
from bathymetry import  varinace_bathymetry_maps
from utils import save_bath_as_array
from utils import save_list_as_json
from utils import save_centroids
from utils import save_array

## Reservoir Parameter Settings
wmax=[15000] #m
tmax=[2] #m
lenght =[30000] #m 
lobes = [30] #number of lobes
cellsize = [100] #cell size
nx = [250]
ny = [250]
t_matrix = [np.array([[0.1,0.13,0.3,0.15,0.22,0.1],
                     [0.3,0.05,0.3,0.15,0.15,0.05],
                     [0.3,0.13,0.1,0.15,0.18,0.14],
                     [0.25,0.1,0.25,0.09,0.22,0.09],
                     [0.05,0.25,0.25,0.25,0.05,0.15],
                     [0.15,0.25,0.25,0.25,0.05,0.05]])] #transition matrix
start_state = ["Q2"] # start states can be ["Q1","Q2","Q3","Q4","NMA","HF"]
quadrant_angles = [ {"Q1": [315,45],"Q2":[45,135],"Q3":[135,225],"Q4":[225,315]}] #lists of quadrants with their angles
source = [[25,200]] #source of the sediment (channel)
a1 = [0.66]
a2  = [0.33]
gp = [0.15]
cellsize_z =  [0.15]
n_mud = [2] #number of cells mud that covers lobe
mud_property = [0.18] #property mud
states = ["Q1", "Q2", "Q3", "Q4", "NMA", "HF"]


num_reals = 1

n = 1
n_tests = 20

while n < n_tests:
    for i in range (0, num_reals): 
        
        result = Lobe_map(
            nx[i],
            ny[i],
            cellsize[i],
            wmax[i],
            lenght[i],
            tmax[i],
            lobes[i],
            t_matrix[i],
            start_state[i],
            quadrant_angles[i],
            source[i],
            cellsize_z[i],
            n_mud[i],
            states
        )
        (
            Bathymetry_maps,
            centroids,
            prob_maps,
            quadrants,
            angle_stack,
            columns_corner,
            rows_corner,
            lobe_image
        ) = result
           
    
        ##Calculates Variance of thicknesses in bathymetry maps
        
        ##Calculates Variance of thicknesses in bathymetry maps
        variance_thickness = varinace_bathymetry_maps(Bathymetry_maps)
        
        #
        save_array("variance_thickness{}".format(n),"surface_variance",variance_thickness)
        
        #Turn list of bathymetry maps to arrays and save array to a file
        save_bath_as_array("bathy_array{}".format(n),"3d_grid_inputs", Bathymetry_maps)
        
        #save centroids
        save_centroids("centroids{}".format(n),"centroids", centroids)
        
        #Save lists as json files
        save_list_as_json("angle_stack{}".format(n),"3d_grid_inputs", angle_stack)
        save_list_as_json("columns_corner{}".format(n),"3d_grid_inputs", columns_corner)
        save_list_as_json("rows_corner{}".format(n),"3d_grid_inputs", rows_corner)
        save_list_as_json("quadrants{}".format(n),"3d_grid_inputs", quadrants)
        
        
        n = n + 1
        
        
