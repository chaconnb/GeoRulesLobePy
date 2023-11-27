# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:23:34 2023

@author: Nataly Chacon-Buitrago
"""
import numpy as np
import math

from .S_lobe_facies import grid_lobe
from .S_RotateCoord import rotate_coord
from .visualization.V_grid import grid


### inputs
# lobe_length = Value_4_lenght[0]
# cell_size = Value_6_cellsize[0]
# lobe_wmax = Value_2_wmax[0]
# cellsize_z = Value_19_cellsize_z[0]
# lobe_tmax = Value_3_tmax[0]
# global_prop = Value_15_gp[0]
# mud_property = Value_21_mud_property[0]
# n_cell_mud = Value_20_n_mud[0]
# a1 = Value_13_a1[0]
# a2 = Value_14_a2[0]
# nx = 100
# ny = 100
# n_lobe = Value_5_lobes[0]



def sandbox(lobe_length,lobe_wmax,cell_size,lobe_image,cellsize_z,lobe_tmax,global_prop,mud_property,n_cell_mud,a1,a2,nx,ny,nz,n_lobe,angle_stack,
            columns_corner,rows_corner,Bathymetry_maps,quadrants):
    
    #Find coordinates of standard lobe in grid system
    new_column = lobe_length/cell_size
    new_row = lobe_wmax/cell_size
        
    coord = []
        
    for i in range(int(new_column)):
        for j in range(int(new_row)):
            coord.append([i,j])
    
    coord = np.array(coord)
    
    #Create 3D Lobe
    grid_lobe_normal_mud = grid_lobe(lobe_image,lobe_length,lobe_wmax,cellsize_z,cell_size,lobe_tmax,global_prop,mud_property,n_cell_mud,1,a1,a2)
    
    #Sandbox_grid
    sandbox_grid = np.zeros((nx,ny,int(nz/cellsize_z)))
    
    #nz_values - values for z axis
    nz_values = np.linspace(0,nz-cellsize_z,int(nz/cellsize_z))
    
    ## Function to filter values that are outside the sandbox
    def verify_range(x_nc_ur,y_nc_ur,x_nc_udr,y_nc_udr,nx,ny):
          if 0 <= x_nc_ur <= nx-1 and 0 <= y_nc_ur <= ny-1 and 0 <= x_nc_udr <= nx-1  and 0 <= y_nc_udr <= ny-1:
              return True
          else:
              return False
    
       
    for n in range(1,n_lobe+1): 
        
        
        if n == 1:
            print(n)
            
            new_coord = rotate_coord(coord, angle_stack[n-1], lobe_image,columns_corner[n-1],rows_corner[n-1])
            
            for i in range(len(coord)):
                x_c = coord[i][0]
                y_c = coord[i][1]
                    
                x_nc_ur = round(new_coord[i][0])
                y_nc_ur = round(new_coord[i][1])
                    
                x_nc_udr = math.floor(new_coord[i][0])
                y_nc_udr = math.floor(new_coord[i][1])
                
                    
                if verify_range(x_nc_ur, y_nc_ur, x_nc_udr, y_nc_udr, nx, ny): #### esto se puede cambiar!!!!!
                    for k in range(int(lobe_tmax/cellsize_z)):
                        if sandbox_grid[y_nc_ur,x_nc_ur,k] == 0:
                            sandbox_grid[y_nc_ur,x_nc_ur,k] =  grid_lobe_normal_mud[x_c,y_c,k]
                              
                        if sandbox_grid[y_nc_udr,x_nc_udr,k] == 0:
                            sandbox_grid[y_nc_udr,x_nc_udr,k] =  grid_lobe_normal_mud[x_c,y_c,k]
                              
                        if sandbox_grid[y_nc_udr,x_nc_ur,k] == 0:
                            sandbox_grid[y_nc_udr,x_nc_ur,k] = grid_lobe_normal_mud[x_c,y_c,k]
                              
                        if sandbox_grid[y_nc_ur,x_nc_udr,k] == 0:
                           sandbox_grid[y_nc_ur,x_nc_udr,k] = grid_lobe_normal_mud[x_c,y_c,k] 
                
            #grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=40, slice_y=30, slice_z=2)       
                           
                       
        else:
            
            if quadrants[n-1] == "HF":
                print(n,"HF")
                
                result_bath = Bathymetry_maps[n]-Bathymetry_maps[n-1]
                cell_num = result_bath / cellsize_z
                cell_num = [[round(element) for element in row] for row in cell_num]
                cell_num = np.array(cell_num)
                
                
                for i in range(nx):
                    for j in range(ny):
                        for k in range(len(nz_values)):
                            if nz_values[k] <= cellsize_z and cell_num[j,i]!=0 and sandbox_grid[j,i,k]==0:
                                cells = cell_num[j,i]
                                for n in range(cells):
                                    sandbox_grid[j,i,k+n]= mud_property+2
                                cell_num[j,i] = 0
                                   
                            else:
                                if k+1 < len(nz_values):
                                    element1 = sandbox_grid[j,i,k]
                                    element2 = sandbox_grid[j,i,k+1]
                                    
                                    if element1 != 0 and element2 ==0 and cell_num[j,i]!=0:
                                        cells = cell_num[j,i]
                                        
                                        for n in range(cells):
                                            if k+n < len(nz_values):
                                                sandbox_grid[j,i,k+n]= mud_property+2
                                        
                                        cell_num[j,i] = 0
            
                #grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=40, slice_y=30, slice_z=2)
                
            
            else: 
                print(n)
                
                #Find new coordinates - new_coord is equivalent to coord
                new_coord = rotate_coord(coord,angle_stack[n-1],lobe_image,columns_corner[n-1],rows_corner[n-1])
                #Filter values that are outside the sandbox
                #Index of the values inside the sandbox
                verify_range_index = np.where((new_coord[:, 0] >= 0) & (new_coord[:, 0] <= nx-1) & (new_coord[:, 1] >= 0) & (new_coord[:, 1] <= ny-1))[0]
                #New coordinates of the values inside the sandbox
                verify_range_new_coord = new_coord[verify_range_index]
                #Find the equivalent coordinates of the verify_range_new_coord using the indices
                verify_range_coord = coord[verify_range_index]
        
                ###create array to verify which coordinates have been filled out
                fill_out_array = np.zeros((nx,ny))
        
        
                for i in range(len(verify_range_coord)):
                    
                    x_c = verify_range_coord[i][0]
                    y_c = verify_range_coord[i][1]
           
           
                    if lobe_image[y_c,x_c]!= 0:
               
                        ####Hipotesis al redondear
                        x_nc_ceil = round(verify_range_new_coord[i][0])
                        y_nc_ceil = round(verify_range_new_coord[i][1])
               
                        if fill_out_array[x_nc_ceil][y_nc_ceil] == 0:
                            fill_out_array[x_nc_ceil][y_nc_ceil] = 1
               
                            ### Find where the deposition starts
                            j = 0
                            z_cell = sandbox_grid[y_nc_ceil,x_nc_ceil,j]
           
                            while z_cell != 0:
                                j = j+1
                                z_cell = sandbox_grid[y_nc_ceil,x_nc_ceil,j]
                 
                            if sandbox_grid.shape[2]-j > grid_lobe_normal_mud.shape[2]:    
                                sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+grid_lobe_normal_mud.shape[2]] = grid_lobe_normal_mud[x_c,y_c,:]
                   
                            else:
                                sandbox_grid[y_nc_ceil,x_nc_ceil,j:sandbox_grid.shape[2]] = grid_lobe_normal_mud[x_c,y_c,0:sandbox_grid.shape[2]-j] 
            
                   
                        x_nc_floor = math.floor(verify_range_new_coord[i][0])
                        y_nc_floor = math.floor(verify_range_new_coord[i][1])
                 
                        if fill_out_array[x_nc_floor][y_nc_floor] == 0:
                            fill_out_array[x_nc_floor][y_nc_floor] = 1
                   
                            ### Find where the deposition starts
                            j = 0
                            z_cell = sandbox_grid[y_nc_floor,x_nc_floor,j]
           
                            while z_cell != 0:
                                j = j+1
                                z_cell = sandbox_grid[y_nc_floor,x_nc_floor,j]
                 
                            if sandbox_grid.shape[2]-j > grid_lobe_normal_mud.shape[2]:  
                                sandbox_grid[y_nc_floor,x_nc_floor,j:j+grid_lobe_normal_mud.shape[2]] = grid_lobe_normal_mud[x_c,y_c,:]
                   
                            else:
                                sandbox_grid[y_nc_floor,x_nc_floor,j:sandbox_grid.shape[2]] = grid_lobe_normal_mud[x_c,y_c,0:sandbox_grid.shape[2]-j] 
            
                   
                        if fill_out_array[x_nc_ceil][y_nc_floor] == 0:
                            fill_out_array[x_nc_ceil][y_nc_floor] = 1
                   
                            ### Find where the deposition starts
                            j = 0
                            z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
           
                            while z_cell != 0:
                                j = j+1
                                z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
                 
                            if sandbox_grid.shape[2]-j > grid_lobe_normal_mud.shape[2]:  
                                sandbox_grid[y_nc_floor,x_nc_ceil,j:j+grid_lobe_normal_mud.shape[2]] = grid_lobe_normal_mud[x_c,y_c,:]
                   
                            else:
                                sandbox_grid[y_nc_floor,x_nc_ceil,j:sandbox_grid.shape[2]] = grid_lobe_normal_mud[x_c,y_c,0:sandbox_grid.shape[2]-j] 
                                
    
               
                   
                        if fill_out_array[x_nc_floor][y_nc_ceil] == 0:
                            fill_out_array[x_nc_floor][y_nc_ceil] = 1
               
                            ### Find where the deposition starts
                            j = 0
                            z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
           
                            while z_cell != 0:
                                j = j+1
                                z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
                 
                            if sandbox_grid.shape[2]-j > grid_lobe_normal_mud.shape[2]:  
                                sandbox_grid[y_nc_ceil,x_nc_floor,j:j+grid_lobe_normal_mud.shape[2]] = grid_lobe_normal_mud[x_c,y_c,:]
                   
                            else:
                                sandbox_grid[y_nc_ceil,x_nc_floor,j:sandbox_grid.shape[2]] = grid_lobe_normal_mud[x_c,y_c,0:sandbox_grid.shape[2]-j] 
                                
                                
            #grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=40, slice_y=30, slice_z=2)
     
                   
     
    return(sandbox_grid)