# Keithley 2400 SourceMeter Python Library and Controller
This repo contains a python class which allows for python-based control an automation of the Keithley 2400 SourceMeter device. A GUI allows for simple implementation of this module for data collection and rapid visualization. This is built with the pygraph library (http://www.pyqtgraph.org/), based on the pyqt framework.

The Keithley class opens a serial connection to the device through an RS232 port using the keithley_serial module. Implemented so far is ability to:
- configure setup parameters
- configure biasing/current parameters
- configure measurements parameters
- define and configure voltage sweeps
- send general commands (given in Keithley manual)
- collect data from Keithley

To run the GUI from the command line, in the directory of keithley_gui.py:

python keithley_gui.py port_for_keithley

The data are stored as JSON files (for simple viewing, future options for binary storage coming!), which are accesible using the json python module. For example, to access the stored data dictionary with python (FIX THIS CODE TO WORK FOR KEITHLEY):

    import json
    f = open('my_data', 'r')
    data = json.load(f)
    signal_from_channel_0 = data['adc0']['signal']

Requires the pyqtgraph and numpy packages.

Notes:
- installing pyqt can be a bit of a pain (at least on macOS). This is a good explanation: link to that explanation.
- Timing of sweep steps appears to be accurate only to a couple of ms. If you request a 0-10V sweep with 1V steps amd 1 ms delays, you get increments of 1V, but the times vary up to a few ms.
- The GUI is mostly meant as a use example, very under developed...
