import os
import time
import numpy
import usbtmc
#TODO: switch to usbtmc module functions instead of file-based reads
import pytest

debug = False

class TekScope1000:
    """Class to control a Tektronix TDS1000 series oscilloscope"""
    def __init__(self, serialno):
        #change to self.inst?
        self.meas = usbtmc.Instrument(0x0699,0x03ab)

        self.name = self.meas.ask("*IDN?")

        print(self.name)

    def write(self, command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)

    def read(self, length = 4000):
        """Read an arbitrary amount of data directly from the scope"""
        return self.meas.read(length)

    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()

    def read_data(self):
        """ Function for reading data and parsing binary into numpy array """
        self.write("CURV?")
        rawdata = self.meas.read_raw(9000)
        if(debug): print(rawdata)

        # First few bytes are characters to specify
        # the length of the transmission. Need to strip these off:
        # we'll assume a 5000-byte transmission
        # so the string would be "#45000" and we therefor strip 6 bytes.
        return numpy.frombuffer(rawdata[6:-1], 'i2')


    def get_data(self,source):
        """
        Get scaled data from source where source is one of
        CH1,CH2,REFA,REFB
        """

        self.write("DATA:SOURCE " + source)
        data = self.read_data()

        # Get the voltage scale
        self.write("WFMP:" + source + ":YMULT?")
        ymult = float(self.read(20))

        # And the voltage offset
        self.write("WFMP:" + source + ":YOFF?")
        yoff = float(self.read(20))

        # And the voltage zero
        self.write("WFMP:" + source + ":YZERO?")
        yzero = float(self.read(20))

        data = ((data - yoff) * ymult) + yzero
        return data

    def get_xdata(self):
        """Method to get the horizontal data array from a scope"""
        # Get the timescale
        self.write("HORIZONTAL:MAIN:SCALE?")
        timescale = float(self.read(20))

        # Get the timescale offset
        self.write("HORIZONTAL:MAIN:POSITION?")
        timeoffset = float(self.read(20))

        # Get the length of the horizontal record
        self.write("HORIZONTAL:RECORDLENGTH?")
        time_size = int(self.read(30))
        if(debug): print("time_array size = ",time_size)

        #time = numpy.arange(0,timescale*10,timescale*10/time_size*2)

        # not sure what the above was for, but I'm doing it with linspace now:
        time = numpy.linspace(0,timescale*10,time_size)

        if(debug): print("length of xdata = ", len(time))
        # For some reason the output was too short compared to the data buffer
        return time

    def test_get_data():
        assert len(self.get_data("CH1")) == 5006




class RigolDG:
    """Class to control a Rigol DG4102 arb wave generator."""
    def __init__(self, device):
        self.meas = usbtmc(device)

        self.name = self.meas.getName()

        print(self.name)

    def write(self, command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)
        time.sleep(0.1)

    def read(self, command):
        """Read an arbitrary amount of data directly from the scope"""
        return self.meas.read(command)

    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()
