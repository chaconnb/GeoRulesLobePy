#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:02:30 2023

@author: Nataly Chacon-Buitrago
Function to build the 3D grid from the Bathymetry maps.
"""
from S_RotateCoord import rotate_coord
from S_Lobegeom import drop_geometry
from S_lobe_facies import grid_lobe
import numpy as np
import math


from V_grid import grid ### temporal
### parameters example

# a1 = 0.66
# a2 = 0.33
# lobe_wmax = 15000
# lobe_length = 30000
# lobe_tmax = 2
# y_interval = 100
# cell_size = 100
# n_cell_mud = 1 # number of cells that are going to be mud
# ##Sandbox grid (nx and ny same as bathymetry maps)
# nx = 400 #nx
# ny = 400  #ny
# cellsize_z = 0.05 ## cell size grid z-axis
# nz = 10 # model height
# lobe_n=30 #number of lobes



def sandbox(a1,a2,lobe_image,lobe_wmax,lobe_length,lobe_tmax,nx,ny,cell_size,cellsize_z,nz,lobe_n,angle_stack,columns_corner,rows_corner,Bathymetry_maps,n_cell_mud, mud_property,quadrants,global_prop):
    
    
    #Standard lobe is build (lobe with characteristics input in function)
    lobe_x=  [i for i in range(0,lobe_length,100)]
    y_interval = cell_size
    
     
    ## lobe thickness
    lobe_thickness = lobe_image
    
    
    #Find coordinates of standard lobe in grid system
    new_column = lobe_length/cell_size
    new_row = lobe_wmax/cell_size
    
    coord = []
    
    for i in range(int(new_column)):
        for j in range(int(new_row)):
            coord.append([i,j])
    
    #Create 3d Lobe
    grid_lobe_normal_mud = grid_lobe(lobe_image,lobe_length,lobe_wmax,cellsize_z,cell_size,lobe_tmax,global_prop,mud_property,n_cell_mud,1,a1,a2)
    sandbox_grid = np.zeros((nx,ny,int(nz/cellsize_z)))
    nz_values = np.linspace(0,nz-cellsize_z,int(nz/cellsize_z))
    
    dict_sandbox = {}
    
    ## Function to filter values that are outside the sandbox
    def verify_range(x_nc_ur,y_nc_ur,x_nc_udr,y_nc_udr,nx,ny):
        if 0 <= x_nc_ur <= nx-1 and 0 <= y_nc_ur <= ny-1 and 0 <= x_nc_udr <= nx-1  and 0 <= y_nc_udr <= ny-1:
            return True
        else:
            return False
        
    
    ## Function to find minimum value that is not zero, when negative it goes to zero
    def min_nozero(array1):
        if np.all(array1 == 0):
            return(0)
        else:
            nonzero_values = array1[array1 != 0]
            min_nonzero = np.min(nonzero_values)
            if min_nonzero < 0:
                min_nonzero = 0
            return(min_nonzero)
       
    f = 0 
       
    for n in range(1,lobe_n+1):
        
        
        #grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=20, slice_y=90, slice_z=6)
        #dict_sandbox[n] = sandbox_grid  ### TEST - DELETE AFTER TEST
    
        if n == 1:
            #print(n)
            
            
            new_coord = rotate_coord(coord, angle_stack[n-1], lobe_thickness,columns_corner[n-1],rows_corner[n-1])
            bath_map = Bathymetry_maps[n]
            
            for i in range(len(coord)):
                x_c = coord[i][0]
                y_c = coord[i][1]
                
                x_nc_ur = round(new_coord[i][0])
                y_nc_ur = round(new_coord[i][1])
                
                
                x_nc_udr = math.floor(new_coord[i][0])
                y_nc_udr = math.floor(new_coord[i][1])
            
                
                if verify_range(x_nc_ur, y_nc_ur, x_nc_udr, y_nc_udr, nx, ny):
                    for k in range(int(lobe_tmax/cellsize_z)):
                        if sandbox_grid[y_nc_ur,x_nc_ur,k] == 0:
                            sandbox_grid[y_nc_ur,x_nc_ur,k] =  grid_lobe_normal_mud[x_c,y_c,k]
                          
                        if sandbox_grid[y_nc_udr,x_nc_udr,k] == 0:
                            sandbox_grid[y_nc_udr,x_nc_udr,k] =  grid_lobe_normal_mud[x_c,y_c,k]
                          
                        if sandbox_grid[y_nc_udr,x_nc_ur,k] == 0:
                            sandbox_grid[y_nc_udr,x_nc_ur,k] = grid_lobe_normal_mud[x_c,y_c,k]
                          
                        if sandbox_grid[y_nc_ur,x_nc_udr,k] == 0:
                            sandbox_grid[y_nc_ur,x_nc_udr,k] = grid_lobe_normal_mud[x_c,y_c,k]
                            
            
    
        else:
           
            #print(n)
            if quadrants[n-1] == 'HF':
                print('HF')
                
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
                                                                
                
                
            else:
        
                #new_coord = rotate_coord(coord, angle_stack[n-1], lobe_thickness,columns_corner[n-1],rows_corner[n-1])
                bath_map = Bathymetry_maps[n]
            
                bath_map = Bathymetry_maps[n]
                bath_map_anterior = Bathymetry_maps[n-1] 
                bath_dif = bath_map - bath_map_anterior 
            
                #create mask to only work with current lobe's thickness
                mask =  (bath_dif != 0) & (bath_dif > 0.0001)
                bma_thick = np.where(mask,bath_map_anterior,0) #bath_map_anterior only where the current lobe is
                real_thick = np.where(mask,bath_map,0)
                bath_min = min_nozero(bma_thick)
                bath_max = np.max(real_thick)
                
                lobe_tmax_new = bath_max - bath_min
            
                ### Find new lobe
                lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,lobe_tmax_new,lobe_x,y_interval, a1, a2)
                grid_lobe_new = grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,lobe_tmax_new,global_prop,mud_property,n_cell_mud,0,a1,a2)                                          
                new_coord = rotate_coord(coord, angle_stack[n-1],lobe_thickness_new,columns_corner[n-1],rows_corner[n-1])
        
                #Equivalent coordinates in z axis in grid lobe and sand box
                z_grid_lobe = nz_values[0:grid_lobe_new.shape[2]]
                z_sand_box = nz_values[np.argmin(np.abs(nz_values -bath_min)):np.argmin(np.abs(nz_values -bath_min))+grid_lobe_new.shape[2]]
        
                #Find indices of z_sand_box 
                nz_values_indices = {round(element,2): index for index, element in enumerate(nz_values)}
                z_sand_box_index = [nz_values_indices[round(element,2)] for element in z_sand_box]  
                
                for i in range(len(coord)):
                          
                    x_c = coord[i][0]
                    y_c = coord[i][1]
                          
                    x_nc_ur = round(new_coord[i][0])
                    y_nc_ur = round(new_coord[i][1])
                          
                    x_nc_udr = math.floor(new_coord[i][0])
                    y_nc_udr = math.floor(new_coord[i][1])
                          
                    if verify_range(x_nc_ur, y_nc_ur, x_nc_udr, y_nc_udr, nx, ny):
                        for k in range(len(z_grid_lobe)):
                            element1 = z_sand_box_index[k]
                              
                            if sandbox_grid[y_nc_ur,x_nc_ur,element1] == 0:                           
                                element2 = bath_map[y_nc_ur,x_nc_ur]
                                if element2 > z_sand_box[k]:
                                    sandbox_grid[y_nc_ur,x_nc_ur,element1] =  grid_lobe_new[x_c,y_c,k]    
        
                            if sandbox_grid[y_nc_udr,x_nc_udr,element1] == 0:                           
                               element2 = bath_map[y_nc_udr,x_nc_udr]
                               if element2 > z_sand_box[k]:
                                   sandbox_grid[y_nc_udr,x_nc_udr,element1] =  grid_lobe_new[x_c,y_c,k]  
                                        
                            if sandbox_grid[y_nc_udr,x_nc_ur,element1] == 0:                           
                               element2 = bath_map[y_nc_udr,x_nc_ur]
                               if element2 > z_sand_box[k]:
                                   sandbox_grid[y_nc_udr,x_nc_ur,element1] =  grid_lobe_new[x_c,y_c,k]     
        
                            if sandbox_grid[y_nc_ur,x_nc_udr,element1] == 0:                           
                               element2 = bath_map[y_nc_ur,x_nc_udr]
                               if element2 > z_sand_box[k]:
                                  sandbox_grid[y_nc_ur,x_nc_udr,element1] =  grid_lobe_new[x_c,y_c,k] 
                                  
              #lobe + mud layer
              
                original_sandbox_grid = sandbox_grid.copy()
              
                for i in range(len(new_coord)):
                    x_nc_ur = round(new_coord[i][0])
                    y_nc_ur = round(new_coord[i][1])
                        
                    x_nc_udr = math.floor(new_coord[i][0])
                    y_nc_udr = math.floor(new_coord[i][1])
                    
                    
                    
                  
                    if verify_range(x_nc_ur, y_nc_ur, x_nc_udr, y_nc_udr, nx, ny):          
                        for k in range(len(z_grid_lobe)-1):
                            element1 = z_sand_box_index[k]
                          
                            val1 = original_sandbox_grid[y_nc_ur,x_nc_ur,element1]
                            val2 = original_sandbox_grid[y_nc_ur,x_nc_ur,element1 +1]
                          
                            if val1 != 0 and val2 == 0:
                                for n in range(0,n_cell_mud):
                                    z_value = element1 + n
                                    
                                    
                                    if z_value < int(nz/cellsize_z):
                                        sandbox_grid[y_nc_ur,x_nc_ur,z_value] = mud_property + 2
                                      
                                      
                            val1 = original_sandbox_grid[y_nc_udr,x_nc_udr,element1]
                            val2 = original_sandbox_grid[y_nc_udr,x_nc_udr,element1 +1]
                         
                            if val1 != 0 and val2 == 0:
                                for n in range(0,n_cell_mud):
                                    z_value = element1 + n
                                    
                                    if z_value < int(nz/cellsize_z):
                                        sandbox_grid[y_nc_udr,x_nc_udr,z_value] = mud_property +2 
                                       
                                       
                                      
                            val1 = original_sandbox_grid[y_nc_udr,x_nc_ur,element1]
                            val2 = original_sandbox_grid[y_nc_udr,x_nc_ur,element1 +1]
                         
                            if val1 != 0 and val2 == 0:
                               for n in range(0,n_cell_mud):
                                   z_value = element1 + n
                                   
                                   if z_value < int(nz/cellsize_z):
                                       sandbox_grid[y_nc_udr,x_nc_ur,z_value] = mud_property +2  
                                      
                                      
                            val1 = original_sandbox_grid[y_nc_ur,x_nc_udr,element1]
                            val2 = original_sandbox_grid[y_nc_ur,x_nc_udr,element1 +1]
                        
                            if val1 != 0 and val2 == 0:
                                for n in range(0,n_cell_mud):
                                    z_value = element1 + n
                                    
                                    if z_value < int(nz/cellsize_z):
                                        sandbox_grid[y_nc_ur,x_nc_udr,z_value] = mud_property +2
                                          
        #print('n',n)                         
        grid(sandbox_grid,1,1,1,plot_slices=True, slice_x=20, slice_y=90, slice_z=6)
        f = f+1
        #print('f',f)
        dict_sandbox[f] =  sandbox_grid.copy()    
                                 
                          
    return(sandbox_grid,dict_sandbox)
       
    
    