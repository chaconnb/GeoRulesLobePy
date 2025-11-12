## Transition Matrices
File with the transtions matrices for different simulations. This transition matrices where used in the paper `GeoRulesLobePy: A Markov Chain-Based Approach for Rule-Based Deepwater Lobe Training Images in Subsurface Modeling`.

### Some definitions
Q1, Q2, Q3, and Q4 refer to the quadrants where the lobe moves. The quadrants are determined by the angles within each quadrant. \
NMA refers to a major avulsion, meaning that the lobe will be deposited in an unrelated place compared to the previous one.\
HF refers to hemipelagic flow, which involves the deposition of a thin mud layer all over the sandbox.

### Simulation 1-3
On x and y-axis: Q1,Q2,Q3,Q4,NMA,HF\
Quadrant angles: Q1: [315,45], Q2:[45,135], Q3:[135,225], Q4:[225,315]\
transition matrix = [[[0.1,0.13,0.3,0.15,0.22,0.1],[0.3,0.05,0.3,0.15,0.15,0.05],[0.3,0.13,0.1,0.15,0.18,0.14],[0.25,0.1,0.25,0.09,0.22,0.09],
[0.05,0.25,0.25,0.25,0.05,0.15],[0.15,0.25,0.25,0.25,0.05,0.05]]]

### Simulation 4-6
On x and y-axis: Q1,Q2,Q3,Q4,NMA,HF\
Quadrant angles: Q1: [315,45], Q2:[45,135], Q3:[135,225], Q4:[225,315]\
transition matrix = [[[0.05,0.25,0.15,0.25,0.15,0.15],[0.15,0.2,0.1,0.3,0.2,0.05],[0.2,0.2,0.1,0.2,0.2,0.1],[0.15,0.3,0.1,0.2,0.2,0.05],
[0.2,0.2,0.2,0.2,0.1,0.1],[0.1,0.3,0.1,0.3,0.1,0.1]]] 
