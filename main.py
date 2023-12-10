# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:50:19 2023

@author: Nataly Chacon-Buitrago
"""

# visualization

from georules.S_ProbMap import Lobe_map
from georules.variance_bathymetry import varinace_bathymetry_maps
from georules.utils import save_bath_as_array
from georules.S_3Dgrid_healing import sandbox
from georules.V_grid import grid
import numpy as np
import os
import math 

## Reservoir Parameter Setting
Value_1_Power=[5]
Value_2_wmax=[15000] #m
Value_3_tmax=[2] #m
Value_4_lenght =[30000] #m 
Value_5_lobes = [10] #number of lobes
Value_6_cellsize = [100] #cell size
Value_7_nx = [250]
Value_8_ny = [250]
Value_9_t_matrix = [[[0.1,0.13,0.3,0.15,0.22,0.1],
                     [0.3,0.05,0.3,0.15,0.15,0.05],
                     [0.3,0.13,0.1,0.15,0.18,0.14],
                     [0.25,0.1,0.25,0.09,0.22,0.09],
                     [0.05,0.25,0.25,0.25,0.05,0.15],
                     [0.15,0.25,0.25,0.25,0.05,0.05]]] #transition matrix
Value_10_start_state = ["Q2"] # start states can be ["Q1","Q2","Q3","Q4","NMA","HF"]
Value_11_quadrant_angles = [ {"Q1": [315,45],"Q2":[45,135],"Q3":[135,225],"Q4":[225,315]}] #lists of quadrants with their angles
Value_12_source = [[25,200]] #source of the sediment (channel)
Value_13_a1 = [0.66]
Value_14_a2  = [0.33]
Value_15_gp = [0.15]
Value_19_cellsize_z =  [0.15]
Value_20_n_mud = [2] #number of cells mud that covers lobe
Value_21_mud_property = [0.18] #property mud


num_tests = 300
n = 1



num_reals = 1

for i in range (0, num_reals): 
    
    result = Lobe_map(
        Value_7_nx[i],
        Value_8_ny[i],
        Value_6_cellsize[i],
        Value_2_wmax[i],
        Value_4_lenght[i],
        Value_3_tmax[i],
        Value_5_lobes[i],
        Value_1_Power[i],
        Value_9_t_matrix[i],
        Value_10_start_state[i],
        Value_11_quadrant_angles[i],
        Value_12_source[i],
        Value_19_cellsize_z[i],
        Value_20_n_mud[i]
    )
    (
        Bathymetry_maps,
        centoids,
        prob_maps,
        quadrants,
        angle_stack,
        columns_corner,
        rows_corner,
        lobe_image
    ) = result
        
 
    ##Calculates Variance of thicknesses in bathymetry maps
    
    variance_thickness = varinace_bathymetry_maps(Bathymetry_maps)
    
    #Turn list of bathymetry maps to arrays and save array to a file

    save_bath_as_array("test_bathy{}".format(n),Bathymetry_maps)
    
    
    ## Create 3D Grid  
    
    #nz = math.ceil(np.max(Bathymetry_maps[len(Bathymetry_maps)-1])) + 5 #Find maximum height 
    #sandbox_grid = sandbox(Value_4_lenght[0],Value_2_wmax[0],Value_6_cellsize[0],lobe_image,Value_19_cellsize_z[0],Value_3_tmax[0],Value_15_gp[0],Value_21_mud_property[0],
     #Value_20_n_mud[0],Value_13_a1[0],Value_14_a2[0],Value_7_nx[0],Value_8_ny[0],nz,Value_5_lobes[0],angle_stack,columns_corner,rows_corner,Bathymetry_maps,quadrants)

    ## Visualize 
    #grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=40, slice_y=30, slice_z=2) #change depending on desired type of visualization 
    
    
    
    
