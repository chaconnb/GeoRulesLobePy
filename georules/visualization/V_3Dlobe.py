# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:56:47 2023

@author: Nataly Chacon-Buitrago
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


#Plot in 3D

# nx = Value_7_nx[0]
# ny = Value_8_ny[0]

#X,Y =np.meshgrid(np.linspace(0, nx-1,nx), np.linspace(0,ny-1,ny))


# #
# for i in range(1,10):
    
    
#     fig = plt.figure(figsize=(20,8))
#     ax = fig.add_subplot(1,3,2, projection ='3d')
    
    
#     Z = Bathymetry_maps[i] #Bathymetry can be changed
#     surf = ax.plot_surface(X,Y,Z, cmap = 'viridis')
    
#     ax.pbaspect = [2.0, 0.6, 0.25]

#     ax.set_box_aspect([30,30,8])  
#     ax.set_xlabel(r'$X$', fontsize = 9)
#     ax.set_ylabel(r'$Y$', fontsize = 9)
#     ax.set_zlabel(r'$Z$', fontsize =9)
#     ax.tick_params(labelsize = 9)
#     #ax.view_init(15,270)

# plt.show()


#Plot lobe_thick in 2D

for i in range(len(Bathymetry_maps)):
 
  fig = plt.figure()
  ax = fig.add_subplot(111)
  #plt.scatter(369,36)
  plt.imshow(Bathymetry_maps[i])
  cbar = plt.colorbar()
  cbar.set_label("m")
  plt.show()
  
  
# fig = plt.figure()
# ax = fig.add_subplot(111)
#   #plt.scatter(369,36)
# plt.imshow(Bathymetry_maps[17])
# cbar = plt.colorbar()
# cbar.set_label("m")
# plt.show()

# nx = 400
# ny = 400


# X,Y =np.meshgrid(np.linspace(0, nx-1,nx), np.linspace(0,ny-1,ny))

# fig = plt.figure(figsize=(20,8))
# ax = fig.add_subplot(1,3,2, projection ='3d')
    
    
# Z = real_thick #Bathymetry can be changed
# surf = ax.plot_surface(X,Y,Z, cmap = 'viridis')
    
# ax.pbaspect = [2.0, 0.6, 0.25]

# ax.set_box_aspect([30,30,8])  
# ax.set_xlabel(r'$X$', fontsize = 9)
# ax.set_ylabel(r'$Y$', fontsize = 9)
# ax.set_zlabel(r'$Z$', fontsize =9)
# ax.tick_params(labelsize = 9)
# ax.view_init(25,320)