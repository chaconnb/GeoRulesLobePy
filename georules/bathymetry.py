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
