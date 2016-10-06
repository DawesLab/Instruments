"""
Tektronix scope interface in python.

Andrew Dawes (dawes@pacificu.edu)
Based on demo by:
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
"""
import os
import pprint
import random
import wx

# The recommended way to use wx with mpl is with the WXAgg
# backend.
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import instrument
import numpy


class ScopeFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Tektronix scope download'

    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)

        self.data = [0, 0, 0, 0, 0]
        self.xdata = range(len(self.data))
        
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()

        self.draw_figure()

    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save data to Numpy\tCtrl-S", "Save data to Numpy file")
        self.Bind(wx.EVT_MENU, self.on_save_data, m_expt)
        m_expt = menu_file.Append(-1, "&Save data to CSV\tCtrl-Shift-S", "Save data to CSVfile")
        self.Bind(wx.EVT_MENU, self.on_save_data_csv, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About this software")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        """ Creates the main panel with all the controls on it:
             * mpl canvas
             * mpl navigation toolbar
             * Control panel for interaction
        """
        self.panel = wx.Panel(self)

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        self.ch1button = wx.Button(self.panel, -1, "CH1")
        self.Bind(wx.EVT_BUTTON, self.on_ch1_button, self.ch1button)

        self.ch2button = wx.Button(self.panel, -1, "CH2")
        self.Bind(wx.EVT_BUTTON, self.on_ch2_button, self.ch2button)

        self.ch3button = wx.Button(self.panel, -1, "CH3")
        self.Bind(wx.EVT_BUTTON, self.on_ch3_button, self.ch3button)

        self.ch4button = wx.Button(self.panel, -1, "CH4")
        self.Bind(wx.EVT_BUTTON, self.on_ch4_button, self.ch4button)

        
        self.refabutton = wx.Button(self.panel, -1, "RefA")
        self.Bind(wx.EVT_BUTTON, self.on_refa_button, self.refabutton)

        self.refbbutton = wx.Button(self.panel, -1, "RefB")
        self.Bind(wx.EVT_BUTTON, self.on_refb_button, self.refbbutton)

        self.cb_grid = wx.CheckBox(self.panel, -1,
            "Show Grid",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)

        # Create the navigation toolbar, tied to the canvas
        #
        self.toolbar = NavigationToolbar(self.canvas)

        #
        # Layout with box sizers
        #

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.AddSpacer(10)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.hbox.Add(self.ch1button, 0, border=3, flag=flags)
        self.hbox.Add(self.ch2button, 0, border=3, flag=flags)
        self.hbox.Add(self.ch3button, 0, border=3, flag=flags)
        self.hbox.Add(self.ch4button, 0, border=3, flag=flags)
        self.hbox.Add(self.refabutton, 0, border=3, flag=flags)
        self.hbox.Add(self.refbbutton, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)
        self.hbox.AddSpacer(30)

        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
        """ Redraws the figure
        """
        
        # clear the axes and redraw the plot anew
        self.axes.clear()
        self.axes.grid(self.cb_grid.IsChecked())

        self.axes.plot([i*1000 for i in self.xdata], self.data)
        self.canvas.draw()

    def on_cb_grid(self, event):
        self.draw_figure()

    def on_ch1_button(self, event):
        self.data = inst.get_data("CH1")
        self.xdata = inst.get_xdata()
        self.draw_figure()

    def on_ch2_button(self, event):
        self.data = inst.get_data("CH2")
        self.xdata = inst.get_xdata()
        self.draw_figure()

    def on_ch3_button(self, event):
        self.data = inst.get_data("CH3")
        self.xdata = inst.get_xdata()
        self.draw_figure()

    def on_ch4_button(self, event):
        self.data = inst.get_data("CH4")
        self.xdata = inst.get_xdata()
        self.draw_figure()
        
    def on_refa_button(self, event):
        self.data = inst.get_data("REFA")
        self.xdata = inst.get_xdata()
        self.draw_figure()

    def on_refb_button(self, event):
        self.data = inst.get_data("REFB")
        self.xdata = inst.get_xdata()
        self.draw_figure()

    def on_save_data(self, event):
        file_choices = "Numpy (*.npy)|*.npy"

        dlg = wx.FileDialog(
            self,
            message="Save data as...",
            defaultDir=os.getcwd(),
            defaultFile="data",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #self.canvas.print_figure(path, dpi=self.dpi)
            numpy.save(path, (self.xdata, self.data))
            self.flash_status_message("Data saved to %s" % path)

    def on_save_data_csv(self, event):
        file_choices = "CSV (*.csv)|*.csv"

        dlg = wx.FileDialog(
            self,
            message="Save data as...",
            defaultDir=os.getcwd(),
            defaultFile="data",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #self.canvas.print_figure(path, dpi=self.dpi)
            out = numpy.zeros((len(self.data), 2))
            for (i,l) in enumerate(zip(self.xdata, self.data)):
                out[i,:] = l
            numpy.savetxt(path, out)
            self.flash_status_message("Data saved to %s" % path)

            
    def on_exit(self, event):
        self.Destroy()

    def on_about(self, event):
        msg = """ View and save data from Tektronix scope:

         * Use the matplotlib navigation bar
         * Select a channel to view or save
         * Save the data to a file using the File menu
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER,
            self.on_flash_status_off,
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)

    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


if __name__ == '__main__':
    inst = instrument.TekScope1000("/dev/usbtmc0")

    app = wx.App(False)
    app.frame = ScopeFrame()
    app.frame.Show()


    app.MainLoop()
