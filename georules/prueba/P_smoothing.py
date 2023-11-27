# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:07:18 2023

@author: Nataly Chacon-Buitrago
"""
import matplotlib.pyplot as plt 
import numpy as np
from scipy.ndimage import convolve

# we want to find the new bathymetry

c_bathymetry = Bathymetry_maps[2]

### Let's create a kernel - mean kernel
kernel_size = 17  #number of rows or column of the kernel (recommended an uneven number)
kernel = np.ones((kernel_size,kernel_size), dtype=float) / (kernel_size*kernel_size) 
Bathymetry_new = convolve(c_bathymetry, kernel, mode='constant', cval=0.0)




fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(c_bathymetry)
plt.colorbar()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(Bathymetry_new)
plt.colorbar()
plt.show()