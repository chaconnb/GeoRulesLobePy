# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:50:32 2023

@author: Nataly Chacon-Buitrago
"""

from S_lobe_facies import grid_lobe
from S_RotateCoord import rotate_coord
from S_Lobegeom import drop_geometry
import matplotlib.pyplot as plt 
import numpy as np
import math


#inputs
lobe_length = Value_4_lenght[0]
cell_size = Value_6_cellsize[0]
lobe_wmax = Value_2_wmax[0]
cellsize_z = Value_19_cellsize_z[0]
lobe_tmax = Value_3_tmax[0]
global_prop = Value_15_gp[0]
mud_property = Value_21_mud_property[0]
n_cell_mud = Value_20_n_mud[0]
a1 = Value_13_a1[0]
a2 = Value_14_a2[0]
mud_prop = 0.10
nx = 250
ny = 250

#Built standard lobe
lobe_x =  [i for i in range(0,lobe_length,100)]
y_interval = cell_size

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
#sandbox_grid = np.zeros((nx,ny,240))



#nz_values - values for z axis
nz_values = np.linspace(0,nz-cellsize_z,int(nz/cellsize_z))

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
 
 
   
#lobe 1
n = 1
print(n)
    
new_coord = rotate_coord(coord, angle_stack[n-1], lobe_image,columns_corner[n-1],rows_corner[n-1])
bath_map = Bathymetry_maps[n]
            
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
    
    
##lobe 2
n = 2 
print(n)

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 
bath_max = np.max(bath_dif)

### Find new lobe with new thickness 
lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,bath_max,lobe_x,y_interval, a1, a2)
grid_lobe_new =  grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,bath_max,global_prop,mud_property,n_cell_mud,0,a1,a2)  

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
    
    
      if lobe_thickness_new[y_c,x_c]!= 0:
          #print(lobe_thickness_new[y_c,x_c],y_c,x_c)
        z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)
        
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
         
            if sandbox_grid.shape[2]-j >  grid_lobe_new.shape[2]:     
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j: grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
                
            
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
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
            
        if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
            fill_out_array[x_nc_ceil][y_nc_floor] = 1
           
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
                
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j]
                
        
                
        if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
            fill_out_array[x_nc_floor][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_floor,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 


#### lobe 3

n = 3 
print(n)

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 
bath_max = np.max(bath_dif)

### Find new lobe with new thickness 
lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,bath_max,lobe_x,y_interval, a1, a2)
grid_lobe_new =  grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,bath_max,global_prop,mud_property,n_cell_mud,0,a1,a2)  

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
    
    
      if lobe_thickness_new[y_c,x_c]!= 0:
          #print(lobe_thickness_new[y_c,x_c],y_c,x_c)
        z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)
        
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
         
            if sandbox_grid.shape[2]-j >  grid_lobe_new.shape[2]:     
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j: grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
                
            
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
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
            
        if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
            fill_out_array[x_nc_ceil][y_nc_floor] = 1
           
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
                
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j]
                
        
                
        if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
            fill_out_array[x_nc_floor][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_floor,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 


#### lobe 4

n = 4
print(n)

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 
bath_max = np.max(bath_dif)

### Find new lobe with new thickness 
lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,bath_max,lobe_x,y_interval, a1, a2)
grid_lobe_new =  grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,bath_max,global_prop,mud_property,n_cell_mud,0,a1,a2)  

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
    
    
      if lobe_thickness_new[y_c,x_c]!= 0:
          #print(lobe_thickness_new[y_c,x_c],y_c,x_c)
        z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)
        
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
         
            if sandbox_grid.shape[2]-j >  grid_lobe_new.shape[2]:     
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j: grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
                
            
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
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 
            
        if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
            fill_out_array[x_nc_ceil][y_nc_floor] = 1
           
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_floor,x_nc_ceil,j]
                
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_ceil,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j]
                
        
                
        if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
            fill_out_array[x_nc_floor][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid[y_nc_ceil,x_nc_floor,j]
         
            if sandbox_grid.shape[2]-j > grid_lobe_new.shape[2]:   
                sandbox_grid[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid[y_nc_ceil,x_nc_floor,j:grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,sandbox_grid.shape[2]-j] 

##### HF = 5
n = 5
print (n)

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

# lobe 6

sandbox_grid_copy = sandbox_grid.copy()

n = 6
print(n)

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 
bath_max = np.max(bath_dif)

### Find new lobe with new thickness 
lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,bath_max,lobe_x,y_interval, a1, a2)
grid_lobe_new =  grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,bath_max,global_prop,mud_property,n_cell_mud,0,a1,a2)  

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
    
    
      if lobe_thickness_new[y_c,x_c]!= 0:
          #print(lobe_thickness_new[y_c,x_c],y_c,x_c)
        z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)
        
        x_nc_ceil = round(verify_range_new_coord[i][0])
        y_nc_ceil = round(verify_range_new_coord[i][1])
        
        if fill_out_array[x_nc_ceil][y_nc_ceil] == 0: 
            fill_out_array[x_nc_ceil][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j]
         
            if sandbox_grid_copy.shape[2]-j >=  grid_lobe_new.shape[2]:     
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]  
                
                
        x_nc_floor = math.floor(verify_range_new_coord[i][0])
        y_nc_floor = math.floor(verify_range_new_coord[i][1])
          
        if fill_out_array[x_nc_floor][y_nc_floor] == 0: 
            fill_out_array[x_nc_floor][y_nc_floor] = 1
            
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid_copy[y_nc_floor,x_nc_floor,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid_copy[y_nc_floor,x_nc_floor,j]
         
            if sandbox_grid_copy.shape[2]-j >= grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j] 
                
            
        if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
            fill_out_array[x_nc_ceil][y_nc_floor] = 1
           
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid_copy[y_nc_floor,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid_copy[y_nc_floor,x_nc_ceil,j]
                
         
            if sandbox_grid_copy.shape[2]-j >= grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]
                
        
                
        if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
            fill_out_array[x_nc_floor][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = 0
            z_cell = sandbox_grid_copy[y_nc_ceil,x_nc_floor,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid_copy[y_nc_ceil,x_nc_floor,j]
         
            if sandbox_grid_copy.shape[2]-j >=  grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]
 
#######################

n = 7
print(n)

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 
bath_max = np.max(bath_dif)

### Find new lobe with new thickness 
lobe_thickness_new = drop_geometry(lobe_wmax,lobe_length,bath_max,lobe_x,y_interval, a1, a2)
grid_lobe_new =  grid_lobe(lobe_thickness_new,lobe_length,lobe_wmax,cellsize_z,cell_size,bath_max,global_prop,mud_property,n_cell_mud,0,a1,a2)  

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
    
    
      if lobe_thickness_new[y_c,x_c]!= 0:
          #print(lobe_thickness_new[y_c,x_c],y_c,x_c)
        z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)
        
        x_nc_ceil = round(verify_range_new_coord[i][0])
        y_nc_ceil = round(verify_range_new_coord[i][1])
        
        if fill_out_array[x_nc_ceil][y_nc_ceil] == 0: 
            fill_out_array[x_nc_ceil][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])
         
            if sandbox_grid_copy.shape[2]-j >=  grid_lobe_new.shape[2]:     
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]  
                
                
        x_nc_floor = math.floor(verify_range_new_coord[i][0])
        y_nc_floor = math.floor(verify_range_new_coord[i][1])
          
        if fill_out_array[x_nc_floor][y_nc_floor] == 0: 
            fill_out_array[x_nc_floor][y_nc_floor] = 1
            
            ### Find where the deposition starts
            j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])
         
            if sandbox_grid_copy.shape[2]-j >= grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j] 
                
            
        if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
            fill_out_array[x_nc_ceil][y_nc_floor] = 1
           
            ### Find where the deposition starts
            j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])
                
         
            if sandbox_grid_copy.shape[2]-j >= grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]
                
        
                
        if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
            fill_out_array[x_nc_floor][y_nc_ceil] = 1
        
            ### Find where the deposition starts
            j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])
         
            if sandbox_grid_copy.shape[2]-j >=  grid_lobe_new.shape[2]:   
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy.shape[2]-j]
 




                
 



    

# #### test con los numeros escogidos

# y_c = 42
# x_c = 93

# z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z)

# sandbox_grid_copy2 = sandbox_grid_copy.copy()

# x_nc_ceil = 160
# y_nc_ceil = 1
# fill_out_array[x_nc_ceil][y_nc_ceil] = 0



# if fill_out_array[x_nc_ceil][y_nc_ceil] == 0: 
#     fill_out_array[x_nc_ceil][y_nc_ceil] = 1

#     ### Find where the deposition starts (Where in the column the value is different than zero)
#     j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])

#     if sandbox_grid_copy2.shape[2]-j >=  grid_lobe_new.shape[2]: 
#         sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
#         sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
    
#     else:
#         sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy2.shape[2]-j]







