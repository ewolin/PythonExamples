#!/usr/bin/env python

import obspy
from obspy.clients.fdsn import Client
from obspy.signal.tf_misfit import plot_tfr  
from obspy.geodetics import gps2dist_azimuth

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

#####################
# earthquake, station, and plotting parameters
# edit to suit your quake/station of interest
# easy math: 3600 s = 1 hr, 86400 s = 1 day

# Earthquake origin parameters
elat = 29.735 # earthquake latitude
elon = -177.282 # earthquake longitude
t0 = obspy.UTCDateTime('2021-03-04T19:28:32') # quake origin time
t_start = t0 - 0.5*86400 
t_end = t0 + 2*86400

# Station parameters
slat = 34.94591
slon = -106.4572
net = "IU"
sta = "ANMO"
loc = "00"
cha = "VHZ"

# Plot parameters
fmin = 1e-3 # minimum frequency for spectrum + spectrogram
fmax = 1e-2 # max frequency for spectrum + spectrogram
#####################

# initialize client for requesting waveforms
client = Client("IRIS")

print('requesting data')
st = client.get_waveforms("IU", "ANMO", "00", "VHZ", t_start, t_end)
st.write('waveforms.mseed')
st = obspy.read('waveforms.mseed')

#print('decimating')
#st.decimate(factor=5)
#st.decimate(factor=5)
#st.decimate(factor=2)
#st.decimate(factor=2)
#st.select(channel='LHZ', location='00')
#st.trim(starttime=t1)
#st.trim(endtime=st[0].stats.starttime + 86400)

print(st)
print(st[0].stats.delta)

print('filtering')
st.detrend('demean')
st.filter('bandpass', freqmin=fmin, freqmax=fmax)

tr = st[0]

dt = tr.stats.starttime - t0

fig = plot_tfr(tr.data, dt=tr.stats.delta, fmin=fmin, fmax=fmax, w0=10,
         clim=1e3, cmap='magma', show=False)


# plot dispersion curves on top
T, u = np.loadtxt('t-vs-u.csv',  unpack=True, delimiter=',')
f = 1./T


#elat = 55.030 
#elon = -158.522
#slat = 50.1867
#slon = -5.2273


# Optional: Plot predicted Rayleigh wave arrival times 
# in t-vs-u.csv from Oliver (1962) Fig 2.
# https://pubs.geoscienceworld.org/ssa/bssa/article/52/1/81/101314

x_m, meh, meh = gps2dist_azimuth(elat, elon, slat, slon)
x = x_m/1000.
earth_circ = 4e4 # circumference of Earth in km

ax_tfr = fig.axes[1]

cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

font_props = {'ha':'center',
              'va':'bottom',
              'fontsize':'large'}

#plot_rayleigh = True
plot_rayleigh = False
if plot_rayleigh:
    for i in range(4):
        n_odd = 2*i+1
        c_odd = cycle[n_odd]
        t_arr = (x+i*earth_circ)/u - dt
        ax_tfr.plot(t_arr,f, label='R{}'.format(2*i+1), color=c_odd)
        t = ax_tfr.text(t_arr[0], 1.0e-2, 'R{}'.format(n_odd), color=c_odd, 
                        **font_props)
        print(2*i+1, x+i*earth_circ)
    
        n_even = 2*(i+1)
        c_even = cycle[n_even]
        t_arr_min = (earth_circ - x + i*earth_circ)/u - dt
        ax_tfr.plot(t_arr_min,f, ls=':', label='R{}'.format(n_even), 
                    color=c_even)
        t = ax_tfr.text(t_arr_min[0], 1e-2, 'R{}'.format(n_even), color=c_even, 
                    **font_props)
        print(2*(i+1), earth_circ - x + i*earth_circ, '--')#


# Add labels etc
ax_seis = fig.axes[0]
ax_seis.set_ylim(-1.0e3,1.0e3)
ax_seis.set_xlabel('time (s) since {} UTC'.format(tr.stats.starttime.strftime('%Y-%m-%dT%H:%M')))


t_M8 = t0 - t_start
t_M74 = obspy.UTCDateTime("2021-03-04T17:41:24") - t_start
t_M73 = obspy.UTCDateTime("2021-03-04T13:27:36") - t_start
n=0
colors = ["orange", "red", "magenta"]
labels = ["M8.1", "M7.4", "M7.3"]
#for t_quake, label in zip([ t_M8, t_M74, t_M73], ["M8.1", "M7.4", "M7.3"]):
for i,t_quake in enumerate([ t_M8, t_M74, t_M73]):
    ax_seis.plot([t_quake, t_quake], [-2000, 2000], colors[i], ls=":")
    ax_seis.text(t_quake, -1000+n, labels[i], color=colors[i], ha="center", va="bottom")
    n+=200
#ax_seis.set_ylabel('Amplitude\n(counts)')


ax_freq = fig.axes[2]
ax_freq.set_ylabel('frequency (Hz)')
#ax.legend()
#fig3.gca().semilogy()
#plt.savefig('meh.eps')
fig.set_size_inches(10,5)
fig.suptitle('M8.1 Kermadec Earthquake, recorded on GSN IU.ANMO.00')#\n24 hours of data beginning UTC 2020-01-28 19:00\n    ') 
plt.savefig('multiplepassage.png', dpi=300)
#plt.show()


#fig.axes[1]

