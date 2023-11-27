#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 17:19:51 2023

@author: Nataly Chacon-Buitrago
Function to include the properties (lithology, net to gross, permeability  etc of the lobe element)
Lobe is divided in 3 sections: Inner lobe (axis), medial lobel (off-axis) and outer lobe (lobe) see Stammer (2014) for more details
    
"""

from S_Lobegeom import drop_geometry
import numpy as np
from S_PasteArray import paste
from S_nonzero_one import convert_nonzero_to_one



### IMPORTANTE: asegurate que esta parte del codigo vaya despues de lobe_thickness!!!!
### IMPORTANTE: FALTA PARTE PARA REEMPLAZAR PROPIEDADES POR LOS NUMEROS, EN ESTE MOMENTO SOLO ESTA NUMERADO DE 1 A 3,
### ESTO DEBE SER CAMBIADO SEGUN LA PROPIEDAD
## IMPORTANTE:FALTA PONERLE UN VERTICAL TREND!!!!!
### IMPORTANTE:MUD NO ESTA FUNCIONANDO BIEN!!!

#Example inputs

# lobe_wmax = 16000
# lobe_length = 30000
# lobe_tmax = 2
# off_axis_wmax = 12000
# off_axis_lenght = 25000
# axis_wmax = 8000
# axis_lenght = 20000
# lobe_x=  [i for i in range(0,lobe_length,100)]
# off_axis_x = [i for i in range(0,off_axis_lenght,100)]
# axis_x = [i for i in range(0,axis_lenght,100)]
# y_interval = 100
# a1 = 0.66
# a2 = 0.33
# cell_size = 100
# lobe_thickness =  np.load("lobe_thickness.npy") 



def lobe_properties(a1,a2,lobe_wmax,lobe_length, lobe_tmax,lobe_x, y_interval,lobe_thickness,cell_size,
                    off_axis_wmax,off_axis_lenght,axis_wmax,axis_lenght):

    
    #Lobe off-axis dimensiions
    off_axis_x = [i for i in range(0,off_axis_lenght, cell_size)]
    
    #Lobe axis dimensiions
    axis_x = [i for i in range(0,axis_lenght, cell_size)]
    
    
    off_axis_geom=  drop_geometry(off_axis_wmax,off_axis_lenght,1, off_axis_x,y_interval,a1,a2) #the maximum thickness doesn't matter as we want only the shape of the lobe
    axis_geom =  drop_geometry(axis_wmax,axis_lenght,1, axis_x,y_interval,a1,a2) #the maximum thickness doesn't matter as we want only the shape of the lobe


    #Create an array of zeros of lobe_thickness size
    n1 = int(lobe_wmax/y_interval)
    n2 = int(lobe_length/y_interval)
    frame_array = np.zeros([n1,n2])

    #Paste lobe_array and off_axis_geom 
    coor1 = int((lobe_wmax - off_axis_wmax)/(y_interval*2))
    off_axis_geom = paste(frame_array.copy(),off_axis_geom.copy(),(coor1,0))

    #Paste lobe_array and axis_geom
    coor2 = int((lobe_wmax - axis_wmax)/(y_interval*2))
    axis_geom = paste(frame_array.copy(),axis_geom.copy(),(coor2,0))

    # lobe_axis
    axis =  convert_nonzero_to_one(axis_geom)

    # lobe_off_axis
    off_axis = convert_nonzero_to_one(off_axis_geom)

    # lobe_margin
    margin = convert_nonzero_to_one(lobe_thickness)

    ####add arrays -> find lithology division

    lobe_properties = axis + off_axis + margin
    
    return(lobe_properties)