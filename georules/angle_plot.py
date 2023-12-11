# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:20:09 2023

@author: nc25884
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA

from utils import load_array

#input
n_test = 1
grid_center = np.array([Value_7_nx[0]/2, Value_8_ny[0]/2])

##functions
def angle_between(center_arc, start_pointarc, end_pointard):
    
    """Calculate angle between two vectors in counterclockwise direction (ccw) .
       
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




for n in range(n_test): 

    centroids =  load_array("centroids{}".format(n),"centroids")     
        

#Remove rows containing "nan" values
# Find rows that do not contain NaN values
valid_rows = ~np.isnan(centroids).any(axis=1)

# Use boolean indexing to select rows without NaN
centroids = centroids[valid_rows]

# Find the angle between three points - the reference point is grid center
# Find the angles at which centroids move.
angles = []
 
for i in range(len(centroids)-1):
    a = centroids[i]
    b = centroids[i+1]
    
    angles.append(angle_between(grid_center,a, b))
    
    
theta = np.linspace(0,360,21)
print(theta)    
    



import numpy as np

# Your lists of angles
list1 = [1, 34, 78, 94, 21, 89, 267, 350]
list2 = [[0, 10], [10, 20], [20, 30], [350, 360]]  # Add more intervals as needed

# Convert lists to numpy arrays for easier manipulation
angles_array = np.array(list1)
intervals_array = np.array(list2)

# Initialize a dictionary to store the count of angles in each interval
angle_counts = {}

# Iterate through each interval in list2
for interval in intervals_array:
    # Filter angles within the current interval
    filtered_angles = angles_array[(angles_array >= interval[0]) & (angles_array < interval[1])]
    
    # Count the number of angles in the interval
    count = len(filtered_angles)
    
    # Store the count in the dictionary
    angle_counts[tuple(interval)] = count

# Print the results
for interval, count in angle_counts.items():
    print(f"Interval {interval}: {count} angles")

    
    
# x = centroids[:15,0]
# y = centroids[:15,1]
# fig,ax = plt.subplots()
# ax.scatter(x,y)

# for i in range(0,36):
#     ax.annotate(i,(x[i],y[i]))



    
    
    

