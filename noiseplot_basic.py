#!/usr/bin/env python

import matplotlib.pyplot as plt
from obspy.signal.spectral_estimation import get_nlnm, get_nhnm

def setupPSDPlot():
    '''Set up a plot with Peterson noise model for plotting PSD curves.
       x axis = period (s)
       y axis = decibels
       then add a second set of axes for frequency (Hz)
       returns: fig, ax, ax_freq'''
    # get Peterson noise models from ObsPy
    nhnm = get_nhnm()
    nlnm = get_nlnm()

    # Set up period axis
    width=5
    fig = plt.figure(figsize=(6,5))
    ax = fig.add_subplot()
    pd_min = 0.05
    pd_max = 200
    ax.semilogx()
    ax.set_xlim(0.05, 200)
    ax.set_xlabel('Period (s)')
    ax.set_ylabel(r'Power (dB[m$^2$/s$^4$/Hz])')
    ax.set_ylim(-200, -50)
    ax.tick_params(right=True)

    # Plot Peterson noise models 
    ax.plot(nhnm[0], nhnm[1], linewidth=2, color='black', label='NHNM/NLNM')
    ax.plot(nlnm[0], nlnm[1], linewidth=2, color='black')

    # Add frequency axis to plot
    ax_freq = ax.twiny()
    ax_freq.set_xlabel('Frequency (Hz)')
    ax_freq.semilogx()
    ax_freq.set_xlim(1/pd_min, 1/pd_max)
    ax_freq.xaxis.set_label_position('top')
    ax_freq.tick_params(axis='x', top=True, labeltop=True) 


    return fig, ax, ax_freq

fig, ax, ax_freq = setupPSDPlot()
# then more plotting of PSDs here using ax.plot(...) or ax_freq.plot(...)
# then save it
fig.savefig('noise.png')

