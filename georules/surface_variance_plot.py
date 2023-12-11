# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:50:46 2023

@author: Nataly Chacon-Buitrago 
This code plots the number of lobes on the x-axis and the surface variance on the y-axis.
The surface variance is loaded from the data obtained during the test,
and P10, P25, P50, P85, and P90 are calculated and plotted.
"""

import matplotlib.pyplot as plt
from utils import load_array
import numpy as np



#input
n_lobes = 40
n_test = 300

#create array of zeros to store the variances of the bathymetry maps
#Add four columns to the array to accommodate space for p10, p25, p85, and p90 values for each row.
#Add one row, as there are n_lobes + 1 bathymetry maps, with the first one being just an array of zeros.
array_variances_percentiles = np.zeros((n_lobes+1,n_test+5))


for n in range(n_test): 

    variance_bathymetry =  load_array("variance_thickness{}".format(n),"surface_variance")
    array_variances_percentiles[:,n] = variance_bathymetry
    
    
#Find P10, P25, P85 and P90

for n in range(n_lobes+1):
    #p10
    array_variances_percentiles[n,n_test] = np.percentile(array_variances_percentiles[n,:n_test],10)
    #p25
    array_variances_percentiles[n,n_test+1] = np.percentile(array_variances_percentiles[n,:n_test],25)
    #p50
    array_variances_percentiles[n,n_test+2] = np.percentile(array_variances_percentiles[n,:n_test],50)
    #p85
    array_variances_percentiles[n,n_test+3] = np.percentile(array_variances_percentiles[n,:n_test],85)
    #p90
    array_variances_percentiles[n,n_test+4] = np.percentile(array_variances_percentiles[n,:n_test],90)
    

# #### plot variance vs surface and percentiles

bathy_lenght = list(range(0,n_lobes+1))

for n in range(n_test):
    
    # # set the title of a plot 
    #plt.title("Surface Variance")

    # # plot scatter plot with x and y data 
    plt.plot(bathy_lenght,array_variances_percentiles[:,n],alpha=0.2) 
    
 
#plt.plot(bathy_lenght,array_variances_percentiles[:,300],"k--") #p10 
plt.plot(bathy_lenght,array_variances_percentiles[:,n_test+1],"b--", label = 'P25') #p25
plt.plot(bathy_lenght,array_variances_percentiles[:,n_test+2],"k", label = 'P50') #p50
plt.plot(bathy_lenght,array_variances_percentiles[:,n_test+3],"r--", label = 'P85') #p85 
#plt.plot(bathy_lenght,array_variances_percentiles[:,304],"k--") #p90
 
   
plt.xlim([0, 40]) 
plt.xlabel('Number of Lobes')
plt.ylabel('Variance') 
plt.grid()
plt.legend()
#save image
plt.savefig("surface_variance_percentiles.png", format="png", dpi=1200)
plt.show()







    

















