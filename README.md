`GeorulesLobePy`

# GeorulesLobePy
To run the main code run: 
1. Activate the `georuleslobepy` environment
```bash
conda activate georuleslobepy
```
2. Run the main notebook:
``` bash
    GeoRulesLobePy/notebooks/Results_Visualizations.ipynb
```
4. Run the main:
```bash
main.py
```  


### Developer Quick Start
GeorulesLobePy uses Conda to manage the Python environment. External libraries are installed using PIP. Please refer to the Conda documentation.  
- [Managing Conda environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
- [Conda installation guide](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#)

#### Python Environment
To set up the environment from scratch, perform the following commands in the project root. 

1. Create a new conda environment
2. Active the environment
3. Install PIP dependencies
4. Install local project code: 
```bash
# run these commands in the project root
conda create -n georuleslobepy python=3.11 # Step 1: create new georuleslobepy env
conda activate georuleslobepy # Step 2: activate georuleslobepy env
pip install -r requirements.txt # Step 3: install PIP dependencies
pip install -e . # Step 4: install local project code with PIP 
```

**WARNING:** If the requirements change (i.e., in the requirements.txt) you should rebuild the environment from scratch.  
To delete the existing `georuleslobepy` environment run: 
```bash
conda remove --name georuleslobepy --all # remove georuleslobepy env
```
