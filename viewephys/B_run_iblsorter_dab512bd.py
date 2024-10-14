from pathlib import Path

from one.api import ONE
from brainbox.io.one import SpikeSortingLoader
from iblatlas.atlas import BrainRegions

from iblsorter.ibl import run_spike_sorting_ibl, ibl_pykilosort_params, download_test_data

# we download the raw data from the IBL server
one = ONE(base_url='https://openalyx.internationalbrainlab.org')
regions = BrainRegions()
pid = 'dab512bd-a02d-4c1f-8dbc-9155a163efc0'
ssl = SpikeSortingLoader(pid=pid, one=one)
sr_ap = ssl.raw_electrophysiology(band="ap", stream=False)

# load the parameters - this is the dictionary that can be edited if necessary
params = ibl_pykilosort_params(sr_ap.file_bin)

# setup output paths
SCRATCH_DIR = Path.home().joinpath("scratch", 'iblsorter')  # temporary path on which intermediate raw data will be written, we highly recommend a SSD drive
ks_output_dir =  Path.home().joinpath("scratch", pid)  # path containing the kilosort output unprocessed
alf_path = ks_output_dir.joinpath('alf')  # this is the output standardized as per IBL standards (SI units, ALF convention)

# for the multiprocessing part of the spike sorting code, it is
# important to wrap the main call into a __name__ == "__main__" function
if __name__ == "__main__":
    SCRATCH_DIR.mkdir(exist_ok=True)
    ks_output_dir.mkdir(parents=True, exist_ok=True)

    # run sorter
    run_spike_sorting_ibl(
        sr_ap.file_bin,
        delete=True,
        scratch_dir=SCRATCH_DIR,
        ks_output_dir=ks_output_dir,
        alf_path=alf_path,
        log_level='INFO',
        params=params
    )
