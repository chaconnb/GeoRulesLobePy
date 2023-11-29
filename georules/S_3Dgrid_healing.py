# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:23:34 2023

@author: Nataly Chacon-Buitrago
"""
from S_lobe_facies import grid_lobe
from S_RotateCoord import rotate_coord
from S_Lobegeom import drop_geometry
import numpy as np
import math


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


def get_standard_lobe_coordinates(lobe_length:float, lobe_wmax:float, cell_size:float) -> np.ndarray:
    """Find coordinates of standard lobe in grid system.

    Parameters
    ----------
   lobe_length : float
       Maximum length lobe.
   lobe_wmax : float
       Maximum width lobe.
   cell_size : float
       Size of the grid x and y directions. 
    """
    coord = []
    for i in range(int(lobe_length/cell_size)):
        for j in range(int(lobe_wmax/cell_size)):
            coord.append([i,j])
    coord = np.array(coord)
    return coord

def verify_range(x_nc_ur,y_nc_ur,x_nc_udr,y_nc_udr,nx,ny):
    """Function to filter values that are outside the sandbox."""
    if 0 <= x_nc_ur <= nx-1 and 0 <= y_nc_ur <= ny-1 and 0 <= x_nc_udr <= nx-1  and 0 <= y_nc_udr <= ny-1:
        return True
    else:
        return False

def get_cell_num(n, cellsize_z, mud_property, nx, ny, Bathymetry_maps, sandbox_grid, nz_values):
    """Get the 'cell_num' array."""
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
    return cell_num

def get_initial_sandbox(sandbox_grid, cellsize_z, lobe_tmax, nx, ny, grid_lobe_normal_mud, new_coord, i, x_c, y_c) -> np.ndarray:
    """Update sandbox grid."""
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
    return sandbox_grid

def intialize_sandbox_grid(lobe_image, cellsize_z, lobe_tmax, nx, ny, nz, angle_stack, columns_corner, rows_corner, coord, grid_lobe_normal_mud, n):
    sandbox_grid = np.zeros((nx,ny,int(nz/cellsize_z)))
    new_coord = rotate_coord(
                coord=coord,
                angle=angle_stack[n-1],
                image=lobe_image,
                column_corner=columns_corner[n-1],
                row_corner=rows_corner[n-1], 
            )
    for i in range(len(coord)):
        x_c = coord[i][0]
        y_c = coord[i][1]
        sandbox_grid = get_initial_sandbox(sandbox_grid, cellsize_z, lobe_tmax, nx, ny, grid_lobe_normal_mud, new_coord, i, x_c, y_c)
    return sandbox_grid

def get_new_lobe(lobe_length, lobe_wmax, cell_size, cellsize_z, global_prop, mud_property, n_cell_mud, a1, a2, Bathymetry_maps, n):
    bath_map = Bathymetry_maps[n]
    bath_map_anterior = Bathymetry_maps[n-1] 
    bath_dif = bath_map - bath_map_anterior 
    bath_max = np.max(bath_dif)

                ### Find new lobe with new thickness 
    lobe_thickness_new = drop_geometry(
                    wmax=lobe_wmax,
                    lenght=lobe_length,
                    tmax=bath_max, 
                    x=[i for i in range(0, lobe_length, 100)],
                    y_interval=cell_size,
                    a1=a1,
                    a2=a2,
                )
    grid_lobe_new =  grid_lobe(
                    lobe_thi=lobe_thickness_new,
                    length=lobe_length,
                    wmax=lobe_wmax,
                    cellsize_z=cellsize_z,
                    cell_size=cell_size,
                    tmax=bath_max,
                    global_property=global_prop,
                    mud_prop=mud_property,
                    n_cell_mud=n_cell_mud,
                    mud_layer=0,
                    a1=a1,
                    a2=a2, 
                )
    
    return bath_dif,lobe_thickness_new,grid_lobe_new

def get_verified_coords(nx, ny, coord, new_coord):
    verify_range_index = np.where((new_coord[:, 0] >= 0) & (new_coord[:, 0] <= nx-1) & (new_coord[:, 1] >= 0) & (new_coord[:, 1] <= ny-1))[0] 
                #New coordinates of the values inside the sandbox
    verify_range_new_coord = new_coord[verify_range_index]
                #Find the equivalent coordinates of the verify_range_new_coord using the indices 
    verify_range_coord = coord[verify_range_index]
    return verify_range_new_coord,verify_range_coord

def sandbox(lobe_length,lobe_wmax,cell_size,lobe_image,cellsize_z,lobe_tmax,
            global_prop,mud_property,n_cell_mud,a1,a2,nx,ny,nz,n_lobe,angle_stack,
            columns_corner,rows_corner,Bathymetry_maps,quadrants):
    
    """
    Converts lobes in smoothed (healed) 2D bathymetry maps into a 3D grid. 
    The lobes have internal facies built using the S_lobe_facies function.

   Parameters
   ----------
   lobe_length : float
       Maximum length lobe.
   lobe_wmax : float
       Maximum width lobe.
   cell_size : float
       Size of the grid x and y directions. 
   lobe_tmax : float
       Maximum thickness lobe. 
   global_prop : float
       Total percentage in decimal of propetry the facies are modelling 
       (i.e. percentage of sand).
   mud_property : float 
   n_cell_mud : float
       Number of cells of mudstone that will cover each lobe. 
   a1 : float
       Parameter to built lobe object, usually 0.66.
   a2 : float
       Parameter to built the lobe object, usually 0.33.
   nx : float
       Number of cells in the x direction of the bathymetry map.
   ny : float
       Number of cells in the y direction of the bathymetry map.
   nz : float
       Maximum height in the 2D bathymetry maps. 
   n_lobe : float
       Number of lobes in the model.
   angle_stack :  list
       List of lobe apices with respect to the source. 
   columns_corner : list
       List of the locations of the top-left corners of the lobe images for
       each lobe with respect to the bathymetry map. Explanation 
       in S_PasteArray.py.
   rows_corner : list
       List of the locations of the top-left rows of the lobe images for
       each lobe w.r.t. the bathymetry map. Explanation 
      in S_PasteArray.py.
   Bathymetry_maps : BathymetryLayers
     Bathymetry layer instance.

   Returns
   -------
   sandboxgrid : array
       3D grid of lobes with facies.
   """

    #Find coordinates of standard lobe in grid system
    coord = get_standard_lobe_coordinates(lobe_length, lobe_wmax, cell_size)
    
    #Create 3D Lobe
    grid_lobe_normal_mud = grid_lobe(
        lobe_thi=lobe_image,
        length=lobe_length,
        wmax=lobe_wmax,
        cellsize_z=cellsize_z,
        cell_size=cell_size,
        tmax=lobe_tmax,
        global_property=global_prop,
        mud_prop=mud_property,
        n_cell_mud=n_cell_mud,
        mud_layer=1,
        a1=a1,
        a2=a2,
    )
    
    for n in range(1,n_lobe+1): 
        if n == 1:
            print(n)
            # intialize sandbox grid
            sandbox_grid = intialize_sandbox_grid(lobe_image, cellsize_z, lobe_tmax, nx, ny, nz, angle_stack, columns_corner, rows_corner, coord, grid_lobe_normal_mud, n)

        else:
            
            if quadrants[n-1] == "HF":
                print(n)
                #nz_values - values for z axis
                nz_values = np.linspace(0, nz-cellsize_z, int(nz/cellsize_z))
                cell_num = get_cell_num(n, cellsize_z, mud_property, nx, ny, Bathymetry_maps, sandbox_grid, nz_values)
                
                # NOTE: It looks like you do not use `cell_num` any where in the code after 
                # you create it - why do you have it? 
        
            else: 
                print(n)
                
                bath_dif, lobe_thickness_new, grid_lobe_new = get_new_lobe(lobe_length, lobe_wmax, cell_size, cellsize_z, global_prop, mud_property, n_cell_mud, a1, a2, Bathymetry_maps, n)  

                #Find new coordinates - new_coord is equivalent to coord
                new_coord = rotate_coord(coord, angle_stack[n-1], lobe_image, columns_corner[n-1], rows_corner[n-1])
                
                #Filter values that are outside the sandbox
                #Index of the values inside the sandbox
                verify_range_new_coord, verify_range_coord = get_verified_coords(nx, ny, coord, new_coord)
                
                ###create array to verify which coordinates have been filled out
                fill_out_array = np.zeros((nx,ny))
                
                for i in range(len(verify_range_coord)):
                    
                     x_c = verify_range_coord[i][0]
                     y_c = verify_range_coord[i][1]
                    
                     x_nc_ceil = round(verify_range_new_coord[i][0])
                     y_nc_ceil = round(verify_range_new_coord[i][1])
                     
                     x_nc_floor = math.floor(verify_range_new_coord[i][0])
                     y_nc_floor = math.floor(verify_range_new_coord[i][1])
                     
                     
                     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
                         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
                         
                         z_cell_number = round(lobe_thickness_new[y_c, x_c]/cellsize_z) 
                
                        ### Find where the deposition starts
                         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])
                
                         if sandbox_grid.shape[2]-j >  grid_lobe_new.shape[2]:     
                            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
                        
                         else:
                            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
                            
                            
                          
                     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
                         fill_out_array[y_nc_floor][x_nc_floor] = 1
                        
                         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 
                
                        ### Find where the deposition starts
                         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])
                
                         if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:     
                            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
                       
                         else:
                            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
                   
                     
                     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
                           fill_out_array[y_nc_floor][x_nc_ceil] = 1
                        
                           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 
                
                          ### Find where the deposition starts
                           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])
                
                           if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:     
                              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
                       
                           else:
                               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
                   
                     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
                           fill_out_array[y_nc_ceil][x_nc_floor] = 1
                       
                           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 
                
                          ### Find where the deposition starts
                           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])
                
                           if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:     
                              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
                      
                           else:
                               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
 
                   
     
    return(sandbox_grid)







