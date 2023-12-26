# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 09:20:45 2023

@author: nc25884
"""
import numpy as np

#Location_, prob_s, prob_bsm = stacking(ls, n, lobe_geometry.scaled_width, 0.2, nx, ny, bathymetry.layers[-1], power,angle1, angle2)
#def stacking(centroid_list, n, Loberadius, search_radius,n_x,n_y, Bathymetry_,power, angle_move1, angle_move2):
    
##INPUTS
centroid_list =  centoids
n = 2
Loberadius = 150
search_radius = 0.2
n_x = 250
n_y = 250
Bathymetry_ = Bathymetry_maps[n]
power = 5
current_state = quadrants[n]
#current_state = "Q2"
angle_move1 = quadrant_angles[current_state][0]
angle_move2 = quadrant_angles[current_state][1]


########################## NEW
    
if len(centroid_list[n-1]) == 0: #this will happen when the last event was HF
     #Find area to move the lobe
    centroid = centroid_list[n-2]
else:
    centroid = centroid_list[n-1]
        
rad_int = Loberadius + Loberadius*0.00002
 
#Create the circular mask

circular_mask1= np.zeros((n_x,n_y))

for i in range(0,n_x):
    for j in range(0,n_y):
        dis_centroid = (j - centroid[0])**2 + (i-centroid[1])**2# distance from the point(x,y) to the centroid
             
        if dis_centroid< rad_int**2:
            circular_mask1[i,j]= 1
                
#find angles from the centroid
     
ang_rad2 = np.zeros((n_x,n_y))

for i in range(0,n_x):
    for j in range(0,n_y):
            ang_rad2[i,j]= np.arctan2((i-centroid[1]),(j-centroid[0])) #find the angle from the centroid -radians-
            
ang_degrees2 = np.rad2deg(ang_rad2) #Find the angle from the centroid -degrees-
ang_degrees2 = ang_degrees2 + 180 # Find the angle from  the centroid from 0 - 360
ang_degrees2[ang_degrees2 == 360] = 0 #make 360 degrees equal to zero
    
#angle mask
                
#1 if it is inside angle_move1 and angle_move2:
ang_mask1 = np.zeros((n_x,n_y)) #mask to determine where the lobe is going to move based on the angles

for i in range(0,n_x):
    for j in range(0,n_y):
        angle = ang_degrees2[i][j]
        if angle_move1 < angle_move2:
            if angle_move1 <= angle <= angle_move2:
                ang_mask1[i][j]=1
        else:
            if 0 <= angle <= angle_move2:
                ang_mask1[i][j]=1
            elif angle_move1 <= angle<= 360:
                ang_mask1[i][j] = 1
                    
# # overlap circle mask  ang angle mask
moving_mask1 = np.zeros((n_x,n_y))

for i in range(0,n_x):
    for j in range(0,n_y):
        if ang_mask1[i][j] ==circular_mask1[i][j] and ang_mask1[i][j] == 1 and circular_mask1[i][j] == 1:
            moving_mask1[i][j] = 1
                
#Find Probabilities
elevation_s = (Bathymetry_ - np.min(Bathymetry_))/(np.max(Bathymetry_)+0.0001)+0.0001
prob_s_b = 1-elevation_s
#prob_s_b is the probability map before  the mask 
prob_s1 = prob_s_b.copy() #create deep copy

#Filter probabilities inside the area of interest

for i in range(0,n_x):
    for j in range(0,n_y):
        if moving_mask1[i,j] == 0:
            prob_s1[i,j]=0 
   
#prob_sum1 = np.sum(prob_s1) #prob_s has to be positive
# norm_prob_s = prob_s/prob_sum
# # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
# #np.random.seed(351023)
#index = np.argmax(norm_prob_s.flatten())


#filter negative probabilities
prob_s1 = np.where(prob_s1 > 0, prob_s1,0)
prob_sum1 = np.sum(prob_s1) #prob_s has to be positive
norm_prob_s1 = prob_s1/prob_sum1
index = np.random.choice(elevation_s.size, p=norm_prob_s1.flatten())
# # Convert the flattened index to a row and column index
a, b = divmod(index, elevation_s.shape[1])
Location1_ = [a,b] #location of the centroid
    
fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(circular_mask1)
plt.title("NEW")
plt.scatter(centroid[0],centroid[1])
plt.colorbar()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(ang_degrees2)
plt.title("ang_degrees new")
plt.scatter(centroid[0],centroid[1])
plt.colorbar()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(ang_mask1)
plt.title("ang_mask new")
plt.scatter(centroid[0],centroid[1])
plt.colorbar()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(prob_s_b)
plt.title("prob_sb")
plt.scatter(centroid[0],centroid[1])
plt.colorbar()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(prob_s1)
plt.title("prob_s1")
plt.scatter(centroid[0],centroid[1])
plt.scatter(102,244)
plt.scatter(b,a)
plt.colorbar()
plt.show()

########################## OLD
    
# if len(centroid_list[n-1]) == 0: #this will happen when the last event was HF
#      #Find area to move the lobe
#     centroid = centroid_list[n-2]
# else:
#     centroid = centroid_list[n-1]
        
# rad_int = Loberadius + Loberadius*search_radius
 
# #Create the circular mask

# circular_mask= np.zeros((n_x,n_y))

# for i in range(0,n_x):
#     for j in range(0,n_y):
#         dis_centroid = (j - centroid[1])**2 + (i-centroid[0])**2# distance from the point(x,y) to the centroid
             
#         if dis_centroid< rad_int**2:
#             circular_mask[i,j]= 1
            

     
# ang_rad2 = np.zeros((n_x,n_y))

# for i in range(0,n_x):
#     for j in range(0,n_y):
#             ang_rad2[i,j]= np.arctan2((i-centroid[0]),(j-centroid[1])) #find the angle from the centroid -radians-

# ang_degrees2 = np.rad2deg(ang_rad2) #Find the angle from the centroid -degrees-
# ang_degrees2 = ang_degrees2 + 180 # Find the angle from  the centroid from 0 - 360
# ang_degrees2[ang_degrees2 == 360] = 0 #make 360 degrees equal to zero
    

# #angle mask
                
# # 1 if it is inside angle_move1 and angle_move2:
# ang_mask = np.zeros((n_x,n_y)) #mask to determine where the lobe is going to move based on the angles

# for i in range(0,n_x):
#     for j in range(0,n_y):
#         angle = ang_degrees2[i][j]
#         if angle_move1 < angle_move2:
#             if angle_move1 <= angle <= angle_move2:
#                 ang_mask[i][j]=1
#         else:
#             if 0 <= angle <= angle_move2:
#                 ang_mask[i][j]=1
#             elif angle_move1 <= angle<= 360:
#                 ang_mask[i][j] = 1


# # # overlap circle mask  ang angle mask
# moving_mask = np.zeros((n_x,n_y))

# for i in range(0,n_x):
#     for j in range(0,n_y):
#         if ang_mask[i][j] ==circular_mask[i][j] and ang_mask[i][j] == 1 and circular_mask[i][j] == 1:
#             moving_mask[i][j] = 1
            
# #Find Probabilities
# elevation_s = (Bathymetry_ - np.min(Bathymetry_))/(np.max(Bathymetry_)+0.0001)+0.0001
# prob_s_b = (1/np.transpose(elevation_s))**power
# #prob_s_b is the probability map before  the mask 
# prob_s = prob_s_b.copy() #create deep copy

# #Filter probabilities inside the area of interest

# for i in range(0,n_x):
#     for j in range(0,n_y):
#         if moving_mask[i,j] == 0:
#             prob_s[i,j]=0 
   

# prob_sum = np.sum(prob_s) #prob_s has to be positive
# norm_prob_s = prob_s/prob_sum
# # Use numpy.random.choice to select a flattened index - the centroid- with the specified weights
# #np.random.seed(351023)
# #index = np.argmax(norm_prob_s.flatten())
# index = np.random.choice(elevation_s.size, p=norm_prob_s.flatten())
# # Convert the flattened index to a row and column index
# a, b = divmod(index, elevation_s.shape[1])
# Location_ = [a,b] #location of the centroid


# fig = plt.figure() 
# ax = fig.add_subplot(111)
# plt.imshow(circular_mask)
# plt.title("OLD")
# plt.scatter(centroid[1],centroid[0])
# plt.colorbar()
# plt.show()

# fig = plt.figure() 
# ax = fig.add_subplot(111)
# plt.imshow(ang_degrees2)
# plt.title("OLD ANG degree")
# plt.scatter(centroid[1],centroid[0])
# plt.colorbar()
# plt.show()

# fig = plt.figure() 
# ax = fig.add_subplot(111)
# plt.imshow(ang_mask)
# plt.title("OLD ANG mask")
# plt.scatter(centroid[1],centroid[0])
# #plt.scatter(11,65)
# plt.colorbar()
# plt.show()


# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.imshow(prob_s_b)
# plt.title("prob_s_b")
# plt.scatter(centroid[1],centroid[0])
# plt.scatter(b,a)
# plt.colorbar()
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.imshow(norm_prob_s)
# plt.title("norm_prob_s ")
# plt.colorbar()
# plt.show()