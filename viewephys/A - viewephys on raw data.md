# Use Viewephys to look at raw data

## Step 1 : Open a raw recording
On a terminal activate your environment, and type the following command 

```shell
viewephys
```

![gui file](./viewephys/assets/viewephys.png)

- Click on file, and go to the place where you downloaded the raw data.  This is usually in your `Downloads` folder in your home directory:
`~/Downloads/ONE/openalyx.internationalbrainlab.org/danlab/Subjects/DY_016/2020-09-12/001/raw_ephys_data/probe00/_spikeglx_ephysData_g0_t0.imec0.ap.cbin`
- check the destripe box
- move the slider to the middle of the recording ~1700 seconds
- adjust the window size to your liking
- in view -> colormaps choose the `PuOr` map
- adjust the gain of the display using Control + A or Control + Z
- Control + P will propagate and link the 2 windows together for both
- With the right mouse button pressed you can zoom, with the left button pressed you can pan


On the **raw data** 
- Does this look like neural activity to you? Do you notice any signals leaking into the AP band ? 
- What is the origin of the large black and white oscillations visible near the dentate gyrus ?
- Can you see the vertical stripes, and how they disappear after destriping - does the signal lools like it is preserved ?

On the **destriped data**, do you see any sign of:
- Saturation / Bad channel / Noise
- Can you locate some events that seem to be propagating from top to bottom ? 

![side by side](/viewephys/asset/viewephys_sidebyside.png)


### Open a live recording

You can use this tool on a file during acquisition (it will always access the data read-only).
However at writing the meta-data is incomplete, so you can use the file -> open live recording menu instead. 


## Step 2 : Compute the channel acceptance criteria

One useful step before launching spike sorting is to verify the acceptance critera of channels.

There are 3 ways a channel can be detected as faulty:
- dead channel
- noisy channel
- channel outside of the brain

The thresholds are set by default for NP1.0 and NP2.0 probes from IBL but they may need adapting.

```python
from one.api import ONE
from brainbox.io.one import SpikeSortingLoader
from ibldsp.voltage import detect_bad_channels

one = ONE(base_url='https://openalyx.internationalbrainlab.org')
pid = "dab512bd-a02d-4c1f-8dbc-9155a163efc0"
ssl = SpikeSortingLoader(pid=pid, one=one)
channels = ssl.load_channels()

# here set stream to true if you don't have the raw on disk
sr = ssl.raw_electrophysiology(stream=False, band='ap')  
t0 = 600
first, last = (int(t0 * sr.fs), int((t0 + 0.4) * sr.fs))
raw = sr[first:last, :-sr.nsync].T

channel_labels, _ = detect_bad_channels(raw, fs=sr.fs, display=True)
```

![channels ap](/viewephys/assets/channel_detect_ap.png)

Note that this can also be done on the LFP band in this manner:

```python
# here set stream to true if you don't have the raw on disk
sr = ssl.raw_electrophysiology(stream=True, band='lf')  
t0 = 600
first, last = (int(t0 * sr.fs), int((t0 + 10) * sr.fs))
raw = sr[first:last, :-sr.nsync].T

channel_labels, _ = detect_bad_channels(raw, fs=sr.fs, display=True)
```

![channels lf](/viewephys/assets/channel_detect_lf.png)

