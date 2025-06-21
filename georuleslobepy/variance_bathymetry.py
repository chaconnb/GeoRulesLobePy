import numpy as np

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
    
    for arr in Bathymetry_maps:
        
        # calculate mean
        mean_array = np.mean(arr)
        # calculate squared differences
        squared_diff = (arr - mean_array)**2
        #calculate variance
        variance_array = np.mean(squared_diff)
        #append variance to the bathymetry map
        variance_bathymetry.append(variance_array)
        
    # Convert the list to a NumPy array
    
    return(np.array(variance_bathymetry)) 