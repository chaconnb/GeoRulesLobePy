# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:50:19 2023

@author: Nataly Chacon-Buitrago
"""



from S_ProbMap import Lobe_map
from S_3Dgrid_healing import sandbox
from V_grid import grid
import numpy as np
import math 

## Reservoir Parameter Settings
wmax=[15000] #m
tmax=[2] #m
lenght =[30000] #m 
lobes = [5] #number of lobes
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
        centoids,
        prob_maps,
        quadrants,
        angle_stack,
        columns_corner,
        rows_corner,
        lobe_image
    ) = result
           
    
    
    # ## Create 3D Grid  
    
    nz = math.ceil(np.max(Bathymetry_maps[len(Bathymetry_maps)-1])) + 5 #Find maximum height 
    sandbox_grid = sandbox(lenght[0],wmax[0],cellsize[0],lobe_image,cellsize_z[0],tmax[0],gp[0],mud_property[0],
    n_mud[0],a1[0],a2[0],nx[0],ny[0],nz,lobes[0],angle_stack,columns_corner,rows_corner,Bathymetry_maps,quadrants)

    # # Visualize 
    grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=40, slice_y=30, slice_z=2) #change depending on desired type of visualization 
    
    
    
    
