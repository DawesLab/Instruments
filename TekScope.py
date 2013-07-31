#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot
 
import instrument
 
""" Example program to plot the Y-T data from Channel 1"""
 
# Initialize our scope
test = instrument.TekScope1000("/dev/usbtmc0")
 
# Stop data acquisition
test.write("ACQ:STATE STOP")
 
# Grab the data from channel 1
test.write("DATA:SOURCE CH1")

# Set data format to ASCII
test.write("DATA:ENCD ASCII")
 
test.write("CURV?")
rawdata = test.read(9000)
data = numpy.frombuffer(rawdata, 'B')
 
# Get the voltage scale
test.write("CH1:SCALE?")
voltscale = float(test.read(20))
 
# And the voltage offset
test.write("CH1:POSITION?")
voltoffset = float(test.read(20))


#TODO this is all leftover, and probably not valid!
 
# Walk through the data, and map it to actual voltages
# First invert the data (ya rly)
data = data * -1 + 255
 
# Now, we know from experimentation that the scope display range is actually
# 30-229.  So shift by 130 - the voltage offset in counts, then scale to
# get the actual voltage.
data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
 
# Get the timescale
test.write("HORIZONTAL:MAIN:SCALE?")
timescale = float(test.read(20))
 
# Get the timescale offset
test.write("HORIZONTAL:MAIN:POSITION?")
timeoffset = float(test.read(20))
 
# Now, generate a time axis.  The scope display range is 0-600, with 300 being
# time zero.
time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
 
# If we generated too many points due to overflow, crop the length of time.
if (time.size > data.size):
    time = time[0:600:1]
 
# See if we should use a different time axis
if (time[599] < 1e-3):
    time = time * 1e6
    tUnit = "uS"
elif (time[599] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
    tUnit = "S"
 
# Start data acquisition again, and put the scope back in local mode
test.write("ACQ:STATE RUN")
test.write("UNLOCK ALL")
 
# Plot the data
plot.plot(time, data)
plot.title("Oscilloscope Channel 1")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + tUnit + ")")
plot.xlim(time[0], time[599])
plot.show()
