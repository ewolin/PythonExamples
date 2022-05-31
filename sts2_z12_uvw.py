#!/usr/bin/env python
# Compare Z12 and UVW components for an STS-2
# EW Feb 2021

import obspy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('MacOSX')


# Rotation matrix for an STS-2, from RBH notes on rotation
rot = 1./(np.sqrt(6))*np.array([[-2, 0, np.sqrt(2)],[1, np.sqrt(3), np.sqrt(2)],[1, -1*np.sqrt(3), np.sqrt(2)]])

#st = obspy.read('/Users/ewolin/tr1/telemetry_days/US_DGMT/2021/2021_007/00_LH*')
st = obspy.read('/Users/ewolin/tr1/telemetry_days/US_BOZ/2021/2021_068/00_LH*')
#st = obspy.read('/Users/ewolin/tr1/telemetry_days/US_DGMT/2021/2021_004/00_LH*')
x = st.select(channel='LH2')[0].data
y = st.select(channel='LH1')[0].data
z = st.select(channel='LHZ')[0].data
u = rot[0][0]*x+rot[0][1]*y+rot[0][2]*z
v = rot[1][0]*x+rot[1][1]*y+rot[1][2]*z
w = rot[2][0]*x+rot[2][1]*y+rot[2][2]*z


meh = np.array([x,y,z,u,v,w])
ylim = (1.05*meh.min(), 1.05*meh.max())
#ylim=(-650e3,150e3)

fig0, ax0 = plt.subplots(3,1, sharey=True, sharex=True)
for i in range(len(st)):
    ax0[i].plot(st[i].times(), st[i].data, label=st[i].stats.channel)
    ax0[i].legend()
#ax0[0].set_xlim(60e3,66e3)
#ax0[0].set_ylim(ylim)
fig0.suptitle('Z12 (unrotated)')
ax0[2].set_xlabel('time(s)')
ax0[1].set_ylabel('counts')
fig0.savefig('unrotated.png')

#fig, ax = plt.subplots(3,1, sharey=True, sharex=True)
fig, ax = plt.subplots(3,1, sharex=True)
ax[0].plot(st[0].times(), u, label='u')
ax[1].plot(st[0].times(), v, label='v')
ax[2].plot(st[0].times(), w, label='w')
for i in range(len(st)):
    ax[i].legend()
#ax[0].set_xlim(60e3,66e3)
#ax[0].set_ylim(ylim)
ax[1].set_ylabel('counts')
ax[2].set_xlabel('time(s)')
fig.suptitle('UVW (rotated)')
fig.savefig('rotated.png')

#plt.show()

st[0].data = u
st[1].data = v
st[2].data = w
st.write('10rot.mseed')
