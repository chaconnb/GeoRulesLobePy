#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nataly Chacon-Buitrago
Function to plot grid using PyVista
For Pyvista tutorials on gridding and slicing: 
    https://docs.pyvista.org/version/stable/examples/01-filter/slicing.html
    https://docs.pyvista.org/version/stable/examples/00-load/create-uniform-grid.html#sphx-glr-examples-00-load-create-uniform-grid-py

"""
import matplotlib.pyplot as plt
import pyvista as pv 
import numpy as np


def grid(array_togrid,cellsize_x,cellsize_y,cellsize_z,plot_grid=None,plot_orthogonal=None, plot_slices = None, 
         slice_x = None, slice_y = None, slice_z = None):
    
    """Function to plot grid using PyVista. 
       
    Parameters
    ----------
    array_togrid: np.array
        3D array to visualize. 
    cellsize_x: float    
        Proportion of cells in x axis with respect to z and y axis.
    cellsize_y: float
        Proportion of cells in y axis with respect to z and x axis.
    cellsize_z: float
        Proportion of cells in z axis with respect to y and x axis. 
    plot_grid: boolean (True or False)
        Plot the grid in 3D. 
    plot_slices: boolean (True or False)
        Plot slices of the volume.
    slices_x: float
        If plot_slices is True -> input number of slice in x.
    slices_y: float
        If plot_slices is True -> input number of slice in y.
    slices_z: float
        If plot_slices is True -> input number of slice in z.
        
    
    Returns
    -------
    grid:
        Grid visualizatiion.
    """
    
    ## Create the spacial reference
    grid = pv.ImageData()
    
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
