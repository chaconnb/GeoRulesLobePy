# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:04:08 2023

@author: Nataly Chacon_Buitrago
Markov- Chain function to select stacking patterns


Markov_chain - Function to select stacking patterns for n lobes
inputs: 
    start_state = Select one string from the states list. Each state represents a quadrant to move the lobe. The value of the quadrant is given by the user. 
    lobe_number = Number of lobes we want to deposit
    transition_matrix = Every state in the state space is included once as a row and again as a column, and each cell in the matrix tells you the 
    probability of transitioning from its row's state to its column's state. See example in: https://www.datacamp.com/tutorial/markov-chains-python-tutorial
    
output:
    stacking_list = List in order of the different quadrants, chosen using Markov chain. 
    
"""

import numpy as np

## Example of Parameters

# The statespace
# states = ["Q1","Q2","Q3","Q4", "NMA","HF ] NMA-> stands for new major avulsion, HF-> stands for hemipelagic flow
# start_state = "Q1" -> Select one state from the states list
# lobe_number = number of lobes  we want to deposit
# transition_matrix = [[0.1,0.5,0.1,0.2,0.1],[0.3,0.1,0.3,0.1,0.2],[0.65,0.2,0.1,0,0.05],[0.2,0.7,0,0,0.1]] # Probabilities matrix




# A function that implements the Markov model to forecast the state/mood.
def stack_forecast(start_state,lobe_number,transition_matrix):
    
    # Choose the starting state
    stacking_angle = start_state
    # Transition Name - combination of differnt states
    transition_name = [["Q1Q1","Q1Q2","Q1Q3","Q1Q4","Q1NMA","Q1HF"],["Q2Q1","Q2Q2","Q2Q3","Q2Q4","Q2NMA","Q2HF"],["Q3Q1","Q3Q2","Q3Q3","Q3Q4","Q3NMA","Q3HF"],["Q4Q1","Q4Q2","Q4Q3","Q4Q4","Q4NMA","Q4HF"],
                       ["NMAQ1","NMAQ2","NMAQ3","NMAQ4","NMANMA","NMAHF"],["HFQ1","HFQ2","HFQ3","HFQ4","HFNMA","HFHF"] ]
    
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    stackingList = [start_state]
    i = 0
    while i != lobe_number-1: # Subtract one, because we know the state of the first lobe
        if stacking_angle == "Q1":
            change = np.random.choice(transition_name[0],replace=True,p=transition_matrix[0])
            if change == "Q1Q1":
                stackingList.append("Q1")
                pass
            elif change == "Q1Q2":
                stacking_angle = "Q2"
                stackingList.append("Q2")
            elif change == "Q1Q3":
                stacking_angle = "Q3"
                stackingList.append("Q3")
            elif  change == "Q1NMA":
                stacking_angle = "NMA"
                stackingList.append("NMA")
            elif  change == "Q1HF":
                stacking_angle = "HF"
                stackingList.append("HF")
            else:
                stacking_angle = "Q4"
                stackingList.append("Q4")
                
        elif stacking_angle == "Q2":
             change = np.random.choice(transition_name[1],replace=True,p=transition_matrix[1])
             if change == "Q2Q1":
                 stackingList.append("Q1")
                 pass
             elif change == "Q2Q2":
                 stacking_angle = "Q2"
                 stackingList.append("Q2")
             elif change == "Q2Q3":
                 stacking_angle = "Q3"
                 stackingList.append("Q3")
             elif  change == "Q2NMA":
                stacking_angle = "NMA"
                stackingList.append("NMA")
             elif  change == "Q2HF":
                stacking_angle = "HF"
                stackingList.append("HF")
             else:
                 stacking_angle = "Q4"
                 stackingList.append("Q4")
                       
        elif stacking_angle == "Q3":
             change = np.random.choice(transition_name[2],replace=True,p=transition_matrix[2])
             if change == "Q3Q1":
                 stackingList.append("Q1")
                 pass
             elif change == "Q3Q2":
                 stacking_angle = "Q2"
                 stackingList.append("Q2")
             elif change == "Q3Q3":
                 stacking_angle = "Q3"
                 stackingList.append("Q3")
             elif  change == "Q3NMA":
                stacking_angle = "NMA"
                stackingList.append("NMA")
             elif  change == "Q3HF":
                stacking_angle = "HF"
                stackingList.append("HF")
             else:
                 stacking_angle = "Q4"
                 stackingList.append("Q4")
        
        elif stacking_angle == "Q4":
               change = np.random.choice(transition_name[3],replace=True,p=transition_matrix[3])
               if change == "Q4Q1":
                   stackingList.append("Q1")
                   pass
               elif change == "Q4Q2":
                   stacking_angle = "Q2"
                   stackingList.append("Q2")
               elif change == "Q4Q3":
                   stacking_angle = "Q3"
                   stackingList.append("Q3")
               elif  change == "Q4NMA":
                  stacking_angle = "NMA"
                  stackingList.append("NMA")
               elif  change == "Q4HF":
                  stacking_angle = "HF"
                  stackingList.append("HF")
               else:
                   stacking_angle = "Q4"
                   stackingList.append("Q4") 
                   
        elif stacking_angle == "NMA":
                change = np.random.choice(transition_name[4],replace=True,p=transition_matrix[4])
                if change == "NMAQ1":
                    stackingList.append("Q1")
                    pass
                elif change == "NMAQ2":
                    stacking_angle = "Q2"
                    stackingList.append("Q2")
                elif change == "NMAQ3":
                    stacking_angle = "Q3"
                    stackingList.append("Q3")
                elif  change == "NMANMA":
                  stacking_angle = "NMA"
                  stackingList.append("NMA")
                elif  change == "NMAHF":
                  stacking_angle = "HF"
                  stackingList.append("HF")
                else:
                    stacking_angle = "Q4"
                    stackingList.append("Q4") 
                
                
        elif stacking_angle == "HF":
                change = np.random.choice(transition_name[4],replace=True,p=transition_matrix[4])
                if change == "HFQ1":
                    stackingList.append("Q1")
                    pass
                elif change == "HFQ2":
                    stacking_angle = "Q2"
                    stackingList.append("Q2")
                elif change == "HFQ3":
                    stacking_angle = "Q3"
                    stackingList.append("Q3")
                elif  change == "HFNMA":
                   stacking_angle = "NMA"
                   stackingList.append("NMA")
                elif  change == "HFHF":
                   stacking_angle = "HF"
                   stackingList.append("HF")
                else:
                   stacking_angle = "Q4"
                   stackingList.append("Q4") 
                     
        i += 1  
        
    return(stackingList)




















