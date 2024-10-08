# Spike sorting assignment

The purpose of the assignment is to show how to assess the performance of a spike sorting algorithm on a dataset from the International Brain Laboratory (IBL).
Running the spike sorting on the recording requires a few hours and a Nvidia GPU, and is not necessary for the assignment, whose main purpose
is to navigate the intermediate outputs and quality controls that the sorter outputs.

The results are already available in the repository, so you can skip this step, but we still provide instructions for the enthusiast user.

The dataset is the Neuropixels recording we have been working with throughout the assignments.


## Installing and running the spike sorter


### Installation

The installation steps are described in the original repository installation guide.
https://github.com/int-brain-lab/ibl-sorter

The important part is to make sure the installation has been successful by running the following command:

```python
from iblsorter.utils import cuda_installation_test
cuda_installation_test()
```

### Running the spike sorter
````shell
python 01_run_iblsorter_dab512bd.py
````