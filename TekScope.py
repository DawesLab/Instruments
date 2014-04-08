#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot
import instrument


if __name__ == "__main__":


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

    if wfms[0]=="1":
        ch1data = test.get_data("CH1")

    if wfms[1]=="1":
        ch2data = test.get_data("CH2")

    if wfms[3]=="1":
        refAdata = test.get_data("REFA")

    if wfms[4]=="1":
        refBdata = test.get_data("REFB")

    # Get the timescale
    test.write("HORIZONTAL:MAIN:SCALE?")
    timescale = float(test.read(20))

    # Get the timescale offset
    test.write("HORIZONTAL:MAIN:POSITION?")
    timeoffset = float(test.read(20))

    # Get the length of the horizontal record
    test.write("HORIZONTAL:RECORDLENGTH?")
    time_size = int(test.read(30))

    time = numpy.arange(0,timescale*10,timescale*10/time_size)

    # Start data acquisition again, and put the scope back in local mode
    #test.write("ACQ:STATE RUN")
    #test.write("UNLOCK ALL")

    # Plot the data
    if wfms[0]=="1":
        plot.subplot(4,1,1)
        plot.plot(time,ch1data)
    if wfms[1]=="1":
        plot.subplot(4,1,2)
        plot.plot(time,ch2data)
    if wfms[2]=="1":
        plot.subplot(4,1,3)
        plot.plot(time,refAdata)
    if wfms[3]=="1":
        plot.subplot(4,1,4)
        plot.plot(time,refBdata)

    plot.title("")
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (S)")
    #plot.xlim(time[0], time[599]
    plot.show()
    #plot.savefig("test.png")

    # TODO add file save to this script
