"""
This code loads data from a Tektronix scope into a 
matplotlib (mpl) plot. Available features:

    * Using the navigation toolbar in the plot
    * Select a channel to view or save
    * Saving the data to a numpy (*.npy) file from the menu

Written by:
Andrew M.C. Dawes (dawes@pacificu.edu)

Based on demo written by:
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""
import sys, os, random
from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

#Use our instrument library for USBTMC communications
import instrument
import numpy


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Tektronix scope data')
        self.data = [0, 0, 0, 0, 0]
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.on_draw()

    def save_plot(self):
        file_choices = "Numpy (*.npy)"

        path, filt = QFileDialog.getSaveFileName(self,
                        'Save file', filter=file_choices)
        if path:
            numpy.save(path, self.data)
            self.statusBar().showMessage('Saved data to %s' % path, 2000)

    def on_about(self):
        msg = """ View and save data from Tektronix scope:
        * Using the navigation toolbar in the plot
        * Select a channel to view or save
        * Saving the data to a numpy (*.npy) file from the menu
        """
        QMessageBox.about(self, "About this code", msg.strip())

    def on_ch1(self):
        self.data = inst.get_data("CH1")
        self.on_draw()

    def on_ch2(self):
        self.data = inst.get_data("CH2")
        self.on_draw()

    def on_refa(self):
        self.data = inst.get_data("REFA")
        self.on_draw()

    def on_refb(self):
        self.data = inst.get_data("REFB")
        self.on_draw()

    def on_draw(self):
        """ Redraws the figure
        """
        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())
        # TODO: scale x data correctly
        self.axes.plot(self.data)
        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QWidget()

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        #
        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)
        self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)

        self.ch1_button = QPushButton("&CH1")
        self.connect(self.ch1_button, SIGNAL('clicked()'), self.on_ch1)

        self.ch2_button = QPushButton("&CH2")
        self.connect(self.ch2_button, SIGNAL('clicked()'), self.on_ch2)

        self.refa_button = QPushButton("&REFA")
        self.connect(self.refa_button, SIGNAL('clicked()'), self.on_refa)

        self.refb_button = QPushButton("&REFB")
        self.connect(self.refb_button, SIGNAL('clicked()'), self.on_refb)




        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.on_draw)

        #
        # Layout with box sizers
        #
        hbox = QHBoxLayout()

        for w in [  self.ch1_button, self.ch2_button, self.refa_button,
                    self.refb_button, self.grid_cb]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save data",
            shortcut="Ctrl+S", slot=self.save_plot,
            tip="Save the numpy data")
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About this code')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    #inst = instrument.TekScope1000("/dev/usbtmc0")
    main()
