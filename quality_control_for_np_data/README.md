# Displaying ibl single unit metrics in phy

## Prerequisites

- Install [phy](https://github.com/cortex-lab/phy?tab=readme-ov-file#installation-instructions)
- Install [IBL compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Download and unzip the file `dataset.zip` from [here](https://rdr.ucl.ac.uk/articles/dataset/Recording_with_a_Neuropixels_probe/25232962/1)
- Download the file `Hopkins_20160722_g0_t0.imec.ap.meta` [here](https://rdr.ucl.ac.uk/articles/dataset/Recording_with_a_Neuropixels_probe/25232962/1) and place it in the unzipped dataset folder.

## Information
This is an optional additional assignment that shows how to compute the IBL metrics on a non IBL dataset and view the IBL metrics in phy. 

## Objective
Compute the IBL metrics on the sample dataset and then add the IBLMetricsPlugin to phy and display the IBL metrics in the phy cluster view.

## Assignment

### 1. Compute IBL metrics on sample dataset
#### 1.1 Convert spikesorted output to alf format
If your spikesorting output is not already in the ibl alf format you will need to convert it using the `alfConverter`
in phylib

The phylib alf conversion process renames the files such that they follow the naming convention used in the IBL
and also converts the units of the amplitude values in the spikesorting output from arbitrary units to volts. 

The ibl metrics use a median amplitude threshold based on volts so this is why this conversion is necessary to compute
the metrics.

If you already have files with the following names then your output has already been converted and you can skip to **section 1.2** e.g
- spikes.amps.npy
- spikes.clusters.npy
- spikes.samples.npy
- ....
- clusters.amps.npy
- clusters.waveforms.npy
- etc

If a `clusters.metrics.pqt` file also already exists then the metrics have already been computed and you can skip to **section 1.3**

If not, the following code can be used to convert your spikesorting output,

```python
from pathlib import Path
from ibllib.ephys.spikes import ks2_to_alf
from ibllib.pipes.ephys_tasks import SpikeSorting

# Path to your spikesorting data (e.g the dataset folder)
ks_path = Path('/Users/admin/dataset')
# Path to your raw ephys ap spikeglx data, we must have an .ap.meta file
# (in this case the raw ephys path is the same as the spikesorting path)
ap_path = Path('/Users/admin/dataset')
ap_file = next(ap_path.rglob('*.ap.*bin'), None)
meta_file = next(ap_path.rglob('*.ap.*meta'), None)
# Path to save alf converted data, must be different from the original spikesorting data
out_path = ks_path.parent.joinpath('alf')

ks2_to_alf(
    ks_path,
    bin_path=ap_path,
    out_path=out_path,
    bin_file = ap_file,
    ampfactor=SpikeSorting._sample2v(meta_file.with_suffix('.bin')),
)

```

The converted data will be saved in the location `print(out_path)`


#### 1.2 Compute ibl single unit metrics

The single unit metrics can be computed from the alf converted spikesorting from section 1.1 using the following code

```python
import one.alf.io as alfio
import numpy as np
import pandas as pd
from brainbox.metrics.single_units import quick_unit_metrics, METRICS_PARAMS

def compute_metrics(file_path):

    spikes = alfio.load_object(file_path, 'spikes')
    clusters = alfio.load_object(file_path, 'clusters')
    df_units = quick_unit_metrics(spikes.clusters, spikes.times, spikes.amps, spikes.depths,
                                  cluster_ids=np.arange(clusters.channels.size), params=METRICS_PARAMS)
    df_units.pop('n_spikes_below2')
    df_units = pd.DataFrame(df_units)
    metrics_file = Path(file_path).joinpath('clusters.metrics.pqt')
    df_units.to_parquet(metrics_file)
    return metrics_file


# out_path is the same out_path as section 1 where your alf converted data is
qc_file = compute_metrics(out_path)
```

#### 1.3 Copy the metrics to the original spikesorting output
You can copy the computed ibl metrics to your original spikesorting folder. This will allow you to view your original spikesorted data. (The only difference between the alf 
converted data is that the units of the waveforms, spike amplitudes and cluster amplitudes will differ, they will be in volts rather than the units output by the spikesorter)

```python
import shutil
shutil.copy(qc_file, ks_path.joinpath(qc_file.name))
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
