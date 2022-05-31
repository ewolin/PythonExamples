#!/usr/bin/env python

# run in an environment with obspy and numpy

import numpy as np
from obspy.signal.spectral_estimation import get_nlnm, get_nhnm
import matplotlib.pyplot as plt

# get_n?nm returns arrays w/ decreasing T
# np.interp needs T in ascending order so flip them around
T_l, dB_l = get_nlnm()
T_h, dB_h = get_nhnm()

# Calculate differences
T = T_l
dB_d = dB_h - dB_l

for pd in [ 0.125, 0.25, 0.5, 1, 4, 8, 18, 22, 90, 110,  200, 500 ]:
    dB_d_i = np.interp(pd, T[::-1], dB_d[::-1])
    print("'"+str(pd)+"'", ':', dB_d_i, ',')

plt.plot(T, dB_d)
plt.semilogx()
plt.xlim(1e-2, 1e3)
plt.show()
