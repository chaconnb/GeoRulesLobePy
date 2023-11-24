`georules`

# GeoRules


### Developer Quick Start
`GeoRules` uses Conda to manage the Python environment. External libraries are installed using PIP. Please refer to the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) for more information. 

([Conda installation docs](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#))

#### Python Environment
If this is the first time, or you don't have the environment yet, or if you need to recreate the environment from scratch, create the python environment, otherwise skip to the next step. 
```console
conda create -n georules python=3.11
```

Active the environment
```console
conda activate georules
```

Install PIP dependencies
```
pip install -r requirements.txt
```

If the requirements change (i.e., in the requirements.txt) you should rebuild the environment from scratch. 