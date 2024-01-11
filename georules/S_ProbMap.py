# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
@refactoring: Daniel Willhelm
 

"""
import numpy as np
from S_Stacking import stacking
from markov import  MarkovSequence
from S_RotationAngle import rot_angle


# import from refactors
from lobes import LobeGeometry, lobe_deposition
from bathymetry import BathymetryLayers

def probability_sum_one(prob_s) -> np.ndarray:
    """Output array sums 1.""" 
    prob_sum = np.sum(prob_s) #prob_s has to be positive
    norm_prob_s = prob_s/prob_sum
    return norm_prob_s

def get_norm_elevation(bathymetry:BathymetryLayers, idx:int=None) -> np.ndarray:
    """Create probability map of the elevations of the mud.""" 
    idx = -1 if idx is None else idx
    inv_bath = 1 - bathymetry.layers[idx]
    norm_elevation = (inv_bath - inv_bath.min())/(inv_bath.max() - inv_bath.min())
    return norm_elevation

def HF_counter(stack_list_segment):
    "Counts how many HF Markov states are at the end of a list"
    count = 0
    for i in reversed(stack_list_segment):
        if i == "HF":
            count += 1
        else:
            return(count)
    

def Lobe_map(
        nx,
        ny,
        cell_size,
        width,
        lenght,
        tmax,
        num_of_lobes,
        transition_matrix,
        startstate,
        quadrant_angles,
        source,
        cellsize_z,
        n_mud,
        states
    ):
    """Function generating the bathymetric map  as the num_of_lobes lobes are deposited.
       
    Parameters
    ----------
    nx : int
        Sandbox size in the x direction.
    ny : int
        Sandbox size in the y direction.
    cell_size : int
        Size of each cell in m.
    width : int
        Maximum lobe width in m.
    lenght : int
        Maximum lobe lenght in m.
    tmax : int
        Maximum height of lome in m. 
    num_of_lobes : int
        Number of lobes to deposit.
    transition_matrix : np.array
        Transition matrix for Markov chain.
    startstate : string
        Starting state for generating Markov chain. 
    quadrant angles : dictionary
        A dictionary with keys representing Markov states and values containing 
        a list of angles indicating the starting and ending points for each key.
    source : list
        Coordinate where the source of sediment (channel) is located in the sandbox. 
    cellsize_z: int
        Size of each cell on the z-axis.
    n_mud: int
        Maximum number of mud cells that will be input into the sandbox at the 
        'HF' Markov state.
    states: list with strings
        List of Markov states.
    
    Returns
    -------
    Bathymetry_steprobability_maps: np.array
        Maprobability_maps of different lobes deposited.
    Centroid_coords: list
        List of centroid coordinates.
    probability_maps: list of np.arrays.
        Probability map for finding new centroid. Topographic highs have low 
        probabilities and topographic lows have high probabilities. 
    stack_list: list
        List with Markov-states
    angle_list: list
        A list indicating the angles towards which the lobes are tilted, 
        relative to the source.
    column_corner_list: list
        A list containing coordinates that specify the location of the 
        upper-right column of a single lobe in the sandbox.
    row_corner_list: list
        A list containing coordinates that specify the location of the 
        upper-right row of a single lobe in the sandbox.
    lobe_geometry.lobe_thickness: np.array
        An array containing the thickness at each specific x and y coordinate
        of a lobe element, with the maximum width, length, and height specified in the input.
    """
    
    # Calculate lobe array with drop geometry
    lobe_geometry = LobeGeometry(width=width,length=lenght, tmax=tmax, cell_size=cell_size)

    # Set initial bathymetry
    bathymetry = BathymetryLayers(nx, ny)

    n=0 

    #Create list with centroids
    centroid_coords = []

    #create list with probability maps
    
    probability_maps = []

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
            
            
            column_corner_list.append(col_corn)
            row_corner_list.append(row_corn)
        
        else: 
           # select stacking angles depending on current state
           current_state = stack_list[n] # according to Markov Chain
           
           if current_state == "NMA":
           
               # Select new source Location - centroid 
               elevation = bathymetry.get_elevation(n)
               probability_map  = 1 - elevation
               prob_sum_one = probability_sum_one(probability_map)
              

               # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
               index = np.random.choice(elevation.size, p=prob_sum_one.flatten())
               # Convert the flattened index to a row and column index
               a, b = divmod(index, elevation.shape[1])
               lobe_location = [a, b] #location of the centroid a = column , b = row
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
               centroid_coords.append([]),probability_maps.append([]),column_corner_list.append([]),row_corner_list.append([]),angle_list.append([])
               
               # update bathymetry
               bathymetry.add_layer(Bathymetry_)
               
               
           else:
               # Angles where new centroid should go
               angle1 = quadrant_angles[current_state][0]
               angle2 = quadrant_angles[current_state][1]
               
               #centroid coords
               if len(centroid_coords[n-1]) == 0: #this will happen when the last event was HF
                    #Find centroid to move the lobe
                   stack_list_segment = stack_list[0:n] #list with states before the present state
                   HF_counts= HF_counter(stack_list_segment)
                   centroid = centroid_coords[n-HF_counts-1]
                   
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
               probability_maps.append(prob_bsm)
           
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
               
        

        Bathymetry_steprobability_maps = bathymetry.layers.copy()
        
        n = n+1 
        print(n) #track progress
        
        # prepare output
        output = (
            Bathymetry_steprobability_maps,
            centroid_coords,
            probability_maps,
            stack_list,
            angle_list,
            column_corner_list,
            row_corner_list,
            lobe_geometry.lobe_thickness
        )
    return output 





    
