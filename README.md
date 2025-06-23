
# GeorulesLobePy
[![DOI](https://zenodo.org/badge/723123162.svg)](https://doi.org/10.5281/zenodo.15717349)


To run the main code run: 
1. Start by following the steps of the `Developer Quick Start Section`
**Note:** If you've already installed the package in editable mode, you can skip that step.
2. Run the main notebook:
``` bash
notebooks/main_notebook.ipynb
```
or run the main script:
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
3. Install the package in editable mode.
```bash
# run these commands in the project root
conda create -n georuleslobepy python=3.11 # Step 1: create new georuleslobepy env
conda activate georuleslobepy # Step 2: activate georuleslobepy env
pip install -e . # Step 4: install local project code with PIP 
```
This will: 
- Install the `georuleslobepy` package in editable mode, allowing you to modify the code without reinstallation
- Install all necessary dependencies (including support for Jupyter notebooks and interactive PyVista plotting)
  

**WARNING:** If the dependencies listed in `pyproject.toml` change (e.g., new packages are added or versions updated), it is recommended to rebuild the environment from scratch to ensure consistency.

To delete the existing `georuleslobepy` environment run: 
```bash
conda remove --name georuleslobepy --all # remove georuleslobepy env
```

### Acknowledgments

Special thanks to Dr. Daniel Willhelm for help with code refactoring.

