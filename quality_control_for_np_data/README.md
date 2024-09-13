# Displaying ibl single unit metrics in phy

## Installation

- Install [phy](https://github.com/cortex-lab/phy?tab=readme-ov-file#installation-instructions)
- Install [ibl compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)


### 1. Convert spikesorted output to alf format
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

If a clusters.metrics.pqt file also already exists then the metrics have already been computed and you can skip to **section 3**

If not, the following code can be used to convert your spikesorting output
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


### 2. Compute ibl single unit metrics

The single unit metrics can be computed from the alf converted spikesorting from section 1 using the following code

```python

from ibllib.pipes.ephys_tasks import CellQCMixin
# out_path is the same out_path as section 1 where your alf converted data is
qc_file, _, _ = CellQCMixin.compute_cell_qc(out_path)
```

### 3. Copy the metrics to the original spikesorting output (optional)
You can copy the computed ibl metrics to your original spikesorting folder. This will allow you to view your original spikesorted data. (The only difference between the alf 
converted data is that the units of the waveforms, spike amplitudes and cluster amplitudes will differ, they will be in volts rather than the units output by the spikesorter)

```python
import shutil
shutil.copy(qc_file, ks_path.joinpath(qc_file.name))
```

### 4. Add the ibl_metrics plugin to phy

To display the ibl metrics in the cluster view when launching phy you will need to add the plugin `ibl_metrics.py` provided in 
this folder to your phy config path. This can be done in the following way

Copy the `ibl_metrics.py` file into the folder `~/.phy/plugins/`. If the `plugins` folder does not exist you may have to create it.

Edit the  `~/.phy/phy_config.py` to include the following line at the end of the file
```python
c.TemplateGUI.plugins = ['IBLMetricsPlugin']
```

If you want the ibl metrics to be computed on the fly for clusters that are merged/ split during manual curation you will
need to install ibllib into your phy environment. This can be done by `pip install ibllib`
