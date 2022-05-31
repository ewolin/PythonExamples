#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from obspy import UTCDateTime, Stream, read_inventory
from obspy.clients.fdsn import Client

# Function to create subplots
def create_subplot(st, maintitle, xlabel, ylabel, plotno):
# NOTE: use times() method of a Trace to automatically generate a time range!
    axis[plotno].plot(st[plotno].times(), st[plotno], linewidth=0.75)
    axis[plotno].set_title(maintitle)
    axis[plotno].set_xlabel(xlabel)
# NOTE: one-liner to set y-axis range
    yrange = np.abs(st[plotno].max()) 
    axis[plotno].set_ylabel(ylabel)

# Main program
stime = UTCDateTime("2020-01-14T12:26:46.500")
# NOTE: I will use this for the final plot, request a longer seismogram first to apply the taper... 
duration = 10 # duration of record in seconds 
seismometer = 'PR04' # ID for seismometer
processing = [['DISP', 'Puerto Rico ' + seismometer + ' displacement ' + str(stime), 'Displacement (m)'], \
              ['VEL', 'Velocity', 'Velocity (m/s)'], ['ACC', 'Acceleration', r'Acceleration (m/s$^2$)']]

client = Client("IRIS")
# NOTE: Here I request a longer window so there is 'extra' seismogram around the window of interest.
# 100 s is probably a bit much but it rarely hurts to have extra.
st = client.get_waveforms('GS', seismometer, '00', 'HHZ', stime-100, stime+100, attach_response=True)
st.detrend('demean') # NOTE: I prefer 'demean' to 'constant', I think it deals w/long-period noise better 
st = st.taper(0.05, type='hann', max_length=None, side='both')

# NOTE: inventory is already attached so no need to get it separately 
#inventory = read_inventory('https://service.iris.edu/fdsnws/station/1/query?net=GS&sta='+seismometer+'&loc=00&starttime='+str(stime)+'&endtime=' + str(stime+duration)+'&level=response&format=xml')

for x in range(2):
    st += st[0].copy() # duplicate streams for the processed data

# Create the plot
fig, axis = plt.subplots(3, 1, figsize=(16,8), sharex=True) # NOTE: sharex nice for interactive plots!
plt.subplots_adjust(hspace=1)
pre_filt = [0.01, 0.05, 10, 30] # NOTE: Define frequency band in which we will remove response
for splot in range(3):
    st[splot].remove_response(output=processing[splot][0], pre_filt = pre_filt, water_level=None)
    st[splot].trim(stime-1, stime+duration) # NOTE: show a little more pre-event signal
    create_subplot(st, processing[splot][1], "time (s)", processing[splot][2], splot)
    
plt.show()
plt.savefig('pr04.png')


