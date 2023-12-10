# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:47:40 2023

@author:Nataly Chacon-Buitrago

Plot probability maps 
"""
import matplotlib.pyplot as plt 

#print bathymetry maps

for i in range (0,10):
  
    fig = plt.figure()
    
    ax = fig.add_subplot(111)

    ax.set_title(i)

    plt.imshow(Bathymetry_maps[i])
    plt.colorbar()

    plt.show()



# for i in range(10,0,-1):
    
#     fig = plt.figure()
      
#     ax = fig.add_subplot(111)
#     l = i-1
    
#     ax.set_title( str(i) + "-" + str(l))
    
#     plt.imshow(Bathymetry_maps[i]-Bathymetry_maps[i-1])
    
#     plt.colorbar()
    
#     plt.show()



