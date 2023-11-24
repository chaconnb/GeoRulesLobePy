# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:07:18 2023

@author: Nataly Chacon-Buitrago
"""
from S_RotatePaste import rot_paste
from S_Lobegeom import drop_geometry
import matplotlib.pyplot as plt 
import numpy as np
# we want to find the new bathymetry

n = 1
wmax = 15000 
lenght = 30000
cell_size = 100
a1 = 0.66
a2 = 0.33
tmax = Value_3_tmax[0] 
x = [i for i in range(0,lenght, cell_size)]
y_interval = cell_size
lenghtn = lenght/cell_size 
wmaxn = wmax/cell_size
bathymetry_post = Bathymetry_maps[n]
Location = centoids[n]
bathymetry_ini = np.zeros((250,250))
angle = angle_stack[n]
lobearr = drop_geometry(wmax,lenght,tmax,x,y_interval,a1,a2)





thick_updated, column_corner, row_corner = rot_paste(lenghtn,wmaxn,lobearr,angle,Location,bathymetry_ini)



fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(thick_updated)
plt.show()