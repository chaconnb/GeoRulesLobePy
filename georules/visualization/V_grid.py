#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:04:57 2023

@author: Nataly Chacon-Buitrago
Function to plot grid using PyVista
For Pyvista tutorials on gridding and slicing: 
    https://docs.pyvista.org/version/stable/examples/01-filter/slicing.html
    https://docs.pyvista.org/version/stable/examples/00-load/create-uniform-grid.html#sphx-glr-examples-00-load-create-uniform-grid-py

input:
    array_togrid = 3d array that we want to tranform to a grid
    cellsize_x, cellsize_y, cellsize_z = proportions of the size in the x,y,z axis respectively (ex: 1,1,1 the size will be the same in the x,y,z - axis)
    plot_grid = plot the grid in 3D. Input True or False
    plot_orthogonal = plot orthogonal fence diagram. Input True or False
    plot_slices = plot slices of the volume. Input True or False
    slice_x = If plot_slices is True -> input number of slice in x
    slice_y = If plot_slices is True -> input number of slice in y
    slice_z = If plot_slices is True -> input number of slice in z
    
    
output:
    visualization

"""
import matplotlib.pyplot as plt
import pyvista
import numpy as np


def grid(array_togrid,cellsize_x,cellsize_y,cellsize_z,plot_grid=None,plot_orthogonal=None, plot_slices = None, 
         slice_x = None, slice_y = None, slice_z = None):
    
    ## Create the spacial reference
    grid = pyvista.UniformGrid()
    
    # Set the grid dimensions: shape + 1 because we want to inject our values on
    #   the CELL data
    grid.dimensions = np.array(array_togrid.shape) + 1 
    
    # Edit the spatial reference
    grid.origin = (0, 0, 0)  # The bottom left corner of the data set
    grid.spacing = (cellsize_x, cellsize_y, cellsize_z)  # These are the cell sizes along each axis
    
    # Add the data values to the cell data
    grid.cell_data["values"] = array_togrid.flatten(order="F")  # Flatten the array
    
    if plot_grid:
        grid.plot(show_edges=True)
        
    if plot_orthogonal:
        cmap = plt.cm.get_cmap("viridis", 4)
        slices = grid.slice_orthogonal()
        slices.plot(cmap=cmap)
        
    if plot_slices:
        cmap = plt.cm.get_cmap("viridis", 5)
        slices = grid.slice_orthogonal(x=slice_x, y=slice_y, z=slice_z)
        slices.plot(cmap=cmap)
