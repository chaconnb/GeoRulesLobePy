`GeorulesLobePy`

# GeorulesLobePy
To run the main code run: 
1. Activate the `georuleslobepy` environment
```bash
conda activate georuleslobepy
```
2. Run the main notebook:
``` bash
notebooks/Results_Visualizations.ipynb
```
3. Run the main:
```bash
main.py
```  


### Developer Quick Start
GeorulesLobePy uses Conda to manage the Python environment. External libraries are installed using PIP. Please refer to the Conda documentation.  
- [Managing Conda environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
- [Conda installation guide](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#)

#### Installation
To set up the environment from scratch and install the package along with all required dependencies, follow these steps:
 
```bash
# run these commands in the project root
# Step 1: Create a new conda environment with Python 3.11
conda create -n georuleslobepy python=3.11
# Step 2: Activate the environment
conda activate georuleslobepy
# Step 3: Install the package in editable mode (installs all dependencies listed in pyproject.toml)
pip install -e .
```
This will: 
- Install the `georuleslobepy` package in editable mode, allowing you to modify the code without reinstallation
- Install all necessary dependencies (including support for Jupyter notebooks and interactive PyVista plotting)
  

**WARNING:** If the dependencies listed in `pyproject.toml` change (e.g., new packages are added or versions updated), it is recommended to rebuild the environment from scratch to ensure consistency.

To delete the existing `georuleslobepy` environment run: 
```bash
conda remove --name georuleslobepy --all # remove georuleslobepy env
```

#### Acknowledgments

Special thanks to Dr. Daniel Willhelm for help with code refactoring.

