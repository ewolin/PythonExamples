#!/usr/bin/env python

# get a 24-hour miniseed file

import obspy
from obspy.clients.fdsn import Client

client = Client("IRIS")


t1 = obspy.UTCDateTime("2021-03-02T00:00:00")
t2 = t1 + 86400

net = "IU"
sta = "MBWA"
loc = "00"
cha = "BH*"

print("requesting waveform data")
print(f"{net} {sta} {loc} {cha}")
print(f"{t1} {t2}")
st = client.get_waveforms(net, sta, loc, cha, t1, t2)

outfile = f'{net}.{sta}.{loc}.mseed'
st.write(outfile, format='mseed')
print(f"wrote waveforms to {outfile}")
