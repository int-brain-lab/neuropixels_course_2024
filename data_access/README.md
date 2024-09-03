# Downloading IBL data

## Prerequisites
- Installation of ibl compatible environment (link here to other read me)
- Space of around 100Gb to download raw data

## Example neuropixel recordings
For the course we will use data from two neuropixels recordings collected as part of the IBL brain-wide-map project.

The first insertion 

The second insertion passes through. This insertion contains a few artefacts midway through the recording. We have chosen
this insertion to showcase some of the nuances of spikesorting preprocessing methods that will be introduced during the course.

You can explore data from the two insertions using the IBL visualisation website
- Insertion 1
- Insertion 2

The example code below will show how to download data for the first insertion. You can download the data for the second insertion
by replacing the `pid` variable in the code below

## Instantiate modules
Activate your iblenv environment (`conda activate iblenv`) and launch an ipython terminal `ipython`
```python
from one.api import ONE
from brainbox.io.one import SpikeSortingLoader

# define insertion, here w
pid = ''
one = ONE()
ssl = SpikeSortingLoader(pid=pid, one=one)
```


## Download raw data 
This code snippet shows how to download the raw ap data which is required for assignments 1.1 and 1.2.

N.B. The raw data for each insertion is large typically between 50-80Gb. You will need to make sure you have enough disk space
and the download will also take a while
```python
sr_ap = ssl.raw_electrophysiology(band='ap', stream=False)
```

## Download spikesorted data
Here we show how to download the spikeorted data. In assignment 1.1 you will be asked to use the ibl spikesorting pipieline
to spikesort the raw data downloaded in section. If you are unable, however, to spikesort you can download the already spikesorted data 
in the following way. We recommend downloading this data anyway so the next section (LINK) can be run in advance to generate
the data required for the histology section
```python
eid, pname = one.pid2eid(pid)
one.load_collection(eid, f'alf/{pname}/pykilosort', revision='2024-05-06', download_only=True)
```

## Download and extract histology data
Here we show how to download the extra histology code
```python
# need to download the lfp features and ap features and move them into the alf collection in order to launch
# the gui in offline mode
# also need to make the xyz_picks.json file using the picks that exist on the alyx database

# Can download the lfp files
```


## More info
Here we have provided code to 