#!/usr/bin/env/python
# Request and plot hourly PSD values from MUSTANG
# Obtain hourly PSDs for a given NSCL
# then extract all values at a user-specified frequency
# and plot them as a function of time
import os
import sys
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import xml.etree.ElementTree as ET

# Find the nearest value in an array to a requested value
# Thank you stack overflow for this nice little function
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


# Arguments and usage
#print(len(sys.argv))
#print(sys.argv)
if len(sys.argv) != 6:
    print(f"usage: {sys.argv[0]} net sta loc cha freq")
    print("if location code is blank, use --")
    sys.exit(1)
net, sta, loc, cha = sys.argv[1:5]
request_freq = float(sys.argv[5])


# Request hourly PSDs
filename = f"{net}.{sta}.{loc}.{cha}.xml"
if not os.path.exists(filename):
    print('requesting data')
    res = requests.get(f"https://service.iris.edu/mustang/noise-psd/1/query?net={net}&sta={sta}&loc={loc}&cha={cha}&quality=M&starttime=2023-01-00T00:00:00&endtime=2023-06-14T00:00:00&correct=true&format=xml&nodata=404")
    if res.status_code == 200:
        print("request successful")
        root = ET.XML(res.text)
        outfile = open(filename, 'w')
        outfile.write(res.text)
        outfile.close()
        print(f"wrote {filename}")
    else:
        print("request to noise-psd service not successful")
        print(res.text)
        sys.exit(1)
else:
    print(f'found file {filename}, parsing')
    xml_data = open(filename, 'r').read()
    root = ET.XML(xml_data)

# Find element of XML that contains PSDs 
# (the other elements are: Created, Requested Date Range, Analyzed Date Range)
for thing in root:
    if thing.tag == 'Psds':
        psd_xml = thing


# Loop over PSDs and find values at requested frequency
dates = []
power = []
for i,psd in enumerate(psd_xml):
#    print(psd)
#    print(psd.attrib['start'])
# first we have to get a list of frequency values and find the closest one to our desired frequency
    if i == 0:
        freq_text = []
        freq = []
        for value in psd:
            freq_text.append(value.attrib['freq'])
            freq.append(float(value.attrib['freq']))
        nearest_freq, index = find_nearest(freq, request_freq)
        text_freq = freq_text[index]
# then we loop over all the PSDs and find the values at that frequency
# we compare frequency as a string to avoid floating point weirdness 
# then append it as a floating point for plotting
    for value in psd:
        if value.attrib['freq'] == text_freq:
            print(psd.attrib['start'], value.attrib['freq'], value.attrib['power'])
            dates.append(pd.to_datetime(psd.attrib['start']))
            power.append(float(value.attrib['power']))

# Plotting
print('plotting')
fig = plt.figure()
plt.plot(dates, power, label=f'{net}.{sta}.{loc}.{cha} at {request_freq:.1f} Hz')
plt.legend()
fig.autofmt_xdate(rotation=45)
plotfile = f'{net}.{sta}.{loc}.{cha}_{request_freq:.1f}.png'
fig.savefig(plotfile)
print(f"saved image to {plotfile}")
plt.show()


