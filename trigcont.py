#!/usr/bin/env python

from glob import glob

from obspy import read_inventory

xmlfiles = glob('*xml')

total_time = 0
trig_time = 0
cont_time = 0

xmlfiles_cont = []

for xf in xmlfiles:
    inv = read_inventory(xf)
#    print(len(inv.networks), len(inv.networks[0].stations), len(inv.networks[0].stations[0].channels))
    t2 = inv.networks[0].stations[0].channels[0].end_date
    t1 = inv.networks[0].stations[0].channels[0].start_date
    chan_type = inv.networks[0].stations[0].channels[0].types
    timespan = t2 - t1 
    if 'CONTINUOUS' in chan_type:
        cont_time += timespan
        xmlfiles_cont.append(xf)
    elif 'TRIGGERED' in chan_type:
        trig_time += timespan
    else:
        print(xf, ':Type contains neither CONTINUOUS nor TRIGGERED flag')
    total_time += timespan

inv_cont = read_inventory(xmlfiles_cont[0])
for xfc in xmlfiles_cont[1:]:
    inv_cont += read_inventory(xfc)
#inv_cont.plot()

print('Total time:')
print(total_time, 's')
print(total_time/86400, 'days')
print(total_time/86400/365, 'years')
    
print('Triggered time:')
print(trig_time, 's')
print(trig_time/86400, 'days')
print(trig_time/86400/365, 'years')

print('Continuous time:')
print(cont_time, 's')
print(cont_time/86400, 'days')
print(cont_time/86400/365, 'years')

print('Cont/Total %: ', cont_time/total_time*100)
print('Trig/Total %: ', trig_time/total_time*100)
