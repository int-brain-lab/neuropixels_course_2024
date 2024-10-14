# 1.8.2 and 1.8.3 Practical: Spike sort raw data and inspect results with viewephys

## Introduction
This tutorial will show you how to:

### Inspect a raw data file prior spike sorting
[A_viewephys_on_raw_data.md](A_viewephys_on_raw_data.md)
- Open a spikeglx recording, during acquisition or after the fact and look at the raw data quality
- Look at the bad channel detection and adjust thresholds if necessary

### Launch a spike sorting and look at intermediate results
[B_run_iblsorter.md](/viewephys/B_run_iblsorter.md)
- launch the spike sorter on the dataset (Optional)
- look at and interpret the intermediate outputs of the spike sorter

### Overlay sorter result over raw-data
[C_Overlay_sorter_results_on_raw_data.ipynb](/viewephys/C_Overlay_sorter_results_on_raw_data.ipynb)
- Load a snippet of raw data, and destripe it
- Load the corresponding spike sorting data occuring during this raw data snippet
- Place the information into viewephys, and navigate the user interface


**You will investigate**:
- What signals are visible onto the raw data, giving you a sense of why we want to perform destriping
- Whether the quality of the raw data is subjectively good
- Whether many channels are flagged as "bad" and why
- How well conditionned the cross
- Whether the spike detection is subjectively good
- Whether there is information contained in the spikes rejected as part of bad units

## Pre-requisite

### Python
- Install [ibl compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Install [viewephys](https://github.com/int-brain-lab/viewephys) in this environment using pip

### Data
- Download sample data, following the [data download instructions](https://github.com/int-brain-lab/neuropixels_course_2024/tree/main/data_access) from the course
