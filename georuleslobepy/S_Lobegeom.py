# -*- coding: utf-8 -*-
"""

@author: Nataly Chacon-Buitrago
New lobe geometry - output array with coordinates x,y and thickness of the lobe
Equations are taken from Zhang et al. 2009. Equation to find w_x_was modified. 
inputs: 
    wmax = maximum lobe width int
    length = maximum lobe length int
    tmax = maximum thickness int
    x = list with the coordinates we want to calculate thickness in x (lenght parameter)
    y_interval = interval of y
    a1 = Relative position of maximum width.
    a2 = Relative position of maximum thickness.
    Default a1 = 0.66 and a2 = 0.33 -> if this changes  S_RotatePaste has to change, becuase centroid location will change!
    
output:
    lobe_thick = array size (wmax/interval_size_x ) x (lenght/y_interval)
                             
"""

import numpy as np
import math


#Example input: 
# a1 = 0.66
# a2 = 0.33
# wmax = 16000 #m 
# lenght = 30000 #m
# tmax = 2 #m
# x = [i for i in range(0,lenght, 100)]
# y_interval = 100

def  drop_geometry(wmax,lenght,tmax,x,y_interval, a1 =0.66, a2 =0.33):

    
    b1 = -np.log(2)/np.log(1-a1)
    
    
    w_x_ = [ 2 * wmax *(1-i/lenght)**b1 *(1-(1-i/lenght)**b1) for i in x] 
    w_x_ = np.array(w_x_)

    b2 = -np.log(2)/np.log(1-a2)
    t_x_ = [4* tmax *(1 -i/lenght)**b2 *(1 - (1- i/lenght)**b2) for i in x] 
    t_x_ = np.array(t_x_)
    
    
    
    t_y_ = []
    lobe_thick = np.zeros([int(wmax/y_interval), len(x)])
    
    
    for i in range(len(x)):
    
        y = [i for i in range(0,int(np.round(2*w_x_[i])),y_interval)]
    
      
       
        ty = []
        
        if w_x_[i] != 0:
    
            
            for j in  range(len(y)):
                a = 0.5
                b = -np.log(2)/np.log(1-a)
                
                t = 4 * t_x_[i] * (y[j]/(2*w_x_[i]))**b *(1-(y[j]/(2*w_x_[i]))**b)
                ty.append(t)
           
            ty = np.array(ty)
            t_y_.append(ty)
            
        else:
            ty = np.zeros(int(wmax/y_interval))
            t_y_.append(ty)
            
        #move all y coordinates to align with the centroid and add zeros
        
        if len(ty) < wmax/y_interval:
        
            dif = wmax- y_interval #subtract to get index starting from zero
            dif = dif - max(y)
            dif = dif/y_interval
            
            if dif%2 == 0:
                limit = np.zeros(int(dif/2))
                thick = np.concatenate((limit,ty))
                thick = np.concatenate((thick,limit))
                thick = np.array(thick)
                thick = np.transpose(thick)
                lobe_thick[:,i] = thick
                
            else:
                upper_limit = np.zeros(math.floor(dif/2))
                lower_limit = np.zeros(math.ceil(dif/2))
                thick = np.concatenate((upper_limit,ty))
                thick = np.concatenate((thick,lower_limit))
                thick = np.array(thick)
                thick = np.transpose(thick)
                lobe_thick[:,i] = thick
            
                
        else:
                lobe_thick[:,i] = ty
         
    return(lobe_thick)

# =============================================================================
#  Useful plots: 
#     
# #Plot lobe_thick in 2D
# # fig = plt.figure()
# # ax = fig.add_subplot(111)
# # plt.imshow(lobe_thick)
# # plt.show()
# 
# 
# 
# #Plot lobe_thick in 3D
# 
# # generate meshgrid for plot
# # xax = np.arange(0, wmax/y_interval)
# # yax = np.arange(0, lenght/y_interval)
# # xax, yax = np.meshgrid(yax, xax)
# 
# 
# # # plot and save
# # fig = plt.figure()
# # ax = fig.add_subplot(1,1,1, projection ='3d')
# # #ax = fig.gca(projection='3d')
# # surf = ax.plot_surface(xax, yax, lobe_thick, cmap = 'viridis')
# # ax.set_box_aspect([30,15,2])  
# # ax.view_init(25,180)
# # plt.show()
# 
# 
# =============================================================================










