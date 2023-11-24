"""
Created on Thu Mar 30 12:20:13 2023

@author: Nataly Chacon-Buitrago
Lobe deposition and healing factor


"""

from S_Healing import Healing_Factor
from S_RotatePaste import rot_paste




def LobeDepos(Location, lenghtn, wmaxn, lobearr, bathymetry_ini,bathymetry,n_x,n_y,angle):
    
    #Embed a small numpy array (lobearr) into a predifined block of a large numpy array
    thick_updated, column_corner, row_corner = rot_paste(lenghtn,wmaxn,lobearr,angle,Location,bathymetry_ini)
    
    bathymetry_updated = Healing_Factor(n_x, n_y,thick_updated,bathymetry)
    
    return(bathymetry_updated,thick_updated, column_corner, row_corner) 




