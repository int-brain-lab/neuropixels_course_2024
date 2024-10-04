# Assignment aligning spikes to histology (2.5.2)

## Prerequisites
- Install [IBL compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Download sample data
  - Either by following [data download instructions](https://github.com/int-brain-lab/neuropixels_course_2024/tree/main/data_access) from the course
  - or downloading the ephys_alignment_sample_dataset from [here](https://ibl.flatironinstitute.org/public/)

## Objective
Use the IBL alignment gui to use electrophysiological features to align the location of the electrodes in the brain.

Some useful features to look out for in this dataset are 
- The LFP power spectrum in the hippocampus
- The firing rate in the thalamus and CA1 regions


## Assignment

### Launch GUI
In a terminal type the following
```shell
conda activate iblenv
ephys-align
```

### Select dataset
Once the GUI has launched you will see a button in top right hand corner with the symbol `...`. 
Click on this button and navigate to the folder where the input data is stored. 
Once you have selected the folder click the Get Data to load the data into the GUI.

If you are using the dataset that has been used throughout the course, the location of the input data can be found
by typing the following into an ipython terminal
```python
from one.api import ONE
one = ONE()
pid = 'dab512bd-a02d-4c1f-8dbc-9155a163efc0'
eid, pname = one.pid2eid(pid)

ss_file = one.load_dataset(eid, 'spikes.times.npy', collection=f'alf/{pname}/pykilosort', download_only=True)
alf_folder = ss_file.parent
print(alf_folder)
```
An example output is,

```python
/Users/admin/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/alf/probe00/pykilosort/#2024-05-06#
```

### Perform alignment
Once the data has loaded use reference lines to align the electrophysiology and histology data.

- Use the menu drop downs to click through the different electrophysiology plots to explore the data.
- Double click on the ephys image or histology image to add reference lines.
- Drag the reference lines on the electrophysiology and histology images to the locations of choice.
- Once you are happy with their locations click the fit button, the location of electrodes should shift in the brain.
- Add as many reference lines as you see necessary to complete the alignment.
- Once you have finished the alignment click on the upload data to save your new channel locations.

Please refer to these [instructions](https://github.com/int-brain-lab/iblapps/wiki/2.-Usage-instructions#external-users) for a more
detailed guide (N.B refer to the `External Users` sections)


  
## Further resources
- [iblapps alignment gui wiki](https://github.com/int-brain-lab/iblapps/wiki)
- [Blog post on performing alignments](https://github.com/sonjafoerster/internshipNL2023/blob/main/00_OMM_Intro.md)