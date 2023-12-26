"""
Created on Sun Mar 19 11:16:23 2023
@author: Nataly Chacon-Buitrago
"""
from ast import List
from typing import Tuple
import numpy as np

def stacking(
        centroid:list,
        n:int,
        lobe_radius:float,
        nx:int,
        ny:int,
        bathymetry_layer:np.ndarray,
        angle_move1:int,
        angle_move2:int, 
    ) -> Tuple[List[float], np.ndarray]:
    """Function to stack n+1 lobe depending on the position of lobe n. 
       The stacking pattern depends on the state of the markov chain. 
       
    Parameters
    ----------
    centroid: list 
        Centroid's coordiantes, in the format [column,row].
    n : int
        Number of lobe being deposited.
    lobe_radius: float
    nx : int
        Sandbox size in the x direction.
    ny : int
        Sandbox size in the y direction.
    bathymetry_layer: np.array
        Bathymetry layer generated from n-1 markov state.
    angle_move1 and angle_move_2: int    
        Range of movement of the centroid is given by this two angles.
        The range of movement will go from angle_move1 to angle_move2.
    
    Returns
    -------
    lobe_location:list
        Centroid's coordiantes for next lobe.
    centroid_probability_map: np.array 
        Probability map for finding new centroid. Topographic highs have low 
        probabilities and topographic lows have high probabilities. 
    """
    rad_int = lobe_radius + lobe_radius * 0.00002
     
    #Create the circular mask
    moving_mask = get_moving_mask(nx, ny, angle_move1, angle_move2, centroid, rad_int)
                    
    #Find Probabilities
    elevation_s = (bathymetry_layer - np.min(bathymetry_layer))/(np.max(bathymetry_layer)+0.0001)+0.0001
    centroid_probability_map = 1-elevation_s # probability map before the mask 
    norm_prob_s = get_normalized_proobability(nx, ny, moving_mask, centroid_probability_map)
    
    # Convert the flattened index to a column and row index
    index = np.random.choice(norm_prob_s.size, p=norm_prob_s.flatten())
    a,b = divmod(index, norm_prob_s.shape[1])
   
    if moving_mask[a,b] != 1.0: 
        raise ValueError('Lobe coordinates are not in the correct quadrant.')

    lobe_location = [b,a] #location of the centroid, I had to swap the positions of 'a' and 'b' to make it work.
    
    return lobe_location, centroid_probability_map 

def get_normalized_proobability(nx, ny, moving_mask, centroid_probability_map):
    prob_s = centroid_probability_map.copy() 
    for i in range(0, nx):
        for j in range(0, ny):
            if moving_mask[i, j] == 0:
                prob_s[i, j] = 0 
                
    prob_s = np.where(prob_s > 0, prob_s,0) # filter negative probabilities
    norm_prob_s = prob_s/np.sum(prob_s)
    return norm_prob_s

def get_moving_mask(nx, ny, angle_move1, angle_move2, centroid, rad_int):
    
    circle_mask = get_circle_mask(nx, ny, centroid, rad_int)
    #find angles from the centroid
    centroid_angles = get_centroid_angles(nx, ny, centroid) #make 360 degrees equal to zero
        
    #angle mask
    #1 if it is inside angle_move1 and angle_move2:
    angle_mask = get_angle_mask(nx, ny, angle_move1, angle_move2, centroid_angles)
                        
    # # overlap circle mask  ang angle mask
    result = get_overlap_mask(nx, ny, circle_mask, angle_mask)
    return result

def get_circle_mask(nx, ny, centroid, rad_int):
    "Mask from the centroid to the radius (rad_int) in every direction."
    
    mask = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
            dis_centroid = (j - centroid[0])**2 + (i-centroid[1])**2# distance from the point(x,y) to the centroid
                 
            if dis_centroid< rad_int**2:
                mask[i,j]= 1
    return mask

def get_centroid_angles(nx, ny, centroid):
    "Finds the angle in degrees from the centroid to every cell in the grid of size nx * ny."
    
    angle_rad = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
                angle_rad[i,j]= np.arctan2((i-centroid[1]),(j-centroid[0])) #find the angle from the centroid -radians-
                
    angle_deg = np.rad2deg(angle_rad) #Find the angle from the centroid -degrees-
    angle_deg = angle_deg + 180 # Find the angle from  the centroid from 0 - 360
    angle_deg[angle_deg == 360] = 0
    return angle_deg

def get_angle_mask(nx, ny, angle_move1, angle_move2, centroid_angles):
    "Finds mask between the angle1 and angle 2"
    
    mask = np.zeros((nx,ny)) #mask to determine where the lobe is going to move based on the angles

    for i in range(0,nx):
        for j in range(0,ny):
            angle = centroid_angles[i][j]
            if angle_move1 < angle_move2:
                if angle_move1 <= angle <= angle_move2:
                    mask[i][j]=1
            else:
                if 0 <= angle <= angle_move2:
                    mask[i][j]=1
                elif angle_move1 <= angle<= 360:
                    mask[i][j] = 1
    return mask

def get_overlap_mask(nx, ny, circle_mask, angle_mask):
    "Overlaps angle_mask and circle_mask to create a mask between the angles and length from the centroid of interest."
    mask = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
            if angle_mask[i][j] ==circle_mask[i][j] and angle_mask[i][j] == 1 and angle_mask[i][j] == 1:
                mask[i][j] = 1
    return mask
                            