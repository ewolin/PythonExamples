#!/usr/bin/env python

import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn import RoutingClient
import os
# Set up client 
# NEW! RoutingClient allows us to get data from multiple sources
# IRIS, GFZ, etc
#client = Client("IRIS")
client = RoutingClient("iris-federator")

# Event info
# Start and end of time window
t1 = obspy.UTCDateTime('2017-12-28T20:23:00')
t2 = t1 + 5*60
# latitude and longitude
evla = 22.056
evlo = 94.404

# Station list for bulk download
bulk = [("MM", "*", "*", "H*", t1, t2),
        ("GE", "NPW", "*", "H*", t1, t2)]

filebase = 'M5nearChauk'
xmlfile=filebase+'.xml'
mseedfile=filebase+'.mseed'

# Uncomment to request data
if not os.path.exists(mseedfile):
    print("requesting waveforms")
    st = client.get_waveforms_bulk(bulk)
    st.write(mseedfile,format='mseed')
    print("got waveforms")
if not os.path.exists(xmlfile):
    print("requesting station inventory")
    inv = client.get_stations_bulk(bulk, level="response")
    inv.write(xmlfile, format='stationxml')
    print("got station inventory")

# Read saved miniseed and inventory
st = obspy.read(mseedfile)
inv = obspy.read_inventory(xmlfile)


# Define station coords for use w/record section plot option 
for tr in st:
    trid = tr.get_id()
    trcoords = inv.get_coordinates(trid)
    tr.stats.coordinates = obspy.core.util.attribdict.AttribDict()
    tr.stats.coordinates.latitude = trcoords['latitude']
    tr.stats.coordinates.longitude = trcoords['longitude']
    tr.data = tr.data/tr.stats.calib


# Select and process broadband channels 
st_bb = st.select(channel="HHZ")
#st_bb.detrend(type='linear').filter('lowpass', freq=20)
st_bb.detrend(type='linear').filter('lowpass', freq=2)

# Optional: trim to starttime of earthquake 
#t0 = obspy.UTCDateTime('2017-12-28T20:23:33')
#st_bb.trim(t0, t2+250)

# Plot record section, but don't show yet
fig = st_bb.plot(equal_scale=False, method='full', type='section', ev_coord=(evla, evlo), dist_degree=True, orientation='horizontal', scale=1, color='station', alpha=0.7, handle=True, norm_method='trace')

# Plot station labels on top of traces
# sttime is seconds after start of plot 
sttime = 5
for tr in st_bb:
    dist_m, az, baz = obspy.geodetics.gps2dist_azimuth(evla, evlo, tr.stats.coordinates.latitude, tr.stats.coordinates.longitude)
    distdeg = obspy.geodetics.kilometers2degrees(dist_m/1000.)
    fig.gca().text(sttime, distdeg, tr.stats.station, alpha=0.5)
# Special stuff to offset many stations at same distance
# probably a more elegant way to automate this
#    if tr.stats.station == 'NPW':
#        fig.gca().text(sttime, distdeg-0.2, tr.stats.station, alpha=0.5)
#    elif tr.stats.station == 'TGI':
#        fig.gca().text(sttime, distdeg+0.2, tr.stats.station, alpha=0.5)
#    else:
#        fig.gca().text(sttime, distdeg, tr.stats.station, alpha=0.5)

# Delete default legend (it's in random order and not that helpful)
fig.gca().legend_.remove()

# Save figure
#fig.show()
fig.savefig('recsec.png')
print('saved plot to recsec.png')

