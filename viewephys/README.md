## 1.8.3 Practical: Inspect sorting results in viewEphys

### Introduction
This tutorial will show you how to:

- Load a snippet of raw data, and destripe it
- Load the corresponding spike sorting data occuring during this raw data snippet
- Place the information into viewephys, and navigate the user interface

You will investigate:
- What signals are visible onto the raw data, giving you a sense of why we want to perform destriping
- Whether the quality of the raw data is subjectively good
- Whether the spike detection is subjectively good
- Whether there is information contained in the spikes rejected as part of bad units

### Pre-requisite

#### Python
- Install [ibl compatible environment](https://github.com/int-brain-lab/neuropixels_course_2024/blob/main/installation/README.md)
- Install [viewephys](https://github.com/int-brain-lab/viewephys) in this environment using pip

#### Data
- Download sample data, following the [data download instructions](https://github.com/int-brain-lab/neuropixels_course_2024/tree/main/data_access) from the course

