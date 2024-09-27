# Assignment aligning spikes to histology (2.5.2)

## Prerequisites
- Install [ibl compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Download sample data
  - Either by following [data download instructions](https://github.com/int-brain-lab/neuropixels_course_2024/tree/main/data_access) from the course
  - or downloading the ephys_alignment_sample_dataset from [here](https://ibl.flatironinstitute.org/public/)


## Launch GUI
In a terminal type the following
```commandline
conda activate iblenv
ephys-align
```

## Select dataset
Once the GUI has launched you will see a button in top right hand corner with the symbol `...`. 
Click on this button and navigate to the folder where the input data is stored. 
Once you have selected the folder click the Get Data to load the data into the GUI.

If you are using the dataset that has been used throughout the course, the location of the input data can be found
by typing the following into an ipython terminal
```python
from one.api import ONE
one = ONE()
pid = 'dab512bd-a02d-4c1f-8dbc-9155a163efc0'

ss_file = one.load_dataset(eid, 'spikes.times.npy', collection=f'alf/{pname}/pykilosort', download_only=True)
alf_folder = ss_file.parent
print(alf_folder)
```

## Objective
Use the alignment gui to use electrophysiological features to align the location of the electrodes in the brain.

Some useful features to look out for in this dataset are 
- The LFP power spectrum in the hippocamapus
- The firing rate in the thalamus and CA1 regions
  
## Further resources
- [iblapps alignment gui wiki](https://github.com/int-brain-lab/iblapps/wiki)
