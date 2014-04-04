#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot


import instrument

""" Program to plot the Y-T data from selected channels."""

# Add command line options:
from optparse import OptionParser

def read_data():
	""" Function for reading data and parsing binary into numpy array """
	test.write("CURV?")
	rawdata = test.read(9000)

	# First few bytes are characters to specify the length of the transmission. Need to strip these off:
	# we'll assume a 5000-byte transmission so the string would be "#45000" and we therefor strip 6 bytes.
	return numpy.frombuffer(rawdata[6:-1], 'i2')

# Initialize our scope
test = instrument.TekScope1000("/dev/usbtmc0")

# Stop data acquisition
test.write("ACQ:STATE STOP")

# Set data width to 2 for better resolution
test.write("DATA:WIDTH 2")

# Set data format to binary, zero is center-frame and big endian
test.write("DATA:ENCD SRI")

# Find out what is displayed on the scope:
# "wfms" is a string with 1 or 0 for CH1,CH2,MATH,REFA,REFB
test.write("SELECT?")
wfms = test.read(20)
# parse into array of characters
wfms = wfms.strip().split(";")

# Grab the data from channel 1

if wfms[0]=="1":
    test.write("DATA:SOURCE CH1")
    ch1data = read_data()

    # Get the voltage scale
    test.write("WFMP:CH1:YMULT?")
    ymult = float(test.read(20))

    # And the voltage offset
    test.write("WFMP:CH1:YOFF?")
    yoff = float(test.read(20))

    # And the voltage zero
    test.write("WFMP:CH1:YZERO?")
    yzero = float(test.read(20))

    ch1data = ((ch1data - yoff) * ymult) + yzero

if wfms[1]=="1":
    test.write("DATA:SOURCE CH2")
    ch2data = read_data()

    # Get the voltage scale
    test.write("WFMP:CH2:YMULT?")
    ymult = float(test.read(20))

    # And the voltage offset
    test.write("WFMP:CH2:YOFF?")
    yoff = float(test.read(20))

    # And the voltage zero
    test.write("WFMP:CH2:YZERO?")
    yzero = float(test.read(20))

    ch2data = ((ch2data - yoff) * ymult) + yzero

def get_data(source):
    """
    Get scaled data from source where source is one of
    CH1,CH2,REFA,REFB
    """

    test.write("DATA:SOURCE" + source)
    data = read_data()

    # Get the voltage scale
    test.write("WFMP:" + source + ":YMULT?")
    ymult = float(test.read(20))

    # And the voltage offset
    test.write("WFMP:" + source + ":YOFF?")
    yoff = float(test.read(20))

    # And the voltage zero
    test.write("WFMP:" + source + ":YZERO?")
    yzero = float(test.read(20))

    data = ((data - yoff) * ymult) + yzero
    return data



if wfms[3]=="1":
    test.write("DATA:SOURCE REFA")
    refAdata = read_data()

    # Get the voltage scale
    test.write("WFMP:REFA:YMULT?")
    ymult = float(test.read(20))

    # And the voltage offset
    test.write("WFMP:REFA:YOFF?")
    yoff = float(test.read(20))

    # And the voltage zero
    test.write("WFMP:REFA:YZERO?")
    yzero = float(test.read(20))

    refAdata = ((refAdata - yoff) * ymult) + yzero


if wfms[4]=="1":
    test.write("DATA:SOURCE REFB")
    refBdata = read_data()

    # Get the voltage scale
    test.write("WFMP:REFB:YMULT?")
    ymult = float(test.read(20))

    # And the voltage offset
    test.write("WFMP:REFB:YOFF?")
    yoff = float(test.read(20))

    # And the voltage zero
    test.write("WFMP:REFB:YZERO?")
    yzero = float(test.read(20))

    refBdata = ((refBdata - yoff) * ymult) + yzero

# Get the timescale
test.write("HORIZONTAL:MAIN:SCALE?")
timescale = float(test.read(20))

# Get the timescale offset
test.write("HORIZONTAL:MAIN:POSITION?")
timeoffset = float(test.read(20))

# Get the length of the horizontal record
test.write("HORIZONTAL:RECORDLENGTH?")
time_size = int(test.read(30))

# Now, generate a time axis.  The scope display range is 0-600, with 300 being
# time zero.
#time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
#time = numpy.arange(time_size)

#time = time / time_size * timescale * 10
time = numpy.arange(0,timescale*10,timescale*10/time_size)

# Start data acquisition again, and put the scope back in local mode
#test.write("ACQ:STATE RUN")
#test.write("UNLOCK ALL")

# Plot the data
plot.subplot(3,1,1)
plot.plot(time,ch1data)
plot.subplot(3,1,2)
plot.plot(time,refAdata)
plot.subplot(3,1,3)
plot.plot(time,refBdata)

plot.title("")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (S)")
#plot.xlim(time[0], time[599]
plot.show()
#plot.savefig("test.png")

# TODO add file save to this script
