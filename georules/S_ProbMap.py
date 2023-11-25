# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago

lobe_map - Function generating the bathymetric map  as the num_of_lobes lobes are deposited
inputs: 
    nx = number of cells
    ny = number of cells
    cell_size = size of each cell in m
    width = maximum lobe width int
    length = maximum lobe length int
    tmax = maximum thickness int
    num_of_lobes = number of lobes to deposit
    power = compensation power (See Jo. 2020)
    tm = transition matrix for markov chain
    startstate = state (the state is the quadrant- there are 4 quadrants the user can determine the angles betwwen each quadrant)
    
output:
    Bathymetry_steps = maps of different lobes deposited
    ls = list with centroids 
    ps = list with probability maps
    angle_list,column_corner_list,row_corner_list = requirements for gridding see S_rotate_coord for explanation
    lobe_array = array of the lobe of interest useful for gridding see S_rotate_coord (equivalent to image)

"""
import numpy as np
from S_Stacking import stacking
from S_Markov import stack_forecast
from S_RotationAngle import rot_angle


### Example of parameters

#nx = 400 
#ny = 400 
#cell_size = 100 
#width = 15000 
#lenght = 30000 
#tmax = 2 
#num_of_lobes = 10  
#power = 5

# import from refactors
from lobes import LobeGeometry, lobe_deposition
from bathymetry import BathymetryLayers


def Lobe_map(nx, ny,cell_size,width,lenght,tmax,num_of_lobes,power, tm, startstate,quadrant_angles,source,a1,a2,cellsize_z,n_mud):

    # Calculate lobe array with drop geometry
    lobe_geometry = LobeGeometry(width=width,length=lenght, tmax=tmax, cell_size=cell_size)

    # Set initial bathymetry
    bathymetry = BathymetryLayers(nx, ny)

    n=0 

    #Create list with centroids
    ls = []

    #create list with probability maps
    ps = []

    # Use markov-chains to find stacking patterns
    stack_list = stack_forecast(startstate, num_of_lobes, tm) # function inputs start state ="Q1"
    print(stack_list)
    #source= channel
    
    # create list with parameters to find coordinates needed for gridding
    angle_list = []
    column_corner_list =[]
    row_corner_list = []
    

    while n < num_of_lobes: 
        if n == 0:
            #Lobe Placement
            # Select Source Location - centroid (No modification)
            elevation_s = bathymetry.get_elevation(n)
            prob_s = (1/np.transpose(elevation_s))**power ## compensational power  ### Sera necesario tenerlo que trasponer???\
            prob_s[:,int(lobe_geometry.scaled_length):int(prob_s.shape[1])] = 0 
            ps.append(prob_s)
                
            #normalize prob_s
            prob_sum = np.sum(prob_s) #prob_s has to be positive
            norm_prob_s = prob_s/prob_sum
            # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
            index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
            # Convert the flattened index to a row and column index
            a, b = divmod(index, elevation_s.shape[1])
            Location_ = [a,b] #location of the centroid a = column , b = row
            ls.append(Location_)
            
            #Find rotation angle
            rotation_angle = rot_angle(Location_,source)
            angle_list.append(rotation_angle) 
            
            res = lobe_deposition(
                Location_,
                lobe_geometry.scaled_length,
                lobe_geometry.scaled_width,
                lobe_geometry.lobe_thickness,
                rotation_angle,
                bathymetry,
            )
            Bathymetry_, thick_updated, col_corn, row_corn = res
            
            bathymetry.add_layer(Bathymetry_)
            print("plot layer")
            fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
            fig.show()
            
            column_corner_list.append(col_corn)
            row_corner_list.append(row_corn)
        
        else: 
           
           # select stacking angles depending on current state
           current_state = stack_list[n] # according to Markov Chain
           
           if current_state == "NMA":
               
               # Select Source Location - centroid (No modification)
               elevation_s = bathymetry.get_elevation(n)
               prob_s = (1/np.transpose(elevation_s))**power ## compensational power  ###Sera necesario tenerlo que trasponer???\
               ps.append(prob_s)
                   
               #normalize prob_s
               prob_sum = np.sum(prob_s) #prob_s has to be positive
               norm_prob_s = prob_s/prob_sum
               # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
               index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
               # Convert the flattened index to a row and column index
               a, b = divmod(index, elevation_s.shape[1])
               Location_ = [a,b] #location of the centroid a = column , b = row
               ls.append(Location_)  
                
               
               #Find rotation angle
               rotation_angle = rot_angle(Location_,source) 
               angle_list.append(rotation_angle)
               
               res = lobe_deposition(
                   Location_,
                   lobe_geometry.scaled_length,
                   lobe_geometry.scaled_width,
                   lobe_geometry.lobe_thickness,
                   rotation_angle,
                   bathymetry,
                ) 
               Bathymetry_, thick_updated, col_corn, row_corn = res
               bathymetry.add_layer(Bathymetry_)
               
               print("plot layer")
               fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               fig.show()

               column_corner_list.append(col_corn)
               row_corner_list.append(row_corn)
               
           elif current_state == "HF":
               
               #Bathymetry_ = np.transpose(Bathymetry_)
               Bathymetry_inverse = 1 - bathymetry.layers[-1] 
               min_value = np.min(Bathymetry_inverse)
               max_value = np.max(Bathymetry_inverse)

               #create probability map of the elevations of the mud
               norm_elevation = (Bathymetry_inverse-min_value)/(max_value-min_value)

               #create an array with mud thickness
               layer_mud_thick = cellsize_z * n_mud
               mud_elevation = np.full((len(norm_elevation[0]),len(norm_elevation[1])),layer_mud_thick)

               #multiply mud_elevation * norm_elevation to know the thickness of the mud layer 
               mud_thickness = mud_elevation * norm_elevation

               Bathymetry_ = Bathymetry_ + mud_thickness
               ls.append([]),ps.append([]),column_corner_list.append([]),row_corner_list.append([]),angle_list.append([])
               
               # update bathymetry
               bathymetry.add_layer(Bathymetry_)
               print("plot layer")
               fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               fig.show()
        
           else:
               angle1 = quadrant_angles[current_state][0]
               angle2 = quadrant_angles[current_state][1]
               
               # Stacking 
               Location_, prob_s, prob_bsm = stacking(ls, n, lobe_geometry.scaled_width, 0.2, nx, ny, bathymetry.layers[-1], power,angle1, angle2) # 0.2 debe ser cambiados por valores de funciones
               ls.append(Location_),ps.append(prob_bsm)
           
               #Find rotation angle
               rotation_angle = rot_angle(Location_,source)
               angle_list.append(rotation_angle)
           
               res = lobe_deposition(
                   Location_,
                   lobe_geometry.scaled_length,
                   lobe_geometry.scaled_width,
                   lobe_geometry.lobe_thickness,
                   rotation_angle, 
                   bathymetry,
                )
               Bathymetry_, thick_updated, col_corn, row_corn = res
               
               column_corner_list.append(col_corn)
               row_corner_list.append(row_corn)

               # update bathymetry
               bathymetry.add_layer(Bathymetry_)
               print("plot layer")
               fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               fig.show()

        # Bathymetry_steps.append(Bathymetry_.copy())
        Bathymetry_steps = bathymetry.layers.copy()
        
        n = n+1 
        print(n) #track progress
        
    return (Bathymetry_steps,ls,ps,stack_list,angle_list,column_corner_list,row_corner_list,lobe_geometry.lobe_thickness) 

    
