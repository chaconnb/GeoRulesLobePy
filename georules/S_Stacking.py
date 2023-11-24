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

def stacking(centroid_list, n, Loberadius, search_radius,n_x,n_y, Bathymetry_,power, angle_move1, angle_move2):
    
    
    if len(centroid_list[n-1]) == 0: #this will happen when the last event was HF
        #Find area to move the lobe
        centroid = centroid_list[n-2]
    else:
        centroid = centroid_list[n-1]
        
    rad_int = Loberadius + Loberadius*search_radius
 
    #Create the circular mask

    circular_mask= np.zeros((n_x,n_y))

    for i in range(0,n_x):
        for j in range(0,n_y):
             
            dis_centroid = (j - centroid[1])**2 + (i-centroid[0])**2# distance from the point(x,y) to the centroid
             
            if dis_centroid< rad_int**2:
                circular_mask[i,j]= 1
                
    #find angles from the centroid
     
    ang_rad2 = np.zeros((n_x,n_y))

    for i in range(0,n_x):
        for j in range(0,n_y):
            
               ang_rad2[i,j]= np.arctan2((i-centroid[0]),(j-centroid[1])) #find the angle from the centroid -radians-
            
    ang_degrees2 = np.rad2deg(ang_rad2) #Find the angle from the centroid -degrees-
    ang_degrees2 = ang_degrees2 + 180 # Find the angle from  the centroid from 0 - 360
    ang_degrees2[ang_degrees2 == 360] = 0 #make 360 degrees equal to zero
    
    #angle mask
                
    # 1 if it is inside angle_move1 and angle_move2:
    ang_mask = np.zeros((n_x,n_y)) #mask to determine where the lobe is going to move based on the angles

    for i in range(0,n_x):
        for j in range(0,n_y):
            
            angle = ang_degrees2[i][j]
            
            if angle_move1 < angle_move2:
                if angle_move1 <= angle <= angle_move2:
                    ang_mask[i][j]=1
            else:
                if 0 <= angle <= angle_move2:
                    ang_mask[i][j]=1
                elif angle_move1 <= angle<= 360:
                    ang_mask[i][j] = 1
                    
    # overlap circle mask  ang angle mask

    moving_mask = np.zeros((n_x,n_y))


    for i in range(0,n_x):
        for j in range(0,n_y):
            
            if ang_mask[i][j] ==circular_mask[i][j] and ang_mask[i][j] == 1 and circular_mask[i][j] == 1:
                moving_mask[i][j] = 1
                
    #Find Probabilities
    elevation_s = (Bathymetry_ - np.min(Bathymetry_))/(np.max(Bathymetry_)+0.0001)+0.0001
    prob_s_b = (1/np.transpose(elevation_s))**power ## compensational power  ###Sera necesario tenerlo que trasponer???\
    #prob_s_b is the probability map before  the mask 
    prob_s = prob_s_b.copy() #create deep copy

     #Filter probabilities inside the area of interest

    for i in range(0,n_x):
        for j in range(0,n_y):
            if moving_mask[i,j] == 0:
                prob_s[i,j]=0 
   
    prob_sum = np.sum(prob_s) #prob_s has to be positive
    norm_prob_s = prob_s/prob_sum
    # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
    #np.random.seed(351023)
    index = np.argmax(norm_prob_s.flatten())
    #index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
    # Convert the flattened index to a row and column index
    a, b = divmod(index, elevation_s.shape[1])

    Location_ = [a,b] #location of the centroid
    
    return(Location_, prob_s, prob_s_b)
    
            
                