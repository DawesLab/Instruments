import os
import time
import numpy

class usbtmc:
    """Simple implementation of a USBTMC device driver, in the style of visa.h"""

    def __init__(self, device):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

        # TODO: Test that the file opened

    def write(self, command):
        os.write(self.FILE, command.encode('utf-8'));

    def read(self, length = 4000):
        return os.read(self.FILE, length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def sendReset(self):
        self.write("*RST")


class TekScope1000:
    """Class to control a Tektronix TDS1000 series oscilloscope"""
    def __init__(self, device):
        self.meas = usbtmc(device)

        self.name = self.meas.getName()

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
        rawdata = self.read(9000)

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

        time = numpy.arange(0,timescale*10,timescale*10/time_size)
        return time




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
