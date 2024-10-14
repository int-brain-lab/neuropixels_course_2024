# Spike sorting assignment

The purpose of the assignment is to show how to assess the performance of a spike sorting algorithm on a dataset from the International Brain Laboratory (IBL).
Running the spike sorting on the recording requires a few hours and a Nvidia GPU, and is not necessary for the assignment, whose main purpose
is to navigate the intermediate outputs and quality controls that the sorter outputs.

The results are already available in the repository, so you can skip this step, but we still provide instructions for the enthusiast user.

The dataset is the Neuropixels recording we have been working with throughout the assignments.


## Installing and running the spike sorter

### Installation

The installation steps are described in the original repository installation guide.
[https://github.com/int-brain-lab/ibl-sorter](https://github.com/int-brain-lab/ibl-sorter)

The important part is to make sure the installation has been successful by running the following command:

```python
from iblsorter.utils import cuda_installation_test
cuda_installation_test()
```

### Running the spike sorter
````shell
python 01_run_iblsorter_dab512bd.py
````
The full output of the spike sorter is available on a S3 bucket [here](https://ibl-brain-wide-map-public.s3.amazonaws.com/index.html#spikesorting/dab512bd-a02d-4c1f-8dbc-9155a163efc0/)

## Looking at the intermediate controls

### Checking the whitening 
As we have seen during the lectures the whitening process can have a drastic impact on the spike sorting outcome. 
Here a good way is to look at the estimated covariance matrix. In this case most of the energy is contained on the diagonal, and we can see the reference channel 191 we detected before.
![Covariance matrix](/viewephys/assets/_iblqc_.covariance_matrix.png)

After inversion the whitening matrix is the operator we apply to the data. Here we can see a flattened rendition of the diagonal along with the conditioning number.
The conditioning is a good estimate of how stable is the operator. Values in the single digit range are fine, up to a couple of dozens it is acceptable and above 50 there is a concern with the data. 

![Whitening matrix diagonal](/viewephys/assets/_iblqc_.whitening_matrix.png)

### Drift estimate
The sorter has a motion correction drift estimation and correction component.  Although we output overall recording drift RMS  and cululative absolute drift per hour for individual units, this is a feature of the spike sorting that is useful to visualize.
In this particular instance, the estimated drift is very small, and we can hardly see a difference before and after srift application.
![Drift estimate](/viewephys/assets/_iblqc_.drift_estimate.png)
![Drift registered raster](/viewephys/assets/_iblqc_.drift_registered.png)



