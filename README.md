Something broke, it only reads from USB in 1024-byte chunks. Need to rewrite the read function?

Instruments
========

Python code for interacting with our lab instruments via USBTMC

 - TekScope - Textronix TDS1000-series scopes
 - RigolDG - Rigol DG4102 Arb Gen.

Requirements:

 - matplotlib
 - numpy
 - wxgtk (i.e. via `sudo apt-get install python-wxgtk3.0` in Ubuntu/Debian linux or `conda install wxpython` for Anaconda python mac)
 - python-usbtmc (installed with `pip`) pypi.python.org/pypi/python-usbtmc


Also included is a desktop file for running the TekScopeGUI.py program in gnome, and an icon file created from the following command:

convert -resize x96 -gravity center -crop 96x96+0+0 ~/Downloads/icon.png -flatten -colors 256 -background transparent tekscope.ico


