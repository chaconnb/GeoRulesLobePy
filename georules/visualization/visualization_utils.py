import numpy as np 
from numpy import linalg as LA

def angle_between(center_arc, start_pointarc, end_pointard):

    """Calculates angle between two vectors in clockwise direction (cw) .
       
        Parameters
        ----------  
        center_arc: np.ndarray[row,column]
        Coordinate joining the endpoints of the arc with the center of the circle.  
        start_pointarc: np.ndarray[row,column]
        Coordinate where the angle will start being measured.
        start_pointarc: np.ndarray[row,column]
        The coordinate where the angle will cease to be measured.
       
        Returns
        -------
        angle : float 
            
    """

    v1 = start_pointarc - center_arc # first vector
    v2 = end_pointard - center_arc  # second vector

    # if the cross product is positive, then the two vector need to rotate counter clockwise
    rot = np.cross(v1,v2)
    vdir = 'ccw' if rot >0 else 'cw'

    r = (v1[0]*v2[0]+v1[1]*v2[1])/(LA.norm(v1)*LA.norm(v2))

    deg = np.arccos(r)/np.pi*180

    if vdir != 'cw':
        deg = 360 -deg

    return (deg)


def lobe_max_thickness(bathymetry_map_n_1, bathymetry_map_n):

    """Calculates maximum thickness for new lobe in bathymetry_map_n.
       
       Parameters
       ----------  
       bathymetry_map_n_1 : np.ndarray
       Bathymetry map generated for n-1 lobe.  
       bathymetry_map_n: np.ndarray
       Bathymetry map generated for n lobe.
       
       Returns
       -------
       max_thickness : max thickness for n+1 lobe. 
            
    """

    bathy_thickness_difference = bathymetry_map_n - bathymetry_map_n_1 
    max_thickness = np.max(bathy_thickness_difference)

    return(max_thickness)