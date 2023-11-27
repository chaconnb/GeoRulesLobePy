# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 22:20:24 2023

@author: nc25884

prueba del lobulo 7
"""

## lobe 7

n = 7
print(n)

sandbox_grid_copy2 = sandbox_grid_copy.copy()

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
            z_cell = sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j]
    
    
            while z_cell != 0:
                j = j+1
                z_cell = sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j]
         
            if sandbox_grid_copy2.shape[2]-j >  grid_lobe_new.shape[2]:     
                sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j:j+ z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j+ z_cell_number] = mud_prop +2 
            
            else:
                sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j: j + grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy2.shape[2]-j]
                
                print(y_nc_ceil,x_nc_ceil,j,x_c,y_c,sandbox_grid_copy2.shape[2]-j)
                                
             
            x_nc_floor = math.floor(verify_range_new_coord[i][0])
            y_nc_floor = math.floor(verify_range_new_coord[i][1])
              
            if fill_out_array[x_nc_floor][y_nc_floor] == 0: 
                fill_out_array[x_nc_floor][y_nc_floor] = 1
                
                ### Find where the deposition starts
                j = 0
                z_cell = sandbox_grid_copy2[y_nc_floor,x_nc_floor,j]
        
        
                while z_cell != 0:
                    j = j+1
                    z_cell = sandbox_grid_copy2[y_nc_floor,x_nc_floor,j]
             
                if sandbox_grid_copy2.shape[2]-j > grid_lobe_new.shape[2]:   
                    sandbox_grid_copy2[y_nc_floor,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                    sandbox_grid_copy2[y_nc_floor,x_nc_floor,j+z_cell_number] = mud_prop +2 
                
                else:
                    sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j:j + grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy2.shape[2]-j]
                    
                
            if fill_out_array[x_nc_ceil][y_nc_floor] == 0: 
                fill_out_array[x_nc_ceil][y_nc_floor] = 1
               
                ### Find where the deposition starts
                j = 0
                z_cell = sandbox_grid_copy2[y_nc_floor,x_nc_ceil,j]
        
        
                while z_cell != 0:
                    j = j+1
                    z_cell = sandbox_grid_copy2[y_nc_floor,x_nc_ceil,j]
                    
             
                if sandbox_grid_copy2.shape[2]-j > grid_lobe_new.shape[2]:   
                    sandbox_grid_copy2[y_nc_floor,x_nc_ceil,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                    sandbox_grid_copy2[y_nc_floor,x_nc_ceil,j+z_cell_number] = mud_prop +2 
                
                else:
                    sandbox_grid_copy2[y_nc_ceil,x_nc_ceil,j:j + grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy2.shape[2]-j]
                    
                    
            if fill_out_array[x_nc_floor][y_nc_ceil] == 0: 
                fill_out_array[x_nc_floor][y_nc_ceil] = 1
            
                ### Find where the deposition starts
                j = 0
                z_cell = sandbox_grid_copy2[y_nc_ceil,x_nc_floor,j]
        
        
                while z_cell != 0:
                    j = j+1
                    z_cell = sandbox_grid_copy2[y_nc_ceil,x_nc_floor,j]
             
                if sandbox_grid_copy2.shape[2]-j >  grid_lobe_new.shape[2]:   
                    sandbox_grid_copy2[y_nc_ceil,x_nc_floor,j:j+z_cell_number] = grid_lobe_new[x_c,y_c,:z_cell_number] 
                    sandbox_grid_copy2[y_nc_ceil,x_nc_floor,j+z_cell_number] = mud_prop +2 
                
                else:
                    sandbox_grid_copy2[y_nc_ceil,x_nc_floor,j:j + grid_lobe_new.shape[2]] = grid_lobe_new[x_c,y_c,:sandbox_grid_copy2.shape[2]-j]
                    
                

