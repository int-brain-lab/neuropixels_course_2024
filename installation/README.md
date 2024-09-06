# Installing compatible python environment

## Creating a new python environment
### Using conda (recommended way)
To create a conda environment, [anaconda](https://www.anaconda.com/) must first be installed.

Once installed launch an anaconda prompt terminal and create a new conda environment.

`conda create --name iblenv python=3.11`

Enter yes when prompted

The new environment can be activated using,

`conda activate iblenv`

### Using virtualenv
A new virtualenv can be created by launching a terminal and typing the following (assumes python has already been 
installed on the system)

`virtualenv iblenv --python=python3`

The new environment can be activated using,

`source ./iblenv/bin/activate`

## Install ibl packages

With your iblenv python environment activated (`conda activate iblenv`) install the following python packages
```commandline
pip install ONE-api
pip install ibllib
pip install git+https://github.com/int-brain-lab/iblapps.git
pip install viewephys
pip install ipython
```

## ONE configuration
The very first time you use ONE (the IBL api to access data) you will need to provide credentials to configure the connection
to the database. 

Open a python or ipython terminal and type the following
```python
from one.api import ONE
ONE.setup(base_url='https://openalyx.internationalbrainlab.org', silent=True)
one = ONE(password='international')
```





