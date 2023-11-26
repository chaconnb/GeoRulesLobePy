import numpy as np
import math 

from S_Healing import Healing_Factor
from S_RotatePaste import rot_paste
from bathymetry import BathymetryLayers

def lobe_deposition(
        location:list,
        length:float,
        width:float,
        lobe_array:np.ndarray,
        angle:float,
        bathymetry_layers:BathymetryLayers, 
    ):
    """Create a new bathymetry layer after a lobe rotation and 'healing' of the lobe.

    Parameters
    ----------
    location : list
        Centroid location.
    length : float
        Lenght (maximum) of the lobe.
    width : float
        Width (maximum) of the lobe. 
    lobe_array : np.ndarry
        Lobe thickness array. 
    angle : float
        Angle of rotation in degrees of the lobe w.r.t source.
    bathymetry_layers : BathymetryLayers
        Bathymetry layer instance. 
    """
    bathymetry_ini = bathymetry_layers.inital_layer.copy() 
    current_bathymetry = bathymetry_layers.layers[-1]
    n_x = bathymetry_layers.nx
    n_y = bathymetry_layers.ny 
    
    #Embed a small numpy array (lobe_array) into a predifined block of a large numpy array
    result = rot_paste(length, width, lobe_array, angle, location, bathymetry_ini)
    thick_updated, column_corner, row_corner = result 
    
    bathymetry_updated = Healing_Factor(n_x, n_y, thick_updated, current_bathymetry)
    
    return bathymetry_updated, thick_updated, column_corner, row_corner



class LobeGeometry:
    a1 = 0.66
    a2 = 0.33

    def __init__(self, width:float, length:float, tmax:float, cell_size:float) -> None:
        self.width = width 
        self.lenght = length
        self.tmax = tmax
        self.cell_size = cell_size
        self.scaled_width = width/cell_size
        self.scaled_length = length/cell_size

        self.x_coords = [i for i in range(0, length, cell_size)]
        self.lobe_thickness = self.get_lobe_thickness() 

    def get_lobe_thickness(self):
        """Calculate the lobe thickness."""
        w_x_ = self._get_x_width() # width along x-direction
        t_x_ = self._get_x_thickness() # thickness along x-direction
        lobe_thick = self._calc_lobe_thickness_loop(w_x_, t_x_)
        return (lobe_thick)

    def _calc_lobe_thickness_loop(self, w_x_:np.ndarray, t_x_:np.ndarray)-> np.ndarray:
        """Constructing the lobe thickness array."""
        t_y_ = []
        lobe_thick = np.zeros([int(self.width/self.cell_size), len(self.x_coords)])
        
        for i in range(len(self.x_coords)):
            y = [i for i in range(0,int(np.round(2*w_x_[i])),self.cell_size)]
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
                ty = np.zeros(int(self.width/self.cell_size))
                t_y_.append(ty)
            #move all y coordinates to align with the centroid and add zeros
            if len(ty) < self.width/self.cell_size:
                dif = self.width - self.cell_size #subtract to get index starting from zero
                dif = dif - max(y)
                dif = dif/self.cell_size
                
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
        return lobe_thick

    def _get_x_thickness(self) -> np.ndarray:
        """Calculate the thickness in the x-direction."""
        b2 = -np.log(2)/np.log(1-self.a2)
        t_x_ = [4 * self.tmax * (1 -i/self.lenght)**b2 * (1 - (1- i/self.lenght)**b2) for i in self.x_coords] 
        t_x_ = np.array(t_x_)
        return t_x_

    def _get_x_width(self) -> np.ndarray:
        """Calculate the width in the x-direction."""
        b1 = -np.log(2)/np.log(1-self.a1)
        w_x_ = [2 * self.width * (1-i/self.lenght)**b1 * (1 - (1-i/self.lenght)**b1) for i in self.x_coords] 
        w_x_ = np.array(w_x_)
        return w_x_


