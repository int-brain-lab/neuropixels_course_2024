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
```shell
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

Once connected correctly the output of `print(one)` should give,
```python
One (online, https://openalyx.internationalbrainlab.org)
```

## Confirming that the installation has worked
### Checking ibllib
To check the installation of ibllib has worked correctly, open a python or ipython terminal and type the following
```
from brainbox.io.one import SpikeSortingLoader
```
If this imports without any errors then ibllib has been succesfully installed.

### Checking the viewephys gui
To check the installation of the viewephys gui (used in assignment 1.8.3) has worked correctly, open a terminal and type the following
```
conda activate iblenv
viewephys
```
The following window should pop up (the first time this command is launched it may take a while for the window to pop up)

<img width="782" alt="Screen Shot 2024-09-27 at 9 03 16 AM" src="https://github.com/user-attachments/assets/cd680d80-f382-4c7e-a18d-a5a0c761f766">

### Checking the alignment gui
To check the installation of the alignment gui (used in assignment 2.5.2) has worked correctly, open a terminal and type the following
```
conda activate iblenv
ephys-align
```
The following window should pop up (the first time this command is launched it may take a while for the window to pop up)

<img width="1603" alt="Screen Shot 2024-09-27 at 9 02 54 AM" src="https://github.com/user-attachments/assets/8b2cf2f9-2aed-4517-9a2b-5aaf96a8f0e0">

# Installing iblsorter

As part of assignment 1.8.2 of the course you will be asked to run the IBL spikesorting pipeline on an example dataset. This requires the installation of another python enviroment with the ibl-sorter. To run spikesorting you will need to have access to a computer with a high-end NVIDIA GPU with at least 8GB of memory. If you have access to these resources please refer to [these instructions](https://github.com/int-brain-lab/ibl-sorter?tab=readme-ov-file#installation) for how to install a compatible environment

If you do not have access to these resources you will instead download the spikesorting results that can be used in the other assignments.
