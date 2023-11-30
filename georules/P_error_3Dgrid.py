# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:37:53 2023

@author: nc25884
"""

lobe_length = Value_4_lenght[0]
lobe_wmax = Value_2_wmax[0]
cell_size = Value_6_cellsize[0]
lobe_image = lobe_image
cellsize_z = Value_19_cellsize_z[0]
lobe_tmax = Value_3_tmax[0]
global_prop = Value_15_gp[0]
mud_property = Value_21_mud_property[0]
n_cell_mud = Value_20_n_mud[0]
a1 = Value_13_a1[0]
a2 = Value_14_a2[0]
nx = Value_7_nx[0]
ny =Value_8_ny[0]

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
grid_lobe_normal_mud = grid_lobe(lobe_image,lobe_length,lobe_wmax,
                                 cellsize_z,cell_size,lobe_tmax,
                                 global_prop,mud_property,n_cell_mud,1,a1,a2)

#Sandbox_grid
sandbox_grid = np.zeros((nx,ny,math.ceil(nz/cellsize_z))) #### cambie math.ceil

#nz_values - values for z axis
nz_values = np.linspace(0,nz-cellsize_z,math.ceil(nz/cellsize_z)) #### cambie math.ceil

## Function to filter values that are outside the sandbox
def verify_range(x_nc_ur,y_nc_ur,x_nc_udr,y_nc_udr,nx,ny):
      if 0 <= x_nc_ur <= nx-1 and 0 <= y_nc_ur <= ny-1 and 0 <= x_nc_udr <= nx-1  and 0 <= y_nc_udr <= ny-1:
          return True
      else:
          return False
      
###Lobe 1
n = 1

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

##Lobe 2
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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
            
          
     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
         fill_out_array[y_nc_floor][x_nc_floor] = 1
        
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
       
         else:
            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
   
     
     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
           fill_out_array[y_nc_floor][x_nc_ceil] = 1
        
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
       
           else:
               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
   
     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
           fill_out_array[y_nc_ceil][x_nc_floor] = 1
       
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
      
           else:
               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 

#### Lobe 3

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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
            
          
     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
         fill_out_array[y_nc_floor][x_nc_floor] = 1
        
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
       
         else:
            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
   
     
     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
           fill_out_array[y_nc_floor][x_nc_ceil] = 1
        
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
       
           else:
               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
   
     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
           fill_out_array[y_nc_ceil][x_nc_floor] = 1
       
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
      
           else:
               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 


#### Lobe 4

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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
            
          
     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
         fill_out_array[y_nc_floor][x_nc_floor] = 1
        
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
       
         else:
            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
   
     
     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
           fill_out_array[y_nc_floor][x_nc_ceil] = 1
        
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
       
           else:
               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
   
     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
           fill_out_array[y_nc_ceil][x_nc_floor] = 1
       
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
      
           else:
               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 

#### Lobe 5

n = 5
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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
            
          
     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
         fill_out_array[y_nc_floor][x_nc_floor] = 1
        
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
       
         else:
            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
   
     
     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
           fill_out_array[y_nc_floor][x_nc_ceil] = 1
        
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
       
           else:
               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
   
     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
           fill_out_array[y_nc_ceil][x_nc_floor] = 1
       
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
      
           else:
               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 


#### Lobe 6

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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
            
          
     if bath_dif[y_nc_floor][x_nc_floor]> 0.0001 and fill_out_array[y_nc_floor][x_nc_floor] == 0:
         fill_out_array[y_nc_floor][x_nc_floor] = 1
        
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_floor,:])

         if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
            sandbox_grid[y_nc_floor,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid[y_nc_floor,x_nc_floor,j+ z_cell_number] = mud_property +2 
       
         else:
            sandbox_grid[y_nc_floor,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]       
   
     
     if bath_dif[y_nc_floor][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_floor][x_nc_ceil] == 0:
           fill_out_array[y_nc_floor][x_nc_ceil] = 1
        
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_floor,x_nc_ceil,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_floor,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_floor,x_nc_ceil,j+ z_cell_number] = mud_property +2 
       
           else:
               sandbox_grid[y_nc_floor,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j]
   
     if bath_dif[y_nc_ceil][x_nc_floor]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_floor] == 0:
           fill_out_array[y_nc_ceil][x_nc_floor] = 1
       
           z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

          ### Find where the deposition starts
           j = np.count_nonzero(sandbox_grid[y_nc_ceil,x_nc_floor,:])

           if sandbox_grid.shape[2]-j >=  grid_lobe_new.shape[2]:     
              sandbox_grid[y_nc_ceil,x_nc_floor,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
              sandbox_grid[y_nc_ceil,x_nc_floor,j+ z_cell_number] = mud_property +2 
      
           else:
               sandbox_grid[y_nc_ceil,x_nc_floor,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 

#### Lobe 7

sandbox_grid_copy = sandbox_grid.copy()

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
    
     x_nc_ceil = round(verify_range_new_coord[i][0])
     y_nc_ceil = round(verify_range_new_coord[i][1])
     
     x_nc_floor = math.floor(verify_range_new_coord[i][0])
     y_nc_floor = math.floor(verify_range_new_coord[i][1])
     
     
     if bath_dif[y_nc_ceil][x_nc_ceil]> 0.0001 and fill_out_array[y_nc_ceil][x_nc_ceil] == 0:
         fill_out_array[y_nc_ceil][x_nc_ceil] = 1
         
         z_cell_number = round(lobe_thickness_new[y_c,x_c]/cellsize_z) 

        ### Find where the deposition starts
         j = np.count_nonzero(sandbox_grid_copy[y_nc_ceil,x_nc_ceil,:])

         if sandbox_grid_copy.shape[2]-j > grid_lobe_new.shape[2]:     
            sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
            sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_property +2 
        
         else:
            sandbox_grid_copy[y_nc_ceil,x_nc_ceil,j:] = grid_lobe_new[x_c,y_c,:sandbox_grid.shape[2]-j] 
            
    






        
      
