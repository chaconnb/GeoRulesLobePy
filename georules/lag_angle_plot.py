# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:20:09 2023

@author: Nataly Chacon Buitrago

Calculate the lag angle between centroids and plot the angles for all lobes and
realizations in a polar bar plot
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA
from utils import load_array


##functions
def angle_between(center_arc, start_pointarc, end_pointard):
    
    """Calculates angle between two vectors in counterclockwise direction (ccw) .
       
       Parameters
       ----------  
       center_arc: np.ndarray
       Coordinate joining the endpoints of the arc with the center of the circle.  
       start_pointarc: np.ndarray
       Coordinate where the angle will start being measured.
       start_pointarc: np.ndarray
       The coordinate where the angle will cease to be measured.
       
       Returns
       -------
       angle : float 
            

    """
    
    v1 = start_pointarc - center_arc # first vector
    v2 = end_pointard - center_arc  # second vector
    
    # if the cross product is positive, then the two vector need to rotate counter clockwise
    rot = np.cross(v1,v2)
    vdir = 'ccw' if rot >0 else 'cw'

    r = (v1[0]*v2[0]+v1[1]*v2[1])/(LA.norm(v1)*LA.norm(v2))
    
    deg = np.arccos(r)/np.pi*180

    if vdir != 'ccw':
        deg = 360 -deg
    
    return (deg)


#input (change input)
n_test = 300 # number of tests
grid_center = np.array([Value_7_nx[0]/2, Value_8_ny[0]/2]) 


#Data prep
# Find the angles at which centroids move.
angles = []


for n in range(n_test): 

    centroids =  load_array("centroids{}".format(n),"centroids")     
        
    
    #Remove rows containing "nan" values
    # Find rows that do not contain NaN values
    valid_rows = ~np.isnan(centroids).any(axis=1)
    
    # Use boolean indexing to select rows without NaN
    centroids = centroids[valid_rows]
    
    # Find the angle between three points - the reference point is grid center
     
    for i in range(len(centroids)-1):
        a = centroids[i]
        b = centroids[i+1]
        
        angles.append(angle_between(grid_center,a, b))
    
    

# polar bar plot - prep
# 
theta = np.linspace(0,360,36)
# Create pais in the theta using list comprehension
theta_pairlist = [[theta[i], theta[i + 1]] for i in range(0, len(theta), 2)]
    
#Convert lists to numpy arrays for easier manipulation
angles_array = np.array(angles)
intervals_array = np.array(theta_pairlist)

#Initialize a list to store the count of angles in each interval
angle_counts = [] 
 
for interval in intervals_array:
    # Filter angles within the current interval
    filtered_angles = angles_array[(angles_array >= interval[0]) & (angles_array < interval[1])]
    
    # Count the number of angles in the interval
    count = len(filtered_angles)
    
    # Store the count in the list
    angle_counts.append(count)
    
      
#calculate the mean of each pair to be able to plot it 
pairlist_mean = [int(sum(pair) / len(pair)) for pair in theta_pairlist]

#transform the pairlist_mean from degrees to radians
pairlist_mean = np.radians(pairlist_mean)
#transform angle_counts from list to an array
angle_counts = np.array(angle_counts)


#plot polar bar plot

# Get an axes handle/object
ax1 = plt.subplot(projection ="polar")

# Plot
bars = ax1.bar(x = pairlist_mean, height= angle_counts,
        color=plt.cm.viridis(pairlist_mean/ 5.),
        width=0.2,
        bottom=0.0,
        alpha=0.5,
        edgecolor='k')

# Radius limits
#ax1.set_ylim(0,np.max(angle_counts))
# Radius ticks
#ax1.set_yticks(np.linspace(0,np.max(angle_counts),np.max(angle_counts)+1))
# Additional Tweaks
plt.grid(True)
#plt.legend()
#plt.title("Polar Bar Plots")

plt.savefig("lag_angle_plot.png", format="png", dpi=1200)
plt.show()
    









    
    
    

