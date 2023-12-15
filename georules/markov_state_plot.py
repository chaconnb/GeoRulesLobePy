# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 07:14:47 2023

@author: Nataly Chacon-Buitrago
Script for plotting the frequency of Markov states across all realizations.
"""
import matplotlib.pyplot as plt
from utils import load_list_json
from collections import Counter

#input 
n_test = 300

#list that will have quadrants (Markov State) for all realizations
total_quadrants = []

for n in range(n_test):
    #combine the lists of quadrants
    total_quadrants = total_quadrants +  load_list_json("quadrants{}".format(n),"3d_grid_inputs")
 
# Calculate the frequency of each quadrant
frequency_counter = Counter(total_quadrants)

# Extract the quadrants and their frequencies
quadrants = list(frequency_counter.keys())
frequencies = list(frequency_counter.values())

# Plot the bar graph
plt.grid()
plt.bar(quadrants, frequencies, color='blue', zorder=2)
# Plot the grid with a lower zorder value
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
plt.xlabel('Markov states')
plt.ylabel('Frequency')

plt.savefig("quadrants_plot.png", format="png", dpi=1200)
plt.show()