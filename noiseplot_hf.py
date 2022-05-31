#!/usr/bin/env python

import numpy as np
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
    pd_min = 0.01
    pd_max = 200
    ax.semilogx()
    ax.set_xlim(pd_min, pd_max)
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

    ax.grid()

    
    codedir = '/Users/ewolin/code/HighFreqNoiseMustang_paper'
#    piecewise = os.path.join(codedir,'PiecewiseModels')
    piecewise = codedir+'/PiecewiseModels'

    nhnb = np.loadtxt(piecewise+'/High_T-vs-dB.txt', unpack=True)
    nlportb = np.loadtxt(piecewise+'/Low_Port_T-vs-dB.txt', unpack=True)

    ax.plot(nlportb[0], nlportb[1], linewidth=3, ls='--', color='grey', 
            label='Low Portable Baseline')
    ax.plot(nhnb[0], nhnb[1], color='grey', ls=(0,(1,1)), lw=3, 
            label='High Baseline')

    ax.plot()
    ax.legend()
    return fig, ax, ax_freq

fig, ax, ax_freq = setupPSDPlot()
# then more plotting of PSDs here using ax.plot(...) or ax_freq.plot(...)
# then save it
fig.savefig('noise.png')

