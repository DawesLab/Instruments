'''
A bokeh-based interface for a tektronix oscilloscope
'''
import numpy as np

import numpy.random as random
import time
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Paragraph, RangeSlider
from bokeh.plotting import figure


import instrument

realInstrument = True
# To debug away from the device. True connects for real, False uses fake data

if realInstrument:
    # TODO automagic this, can't use serial.tools
    inst = instrument.TekScope1000('/dev/usbtmc0')

# Set up data
timedata = np.arange(50)
data = np.zeros(50)
source = ColumnDataSource(data=dict(x=timedata, y=data))

# Set up plot
plot = figure(plot_height=400, plot_width=800, title="Channel 1",
              tools="crosshair,pan,reset,save,wheel_zoom", y_range = (-10,10))

plot.background_fill_color = "white"
plot.border_fill_color = "white"

plot.line(x='x', y='y', source=source)

# Set up widgets to control scale of plots
# TODO change these to actual range sliders
command = TextInput(title="Command Entry:", value='raw counts')
range_slider = RangeSlider(start=-10, end=10, value=(-10,10), step=0.1, title="Y Scale")
scalemin = Slider(title="Singles Scale minimum", value=-10.0, start=-100.0, end=100.0, step=1)
scalemax = Slider(title="Singles Scale maximum", value=10.0, start=-100.0, end=100.0, step=1)
statsA = Paragraph(text="100", width=400, height=40)
statsB = Paragraph(text="100", width=400, height=40)


# Set up callbacks
def send_command(attrname, old, new):
    #TODO turn into a raw command area for sending any device command
    plot.title.text = command.value

command.on_change('value', send_command)

last_time = time.time()
def update_data():
    # TODO: store data in a stream for charting vs time

    global last_time
    T = time.time() - last_time
    last_time = time.time()
    #print(T)

    # get data:
    if realInstrument:
        data = inst.get_data("CH1")  # select channel later on
        timedata = inst.get_xdata()
    else:
        mockdata = np.sin(0.4*np.arange(50))
        data = (random.rand(50)-0.5) + mockdata
        timedata = np.arange(50)

    # statsA.text = "A: %d +/- %d" % (np.mean(a), np.std(a))
    # statsB.text = "B: %d +/- %d" % (np.mean(b), np.std(b))

    #print(raw)
    # plot.title.text = "A:%d B:%d" % (raw[0], raw[1])
    # Get the current slider values
    # a = scalemax.value
    # b = scalemin.value
    # w = phase.value
    # k = freq.value

    source.data = dict(x=timedata, y=data)

def update_scales(attrname, old, new):

    # Get the current slider values
    # smin = scalemin.value
    # smax = scalemax.value

    #update()

    plot.y_range.start = range_slider.value[0]
    plot.y_range.end = range_slider.value[1]

for w in [scalemin, scalemax, range_slider]:
    w.on_change('value', update_scales)


# Set up layouts and add to document
countControls = widgetbox(command, range_slider)

curdoc().add_root(row(countControls, plot, column(statsA, statsB), width=1400))
curdoc().title = "Bokeh Scope"
curdoc().add_periodic_callback(update_data, 100)
