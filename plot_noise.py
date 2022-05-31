#!/usr/bin/env python

# Create PSD PDFs for waveform data from C0 temp experiment
# Helpful in checking out the first few days of data from a deployment
# before MUSTANG metrics are available
# Expects:
#     - waveform data stored locally on disk 
#       in <working_directory>/data/<sta>
#     - responses will be retrieved from IRIS NRL 
#       (user must edit request_nrl, in script below,
#        to reflect correct instrument and digitizer)
# Emily Wolin May 2022

import sys
import obspy
import requests

import numpy as np

from glob import glob
from io import StringIO
from obspy.signal import PPSD
from obspy.imaging.cm import pqlx

if len(sys.argv[1:]) < 4:
    print(f"Usage: {sys.argv[0]} net sta loc ch")
    print("ch is a channel set (BH, HH)")
    print("and the script will loop over 3 components E N Z")
    sys.exit(1)
net, sta, loc, ch = sys.argv[1:]

# Get response from IRIS NRL
# Edit request_url to use appropriate instconfig and datalogger
if sta == 'SHIP':
    request_url = 'https://service.iris.edu/irisws/nrl/1/combine?format=resp&instconfig=sensor_Nanometrics_Trillium120PA_LP120_SG1201_STgroundVel:datalogger_REFTEK_130S-01_PG1_FR100&nodata=404'
if sta == 'RAFT':
    request_url = 'https://service.iris.edu/irisws/nrl/1/combine?instconfig=sensor_Nanometrics_TrilliumCompact120PH_SG754_LP120_STgroundVel:datalogger_REFTEK_130S-01_PG1_FR100&format=resp&nodata=404'

r = requests.get(request_url, verify=False)
outfile = StringIO(r.text)
inv = obspy.read_inventory(outfile, format='RESP')
outfile.close()

# Set NSLC in NRL response to match our station of interest
# NRL should return a response with only one net, sta, loc, cha 
# so we can hard-code this
inv[0].code = 'C0'
inv[0][0].code = sta
inv[0][0][0].location_code = ''
print(inv[0][0][0].response.instrument_sensitivity)
# we'll set the channel code when we compute PPSDs for each station

# Compute and save PPSD
t1 = obspy.UTCDateTime('2022-05-01T00:00')

for comp in ['N', 'E', 'Z']:
    if loc == '--':
        loc = ''
    nslc = f"{net}.{sta}.{loc}.{ch}{comp}"
    print(comp)
    inv[0][0][0].code = f'{ch}{comp}'
    print(inv)
    files = glob(f'data/{sta}/{sta}.{net}.{loc}.{ch}{comp}.2022*')
    st = obspy.read(files[0])
    for f in files[1:]:
        st += obspy.read(f)

    st.trim(starttime=t1)
    tr = st[0]
    
    ppsdnpz = f'{nslc}.npz'
    try: 
        ppsd = PPSD.load_npz(ppsdnpz, metadata=inv)
        print(f'loaded npz from {ppsdnpz}')
    except:
        print('creating new ppsd')
        ppsd = PPSD(tr.stats, metadata=inv, 
                    period_smoothing_width_octaves=1.0)
    ppsd.add(st)
    ppsd.save_npz(ppsdnpz)
    print(f"saved {ppsdnpz}")
    ppsd.calculate_histogram(starttime=t1)

# Plot PPSD, spectrogram, and a few slices at specified periods
# First, PPSD
    use_cmap=pqlx
    fig = ppsd.plot(grid=False, cmap=use_cmap, show=False,
                    show_percentiles=True, percentiles=[5,50,95])
    ax0 = fig.axes[0]
    ax0.tick_params(left=True,right=True)
    try:
        piecewise = '/Users/ewolin/code/HighFreqNoiseMustang_paper/PiecewiseModels'
        nhnb = np.loadtxt(piecewise+'/High_T-vs-dB.txt', unpack=True)
        nlportb = np.loadtxt(piecewise+'/Low_Port_T-vs-dB.txt', unpack=True)
        ax0.plot(nlportb[0], nlportb[1], linewidth=2, ls='--', color='grey',
                label='Low Portable Baseline')
        ax0.plot(nhnb[0], nhnb[1], color='grey', ls=(0,(1,1)), lw=2,
                label='High Baseline')
    except:
        continue
    fig.savefig(f'PPSD_{nslc}.png')
    print(f'saved PPSD_{nslc}.png')

# Spectrogram
    fig = ppsd.plot_spectrogram(clim=[-180,-100],
                                cmap='YlGnBu_r', show=False)
    fig.gca().set_title(f"{nslc}")
    fig.set_size_inches(10,4)
    fig.savefig(f'spectro_{nslc}.png')
    print(f'saved spectro_{nslc}.png')

# Slices at selected periods
    fig2 = ppsd.plot_temporal(period=[0.1, 100], show=False)
    fig2.axes[0].set_ylim(-200,-50)
    fig2.gca().set_title(f"{nslc}")
    fig2.set_size_inches(10,4)
    fig2.savefig(f'pds_{nslc}.png')
    print(f'saved pds_{nslc}.png')
    

     
    
    
    
    
    
