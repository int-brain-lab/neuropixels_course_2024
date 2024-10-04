# Downloading IBL data

## Prerequisites
- Install [IBL compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Minimum of 10Gb of disk space on your local computer to download data

## Example neuropixel recordings
For the course we will use data from a neuropixels recording collected as part of the IBL [brainwide map](https://doi.org/10.1101/2023.07.04.547681) and [reproducible ephys](https://doi.org/10.1101/2022.05.09.491042) projects. 

The selected probe insertion passes through posterior parietal cortex, hippocampus, and thalamus and has a unique probe identifier of `pid = 'dab512bd-a02d-4c1f-8dbc-9155a163efc0'`

You can explore data from this insertion using the IBL [visualisation website](https://viz.internationalbrainlab.org/app?dset=bwm&pid=dab512bd-a02d-4c1f-8dbc-9155a163efc0&tid=0&cid=534&qc=0&spikesorting=ss_2024-05-06)

The example code below will show how to download data for this insertion that is needed for the assignments during the course.

## Instantiate modules
Activate your iblenv environment (`conda activate iblenv`) and launch an ipython terminal `ipython`
```python
from one.api import ONE
from brainbox.io.one import SpikeSortingLoader

# define insertion
pid = 'dab512bd-a02d-4c1f-8dbc-9155a163efc0'
one = ONE()
ssl = SpikeSortingLoader(pid=pid, one=one)
```

## Download raw data (optional)

This code snippet shows how to download the raw AP band electrophysiology data for this probe insertion. This data will be used in
assignment 1.8.2 where you have the option to run the IBL spikesorting pipeline on this dataset. If you do not intend to run spikesorting
this data does not need to be downloaded to complete the other assignments.

N.B. The raw data for each insertion is large, typically between 50 - 80 Gb. You will need to make sure you have enough disk space
and note that the download may also take a while.

```python
sr_ap = ssl.raw_electrophysiology(band='ap', stream=False)
```

## Download spikesorted data
Here we show how to download the spikesorted data for this probe insertion. This data will be used in assignments 1.8.3, 2.5.1 and 2.5.2.
With good internet connection the download of this data should take ~10 mins.

```python
eid, pname = one.pid2eid(pid)
files = one.load_collection(eid, collection=f'alf/{pname}/pykilosort', download_only=True)
```

If the download is proceeding successfully you should see an output similar to the following in your python terminal,

```python
/Users/admin/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/alf/probe00/pykilosort/#2024-05-06#/_ibl_log.info_pykilosort.log: 100%|█| 494k/494k [0
/Users/admin/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/alf/probe00/pykilosort/#2024-05-06#/_kilosort_whitening.matrix.npy: 100%|█| 1.18M/1.18
/Users/admin/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/alf/probe00/pykilosort/#2024-05-06#/_phy_spikes_subset.channels.npy: 100%|█| 13.4M/13.
/Users/admin/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/alf/probe00/pykilosort/#2024-05-06#/_phy_spikes_subset.spikes.npy: 100%|█| 836k/836k [
...
```

Once the download is complete you will be returned a list of downloaded files stored in the variable `files`. Ensure
that number of files downloaded is 35.

```python
print(len(files))
```

## Download histology data
Here we show how to download some extra data (raw ephys features and traced probe insertion info) that will be used to align the histology in assignment 2.5.2. The alignment tool 
requires all the files to be in a single folder so in this code snippet we also ensure this by moving the downloaded features files to the same folder as the spikesorted data.

```python
import shutil
import json
from pathlib import Path

# Download raw ephys features and move them into the alf collection that stores the spikesorting data
# download lfp features
lfp_psd = one.load_object(eid, 'ephysSpectralDensityLF', collection=f'raw_ephys_data/{pname}', download_only=True)
lfp_rms = one.load_object(eid, 'ephysTimeRmsLF', collection=f'raw_ephys_data/{pname}', download_only=True)

# download ap features
ap_rms = one.load_object(eid, 'ephysTimeRmsAP', collection=f'raw_ephys_data/{pname}', download_only=True)

# Get the location of the spikesorted data and copy the raw_feature files to this folder
ss_file = one.load_dataset(eid, 'spikes.times.npy', collection=f'alf/{pname}/pykilosort', download_only=True)
alf_folder = ss_file.parent

for file in lfp_psd + lfp_rms + ap_rms:
  shutil.copy(file, alf_folder.joinpath(file.name))

# Read in the user traced track for the probe insertion and save to file
ins = one.alyx.rest('insertions', 'read', id=pid)
xyz_picks = ins['json']['xyz_picks']
data = {'xyz_picks': xyz_picks}
with open(Path(alf_folder, 'xyz_picks.json'), "w") as f:
  json.dump(data, f, indent=2)

```

## Additional Resources
Here we have provided code to download the data necessary for the course. To explore more about the IBL data the ONE api you can explore
the following resources
- [IBL documentation](https://int-brain-lab.github.io/iblenv/public_docs/public_introduction.html)
- [ONE documentation](https://int-brain-lab.github.io/ONE/)
- [Brainwide map introduction](https://colab.research.google.com/drive/1Ua-NlpYYZCIOF56xbsT9YR71Enkotd-b#scrollTo=7XzVVlhsVHMK)
- [ONE tutorial](https://colab.research.google.com/drive/1y3sRI1wC7qbWqN6skvulzPOp6xw8tLm7#scrollTo=GSvi21Dn84wJ)
