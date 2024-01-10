# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
@refactoring: Daniel Willhelm

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
    centroid_coords = a list of centroid coordinates
    ps = list with probability maps
    angle_list,column_corner_list,row_corner_list = requirements for gridding see S_rotate_coord for explanation
    lobe_array = array of the lobe of interest useful for gridding see S_rotate_coord (equivalent to image)

"""
import numpy as np
from S_Stacking import stacking
from markov import  MarkovSequence
from S_RotationAngle import rot_angle


# import from refactors
from lobes import LobeGeometry, lobe_deposition
from bathymetry import BathymetryLayers

def normalize_probability(prob_s) -> np.ndarray:
    """Normalize the ##WHAT## Probability.""" 
    # NOTE: needs better docstring
    prob_sum = np.sum(prob_s) #prob_s has to be positive
    norm_prob_s = prob_s/prob_sum
    return norm_prob_s

def get_norm_elevation(bathymetry:BathymetryLayers, idx:int=None) -> np.ndarray:
    """Create probability map of the elevations of the mud.""" 
    idx = -1 if idx is None else idx
    inv_bath = 1 - bathymetry.layers[idx]
    norm_elevation = (inv_bath - inv_bath.min())/(inv_bath.max() - inv_bath.min())
    return norm_elevation

def Lobe_map(
        nx,
        ny,
        cell_size,
        width,
        lenght,
        tmax,
        num_of_lobes,
        power,
        transition_matrix,
        startstate,
        quadrant_angles,
        source,
        cellsize_z,
        n_mud,
        states
    ):
    """Lobe Map"""
    # Calculate lobe array with drop geometry
    lobe_geometry = LobeGeometry(width=width,length=lenght, tmax=tmax, cell_size=cell_size)

    # Set initial bathymetry
    bathymetry = BathymetryLayers(nx, ny)

    n=0 

    #Create list with centroids
    centroid_coords = []

    #create list with probability maps
    ps = []

    # Use markov-chains to find stacking patterns
    ms = MarkovSequence(states=states, transition_matrix=transition_matrix)
    stack_list = ms.get_sequence(sequence_len = num_of_lobes, init_state = startstate)
    print(stack_list)
    #source= channel
    
    # create list with parameters to find coordinates needed for gridding
    angle_list = []
    column_corner_list =[]
    row_corner_list = []
    

    # Lobe placement
    while n < num_of_lobes: 
        # intialize lobe 
        if n == 0:
            a, b = np.random.randint(0, nx), np.random.randint(0, ny)
            lobe_location = [a,b] #location of the centroid a = column , b = row
            centroid_coords.append(lobe_location)
            
            #Find rotation angle
            rotation_angle = rot_angle(lobe_location, source)
            angle_list.append(rotation_angle) 
            
            res = lobe_deposition(
                lobe_location,
                lobe_geometry.scaled_length,
                lobe_geometry.scaled_width,
                lobe_geometry.lobe_thickness,
                rotation_angle,
                bathymetry,
            )
            Bathymetry_, thick_updated, col_corn, row_corn = res
            
            bathymetry.add_layer(Bathymetry_)
            
            # print("plot layer")
            # fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
            # fig.show()
            
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
                   
               norm_prob_s = normalize_probability(prob_s)

               # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
               index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
               # Convert the flattened index to a row and column index
               a, b = divmod(index, elevation_s.shape[1])
               lobe_location = [a, b] #location of the centroid a = column , b = row
               centroid_coords.append(lobe_location)  # ?
                
               
               #Find rotation angle
               rotation_angle = rot_angle(lobe_location, source) 
               angle_list.append(rotation_angle)
               
               res = lobe_deposition(
                   lobe_location,
                   lobe_geometry.scaled_length,
                   lobe_geometry.scaled_width,
                   lobe_geometry.lobe_thickness,
                   rotation_angle,
                   bathymetry,
                ) 
               Bathymetry_, thick_updated, col_corn, row_corn = res
               bathymetry.add_layer(Bathymetry_)
               
               # print("plot layer")
               # fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               # fig.show()

               column_corner_list.append(col_corn)
               row_corner_list.append(row_corn)
               
           elif current_state == "HF":
               
               norm_elevation = get_norm_elevation(bathymetry)

               #create an array with mud thickness
               layer_mud_thick = cellsize_z * n_mud
               mud_elevation = np.full((len(norm_elevation[0]),len(norm_elevation[1])),layer_mud_thick)

               #multiply mud_elevation * norm_elevation to know the thickness of the mud layer 
               mud_thickness = mud_elevation * norm_elevation

               Bathymetry_ = Bathymetry_ + mud_thickness
               centroid_coords.append([]),ps.append([]),column_corner_list.append([]),row_corner_list.append([]),angle_list.append([])
               
               # update bathymetry
               bathymetry.add_layer(Bathymetry_)
               
               # print("plot layer")
               # fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               # fig.show()
        
           else:
               # Angles where new centroid should go
               angle1 = quadrant_angles[current_state][0]
               angle2 = quadrant_angles[current_state][1]
               
               #centroid coords
               if len(centroid_coords[n-1]) == 0: #this will happen when the last event was HF
                    #Find area to move the lobe
                   centroid = centroid_coords[n-2]
               else:
                   centroid = centroid_coords[n-1]
               
               
               # Stacking 
               lobe_location, prob_bsm = stacking(
                   centroid=centroid,
                   lobe_radius=lobe_geometry.scaled_width,
                   nx=nx,
                   ny=ny,
                   bathymetry_layer=bathymetry.layers[-1],
                   angle_move1=angle1,
                   angle_move2=angle2,
                ) 
               centroid_coords.append(lobe_location)
               ps.append(prob_bsm)
           
               #Find rotation angle
               rotation_angle = rot_angle(lobe_location,source)
               angle_list.append(rotation_angle)
           
               res = lobe_deposition(
                   lobe_location,
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
               
               # print("plot layer")
               # fig, ax = bathymetry._plot_layer(f'layer-{n}', idx=n, save=False)
               # fig.show()

        # NOTE: `Bathymetry_steps` was being used as a "Global Variable" :(
        Bathymetry_steps = bathymetry.layers.copy()
        
        n = n+1 
        print(n) #track progress
        
        # prepare output
        output = (
            Bathymetry_steps,
            centroid_coords,
            ps,
            stack_list,
            angle_list,
            column_corner_list,
            row_corner_list,
            lobe_geometry.lobe_thickness
        )
    return output 





    
