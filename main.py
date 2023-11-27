"""
Created on Tue Apr 25 14:50:19 2023

@author: Nataly Chacon-Buitrago
"""
import numpy as np
import math 

from georules.S_ProbMap import Lobe_map
from georules.S_3Dgrid import sandbox
from georules.visualization.V_grid import grid

## Reservoir Parameter Setting
POWER = 5
WIDTH = 15000 #m
TMAX = 2 #m
LENGTH = 30000 #m 
N_LOBES = 10 #number of lobes
CELL_SIZE = 100 #cell size
NX = 250
NY = 250
TRANSITION_MATRIX = [[0.4,0.05,0.4,0.05,0.05,0.05],
                     [0.3,0.05,0.25,0.2,0.1,0.1],
                     [0.3,0.1,0.3,0.14,0.08,0.08],
                     [0.3,0.05,0.3,0.25,0.05,0.05],
                     [0.2,0.15,0.2,0.4,0.025,0.025],
                     [0.21,0.13,0.13,0.13,0.28,0.12]] #transition matrix
START_STATE = "Q2" # start states can be ["Q1","Q2","Q3","Q4","NMA","HF"]
QUAD_ANGLES = {"Q1": [315,45],"Q2":[45,135],"Q3":[135,225],"Q4":[225,315]} #lists of quadrants with their angles
SEDIMENT_SOURCE = [25,200] #source of the sediment (channel)
A1 = 0.66
A2  = 0.33
GP = 0.15
CELL_SIZE_Z = 0.05
N_MUD_CELLS = 2 #number of cells mud that covers lobe
MUD_PROPERTY = 0.18 #property mud

# NOTE: @nataly - for the variables above, you should think about which are "user inputs"
# and which are just "constants" that you don't want to expose to the user, at least at 
# a high-level. Then you should separate the variables into "user inputs" and internal 
# "constants".

def get_lobe_map():
    """Get the lob map.""" # NOTE: Better docstring needed here.
    result = Lobe_map(
        NX,
        NY,
        CELL_SIZE,
        WIDTH,
        LENGTH,
        TMAX,
        N_LOBES,
        POWER,
        TRANSITION_MATRIX,
        START_STATE,
        QUAD_ANGLES,
        SEDIMENT_SOURCE,
        CELL_SIZE_Z,
        N_MUD_CELLS
    )

    return result 
    
def create_3d_grid(lobe_map_results):
    """Create a 3D grid based on the lobe mapping."""
    (
        Bathymetry_maps,
        centoids,
        prob_maps,
        quadrants,
        angle_stack,
        columns_corner,
        rows_corner,
        lobe_image
    ) = lobe_map_results

    nz = math.ceil(np.max(Bathymetry_maps[len(Bathymetry_maps)-1])) #Find maximum height 
    sandbox_grid = sandbox(
        LENGTH,WIDTH,
        CELL_SIZE,
        lobe_image,
        CELL_SIZE_Z,
        TMAX,
        GP,
        MUD_PROPERTY,
        N_MUD_CELLS,
        A1,
        A2,
        NX,
        NY,
        nz,
        N_LOBES,
        angle_stack,
        columns_corner,
        rows_corner,
        Bathymetry_maps,
        quadrants
    )
    return sandbox_grid

def visualize(sandbox_grid):
    """Visualize the sandbox.""" 
    grid(
        sandbox_grid,
        1,
        1,
        1,
        plot_slices=True,
        slice_x=40,
        slice_y=30,
        slice_z=2
    ) #change depending on desired type of visualization 

def main():
    """Run GeoRules simulation."""
    res = get_lobe_map()
    sandbox_grid = create_3d_grid(res)
    visualize(sandbox_grid)

if __name__ == '__main__':
    print("\n###### Starting GeoRules! ######")
    main()
