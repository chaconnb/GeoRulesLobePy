import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class BathymetryLayers: 

    def __init__(self, nx:int, ny:int) -> None:

        self.nx = nx 
        self.ny = ny        
        self.layers = [np.zeros((nx,ny))] # create initial layer

    @property
    def inital_layer(self): 
        return self.layers[0]
    
    def add_layer(self, layer):
        self.layers.append(layer)

    def get_elevation(self, idx:int): 
        layer = self.layers[idx]
        elevation = (layer - np.min(layer))/(np.max(layer) + 0.0001) + 0.0001
        return elevation  
    
    def _plot_layer(self, filename:str, idx:int, save:bool=True): 
        fig, ax = plt.subplots()
        ax.set_title(f"layer-{idx}") 
        ax.imshow(self.layers[idx])
        return fig, ax

def varinace_bathymetry_maps(Bathymetry_maps):
    """Calculate Variance of thicknesses in bathymetry maps
       
       Parameters
       ----------  
       Bathymetry_maps : List
       Bathymetry layer instance.
       
       Returns
       -------
       variance_bathymetry: arrays
       array with the variance of the thicknesses of each bathymetry map. 
            

    """ 


    variance_bathymetry = []
    
    for _map in Bathymetry_maps:
        
        # calculate mean
        mean_array = np.mean(_map)
        # calculate squared differences
        squared_diff = (_map - mean_array)**2
        #calculate variance
        variance_array = np.mean(squared_diff)
        #append variance to the bathymetry map
        variance_bathymetry.append(variance_array)
        
    # Convert the list to a NumPy array
    
    return(np.array(variance_bathymetry))