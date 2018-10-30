#!/usr/bin/env python

# AMCDawes 2016 plotting Tektronix scope output. Based on the example:
# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Use our instrument library for USBTMC communications
import instrument
import numpy

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5)
        #TODO: be able to pause
        self.xdata = inst.get_xdata()
        #print(len(self.xdata))
        self.channel = "CH1"

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        #l = [random.randint(0, 10) for i in range(4)]
        self.data = inst.get_data(self.channel)
        #print(len(self.data))
        self.axes.plot(self.xdata, self.data, 'r')
        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.file_menu.addAction('&Save', self.fileSave,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        @pyqtSlot()
        def on_ch1():
            ''' Chan1 button is clicked. '''
            print('ch1 clicked')
            self.dc.channel = "CH1"
            self.statusBar().showMessage("Channel 1")

        @pyqtSlot()
        def on_ch2():
            ''' Chan2 button is clicked. '''
            print('ch2 clicked')
            self.dc.channel = "CH2"
            self.statusBar().showMessage("Channel 2")

        @pyqtSlot()
        def on_ref1():
            ''' Ref1 button is clicked. '''
            print('ref1 clicked')
            #TODO: check for available channel
            self.dc.channel = "REF1"
            self.statusBar().showMessage("Reference 1")

        @pyqtSlot()
        def on_ref2():
            ''' Ref2 button is clicked. '''
            print('ref2 clicked')
            self.dc.channel = "REF2"
            self.statusBar().showMessage("Reference 2")

        @pyqtSlot()
        def on_pause():
            ''' RunStop button is clicked. '''
            print('RunStop clicked')
            #query current state:
            #inst.write("ACQ:STATE STOP")
            inst.write("ACQ:STATE?")
            mesg = inst.read()
            if (mesg == b'1\n'):
                inst.write("ACQ:STATE STOP")
                self.statusBar().showMessage("Stopped")
            elif (mesg == b'0\n'):
                inst.write("ACQ:STATE RUN")
                self.statusBar().showMessage("Running")
            else:
                inst.write("ACQ:STATE RUN")
                print("bad state message, set to RUN")
            #print(mesg)
            #inst.write("ACQ:STATE RUN")

        vbox = QtWidgets.QVBoxLayout(self.main_widget)
        #sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        pauseButton = QtWidgets.QPushButton("&RUN/STOP")
        pauseButton.clicked.connect(on_pause)


        ch1button = QtWidgets.QPushButton("&CH1")
        ch1button.clicked.connect(on_ch1)
        ch2button = QtWidgets.QPushButton("&CH2")
        ch2button.clicked.connect(on_ch2)
        ref1button = QtWidgets.QPushButton("&REF1")
        ref1button.clicked.connect(on_ref1)
        ref2button = QtWidgets.QPushButton("&REF2")
        ref2button.clicked.connect(on_ref2)

        channelBox = QtWidgets.QHBoxLayout() #TODO does this need a parent?
        channelBox.addWidget(ch1button)
        channelBox.addWidget(ch2button)
        channelBox.addWidget(ref1button)
        channelBox.addWidget(ref2button)

        #TODO is this safe or reasonable, had to put dc in self to acces the data for saving
        self.dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        vbox.addWidget(self.dc)
        vbox.addWidget(pauseButton)
        vbox.addLayout(channelBox)



        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileSave(self):
        file_choices = "Numpyz (*.npz)"

        path, filt = QtWidgets.QFileDialog.getSaveFileName(self,
                        'Save file', filter=file_choices)

        if path:
            numpy.savez(path, x=self.dc.xdata, y=self.dc.data)
            self.statusBar().showMessage('Saved data to %s' % path, 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self,"About","Stuff")

def main():
    qApp = QtWidgets.QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())

if __name__ == "__main__":
    inst = instrument.TekScope1000("/dev/usbtmc0")
    main()
