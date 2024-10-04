# Displaying ibl single unit metrics in phy

## Prerequisites

- Install [phy](https://github.com/cortex-lab/phy?tab=readme-ov-file#installation-instructions)
- Install [IBL compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)

## Information
This is an optional extension to the Bombcell quality control metrics assignment. Here we provide
the option to additionally display the IBL metrics in phy in order to compare them to the Bombcell metrics.

## Objective
Add the IBLMetricsPlugin to phy and display the IBL metrics in the phy cluster view.

## Assignment

### 1. Copy IBL metrics to phy path
Copy the `clusters.metrics.pqt` file to the folder that contains the data you want to launch phy from. The location
of the `clusters.metrics.pqt` file can be found in the following way,

```python
from one.api import ONE
one = ONE()
pid = '6358854e-51d2-47de-a278-5cbfd155feb6' # note this pid is different from the rest of the course
eid, pname = one.pid2eid(pid)
metrics_file = one.load_dataset(eid, 'clusters.metrics.pqt', collection=f'alf/{pname}/pykilosort', download_only=True)
print(metrics_file)
```

### 2. Add the IBLMetricsPlugin to phy
To display the ibl metrics in the cluster view when launching phy you will need to add the plugin `ibl_metrics.py` provided in 
this folder to your phy config path. This can be done in the following way

Copy the `ibl_metrics.py` file into the folder `~/.phy/plugins/`. If the `plugins` folder does not exist you may have to create it.

Edit the  `~/.phy/phy_config.py` to include the following line at the end of the file.

```python
c.TemplateGUI.plugins = ['IBLMetricsPlugin']
```

For more information see the original [phy documentation](https://phy.readthedocs.io/en/latest/plugins/) on plugins.

If you want the ibl metrics to be computed on the fly for clusters that are merged/ split during manual curation you will
need to install ibllib into your phy environment. This can be done by doing `pip install ibllib`.

### 3. Launch phy and browse metrics
Navigate to the folder containing your spikesorted data. Activate your phy environment and launch phy using the following
command,

```shell
phy template-gui params.py
```

In the cluster view you should see four additional columns
- amp_median
- noise_cutoff
- max_confidence
- label


## Additional Resources

### Definition of IBL metrics
For more information on the IBL single unit metrics please refer to the [spike sorting white paper](https://doi.org/10.6084/m9.figshare.19705522).


### Computing IBL metrics on your own data
In the sample data used for the course the IBL cluster metrics have already been computed and are available for use. However, if you have your own spikesorted data that
has not been run through the IBL spikesorting pipeline then these metrics will not be computed. The code snippets below walk you through how you can compute these IBL metrics on
your own data.

#### 1. Convert spikesorted output to alf format
If your spikesorting output is not already in the ibl alf format you will need to convert it using the `alfConverter`
in phylib

The phylib alf conversion process renames the files such that they follow the naming convention used in the IBL
and also converts the units of the amplitude values in the spikesorting output from arbitrary units to volts. 

The ibl metrics use a median amplitude threshold based on volts so this is why this conversion is necessary to compute
the metrics.

If you already have files with the following names then your output has already been converted and you can skip to **section 2** e.g
- spikes.amps.npy
- spikes.clusters.npy
- spikes.samples.npy
- ....
- clusters.amps.npy
- clusters.waveforms.npy
- etc

If a `clusters.metrics.pqt` file also already exists then the metrics have already been computed and you can skip to **section 3**

If not, the following code can be used to convert your spikesorting output,

```python
from pathlib import Path
from ibllib.ephys.spikes import ks2_to_alf
from ibllib.pipes.ephys_tasks import SpikeSorting

# Path to your spikesorting data
ks_path = Path('/Users/admin/ks_data')
# Path to your raw ephys ap spikeglx data
ap_path = Path('/Users/admin/raw_data')
ap_file = next(ap_path.rglob('*.ap.*bin'), None)
# Path to save alf converted data, must be different from the original spikesorting data
out_path = ks_path.parent.joinpath('alf')

ks2_to_alf(
    ks_path,
    bin_path=ap_path,
    out_path=out_path,
    bin_file = ap_file,
    ampfactor=SpikeSorting._sample2v(ap_file),
)

```

The converted data will be saved in the location `print(out_path)`


#### 2. Compute ibl single unit metrics

The single unit metrics can be computed from the alf converted spikesorting from section 1 using the following code

```python

from ibllib.pipes.ephys_tasks import CellQCMixin
# out_path is the same out_path as section 1 where your alf converted data is
qc_file, _, _ = CellQCMixin.compute_cell_qc(out_path)
```

#### 3. Copy the metrics to the original spikesorting output (optional)
You can copy the computed ibl metrics to your original spikesorting folder. This will allow you to view your original spikesorted data. (The only difference between the alf 
converted data is that the units of the waveforms, spike amplitudes and cluster amplitudes will differ, they will be in volts rather than the units output by the spikesorter)

```python
import shutil
shutil.copy(qc_file, ks_path.joinpath(qc_file.name))
```
