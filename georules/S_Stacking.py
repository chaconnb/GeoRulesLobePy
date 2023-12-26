# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 11:16:23 2023

@author: Nataly Chacon-Buitrag
                                                                                                                 
Function to stack n+1 lobe depending on the position of lobe n.                                                  0/360
Input:                                                                                                            |
angle_move1 and angle_move_2 : give the range of movement of the lobe whith respect to those two angles. 90 ----- | ----- 270
                              The range of movement will go from angle_move1 to angle_move2                       |
                                                                                                                 180
search_radius : the proportion to multiply the current lobe radius to find how much the n+1 will move
               radius of movement from centroid= lobe radius + search_proportion*lobe radius                                                                                                               

"""
import numpy as np

def stacking(
        centroid_coords, 
        n,
        lobe_radius,
        search_radius,
        nx,
        ny,
        bathymetry_layer,
        power, 
        angle_move1,
        angle_move2,
    ):
    
    if len(centroid_coords[n-1]) == 0: #this will happen when the last event was HF
         #Find area to move the lobe
        centroid = centroid_coords[n-2]
    else:
        centroid = centroid_coords[n-1]
            
    rad_int = lobe_radius + lobe_radius * 0.00002
     
    #Create the circular mask
    moving_mask = get_moving_mask(nx, ny, angle_move1, angle_move2, centroid, rad_int)
                    
    #Find Probabilities
    elevation_s = (bathymetry_layer - np.min(bathymetry_layer))/(np.max(bathymetry_layer)+0.0001)+0.0001
    prob_s_b = 1-elevation_s
    #prob_s_b is the probability map before  the mask 
    prob_s = prob_s_b.copy() #create deep copy

    #Filter probabilities inside the area of interest

    for i in range(0,nx):
        for j in range(0,ny):
            if moving_mask[i,j] == 0:
                prob_s[i,j]=0 
     
    
    prob_s = np.where(prob_s > 0, prob_s,0)#filter negative probabilities
    prob_sum = np.sum(prob_s) #prob_s has to be positive
    norm_prob_s = prob_s/prob_sum
    index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
    
    # # Convert the flattened index to a row and column index
    a, b = divmod(index, elevation_s.shape[1])
    if moving_mask[a,b] != 1.0: 
        raise ValueError('Lobe coordinates are not in the correct quadrant.')

    lobe_location = [a,b] #location of the centroid
    
    
    return(lobe_location, prob_s, prob_s_b)

def get_moving_mask(nx, ny, angle_move1, angle_move2, centroid, rad_int):
    
    circle_mask = get_circle_mask(nx, ny, centroid, rad_int)
    #find angles from the centroid
    centroid_angles = get_centroid_angles(nx, ny, centroid) #make 360 degrees equal to zero
        
    #angle mask
    #1 if it is inside angle_move1 and angle_move2:
    prob_mask = get_prob_mask(nx, ny, angle_move1, angle_move2, centroid_angles)
                        
    # # overlap circle mask  ang angle mask
    result = get_overlap(nx, ny, circle_mask, prob_mask)
    return result

def get_overlap(nx, ny, circle_mask, prob_mask):
    mask = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
            if prob_mask[i][j] ==circle_mask[i][j] and prob_mask[i][j] == 1 and circle_mask[i][j] == 1:
                mask[i][j] = 1
    return mask

def get_prob_mask(nx, ny, angle_move1, angle_move2, centroid_angles):
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

def get_centroid_angles(nx, ny, centroid):
    angle_rad = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
                angle_rad[i,j]= np.arctan2((i-centroid[1]),(j-centroid[0])) #find the angle from the centroid -radians-
                
    angle_deg = np.rad2deg(angle_rad) #Find the angle from the centroid -degrees-
    angle_deg = angle_deg + 180 # Find the angle from  the centroid from 0 - 360
    angle_deg[angle_deg == 360] = 0
    return angle_deg

def get_circle_mask(nx, ny, centroid, rad_int):
    mask = np.zeros((nx,ny))

    for i in range(0,nx):
        for j in range(0,ny):
            dis_centroid = (j - centroid[0])**2 + (i-centroid[1])**2# distance from the point(x,y) to the centroid
                 
            if dis_centroid< rad_int**2:
                mask[i,j]= 1
    return mask
    
            
                