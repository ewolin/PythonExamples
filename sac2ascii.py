#!/usr/bin/env python
# Convert a SAC file to a two-column text file
# First column is time in seconds
# Second column is amplitude

import sys
import obspy

# Read names of input file and output file from command line
infile = sys.argv[1]
outname = sys.argv[2]
outfile = open(outname, 'w')

# Make sure we have provided the correct number of arguments
if len(sys.argv) != 3:
    print("Usage: sac2ascii.py myfile.sac outfile.txt")
    sys.exit()

# Use ObsPy to read SAC file into a Stream object
st = obspy.read(infile) 

# A Stream can hold many Traces (individual records)
# but we just want the first one:
tr = st[0] 

# We are only interested in the times and amplitudes of the trace
amps = tr.data
times = tr.times()

# Write times and amplitudes to a text file:
for i in range(len(amps)):
    outfile.write('{0} {1}\n'.format(times[i], amps[i]))

# Close output file and print the name of the output file
outfile.close()
print('Values written to file {0}'.format(outname))
