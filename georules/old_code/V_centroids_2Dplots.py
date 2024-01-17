# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:53:07 2023

@author: Nataly Chacon-Buitrago

Centroid visualization

"""
import matplotlib.pyplot as plt



y_c = [] 
x_c = []

for i in centoids:
    y_c.append(i[0])
    x_c.append(i[1])
    
    

fig,ax = plt.subplots()
ax.scatter(x_c,y_c)

for i in range(0,20):
    ax.annotate(i,(x_c[i],y_c[i]))
    

# =============================================================================
# Save array
# import numpy as np
# 
# np.save("Bathymetry_maps1",Bathymetry_maps)
#     
#     
# =============================================================================
    

    