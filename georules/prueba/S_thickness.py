# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:59:37 2023

@author: Nataly Chacon-Buitrago
"""
from S_lobe_facies import grid_lobe
from S_RotateCoord import rotate_coord
import matplotlib.pyplot as plt 
import numpy as np


### inputs
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
nx = 100
ny = 100





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
    
new_coord = rotate_coord(coord, angle_stack[n-1], lobe_image,columns_corner[n-1],rows_corner[n-1])
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
    
    
#lobe 2
n = 2 

bath_map = Bathymetry_maps[n]
bath_map_anterior = Bathymetry_maps[n-1] 
bath_dif = bath_map - bath_map_anterior 

#create mask to only work with current lobe's thickness

mask =  (bath_dif != 0) & (bath_dif > 0.0001)            
bma_thick = np.where(mask,bath_map_anterior,0) # mask where current lobe is in the bath_map_anterior map 
current_thick = np.where(mask,bath_map,0)
new_thick = current_thick - bma_thick
new_coord = rotate_coord(coord, angle_stack[n-1],lobe_image,columns_corner[n-1],rows_corner[n-1])
            
 
    
 
#visualization
 
fig = plt.figure()  
ax = fig.add_subplot(111)
ax.set_title("lobe_tmax_new")
plt.imshow(mask)
plt.colorbar()
plt.show()



# fig = plt.figure()  
# ax = fig.add_subplot(111)
# ax.set_title("anterior")
# plt.imshow(bath_map_anterior)
# plt.colorbar()
# plt.show()


# fig = plt.figure()  
# ax = fig.add_subplot(111)
# ax.set_title("dif")
# plt.imshow(bath_dif)
# plt.colorbar()
# plt.show()








   
    
    
    