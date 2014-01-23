#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot

import instrument

""" Script to check connection to Rigol DG4102."""

# Add command line options:
from optparse import OptionParser

# Initialize our scope
rgdg = instrument.RigolDG("/dev/usbtmc1")

# set voltage high
rgdg.write(":VOLT:HIGH 3.95")
