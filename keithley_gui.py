#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Keithley GUI

This script runs a GUI to control and record/plot data
from the Keithley 2400 SourceMeter.

This GUI implmentation was originally inspired by the
ZetCode PyQt5 tutorial by Jan Bodnar (zetcode.com)

author: T. Max Roberts
"""

import sys, time
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtGui, QtCore
import keithley_control as kc

class Keithley_GUI(QtGui.QMainWindow):

    def __init__(self, port, connected=True):
        super(Example, self).__init__()

        self.initKeithley(port, connected=connected)
        self.initUI()

    def initKeithley(self, port, connected):
        if connected:
            self.keithley = kc.Keithley(port)
        else:
            self.keithley = kc.FakeKeithley()


    def initUI(self):

        grid = QtGui.QGridLayout()
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setLayout(grid)
        self.setCentralWidget(self.main_widget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy = QtGui.QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        # Here we define the buttons and inputs

        # Output Toggle
        self.output = QtGui.QCheckBox('Output On', self)
        self.output.toggle()
        self.output.stateChanged.connect(self.toggleOutput)
        self.output.setCheckState(False)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.output)
        grid.addLayout(hbox, 0, 0)


        # Make plotting area
        red = (255,0,0)
        green = (0,255,0)
        blue = (0,0,255)
        self.plotWidget1 = PlotWidget()
        self.a0 = self.plotWidget1.plot([], [], pen=blue)
        self.plotWidget2 = PlotWidget()
        self.a1 = self.plotWidget2.plot([], [], pen=green)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.plotWidget1)
        vbox.addWidget(self.plotWidget2)
        grid.addLayout(vbox, 0, 3, 8, 12)

        # Make reset button
        button = QtGui.QPushButton("reset")
        button.clicked.connect(self.buttonClicked)
        grid.addWidget(button, 0, 1)

        #############  Trigger Field and Label #################
        self.num_trig = self.keithley.get_num_triggers()
        self.trigLabel = QtGui.QLabel('Num Trigs: %s' %self.num_trig)
        self.trigEdit = QtGui.QLineEdit()
        self.trigButton = QtGui.QPushButton('num_trigs')
        self.trigButton.clicked.connect(self.buttonClicked)
        self.trigEdit.returnPressed.connect(self.trigButton.click)
        self.trigEdit.setSizePolicy(sizePolicy)
        grid.addWidget(self.trigLabel, 1, 0)
        grid.addWidget(self.trigEdit, 1, 1, 1, 1)


        ##############################################
        #############  Sweep Section #################
        ##############################################

        self.sweepLabel = QtGui.QLabel('<b><u>Sweep Set up </u></b>')
        grid.addWidget(self.sweepLabel, 2, 0)

        #############  Sweep Start Field and Label #################
        self.startLabel = QtGui.QLabel('Start (Volts):')
        self.startEdit = QtGui.QLineEdit('-10')
        self.startButton = QtGui.QPushButton("start")
        self.startEdit.returnPressed.connect(self.startButton.click)
        self.startEdit.setSizePolicy(sizePolicy)
        self.startButton.clicked.connect(self.buttonClicked)
        grid.addWidget(self.startLabel, 3, 0)
        grid.addWidget(self.startEdit, 3, 1)

        #############  Sweep Stop Field and Label #################
        self.stopLabel = QtGui.QLabel('Stop (Volts):')
        self.stopEdit = QtGui.QLineEdit('10')
        self.stopButton = QtGui.QPushButton("stop")
        self.stopEdit.returnPressed.connect(self.stopButton.click)
        self.stopEdit.setSizePolicy(sizePolicy)
        self.stopButton.clicked.connect(self.buttonClicked)
        grid.addWidget(self.stopLabel, 4, 0)
        grid.addWidget(self.stopEdit, 4, 1)

        #############  Sweep Step Field and Label #################
        self.stepLabel = QtGui.QLabel('Step (Volts):')
        self.stepEdit = QtGui.QLineEdit('1')
        self.stepButton = QtGui.QPushButton('step')
        self.stepEdit.returnPressed.connect(self.stepButton.click)
        self.stepEdit.setSizePolicy(sizePolicy)
        self.stepButton.clicked.connect(self.buttonClicked)
        grid.addWidget(self.stepLabel, 5, 0)
        grid.addWidget(self.stepEdit, 5, 1)

        #############  Sweep Num Sweeps Field and Label #################
        self.numSweepsLabel = QtGui.QLabel('Num Sweeps:')
        self.numSweepsEdit = QtGui.QLineEdit('1')
        self.numSweepsButton = QtGui.QPushButton('numSweeps')
        self.numSweepsEdit.returnPressed.connect(self.numSweepsButton.click)
        self.numSweepsEdit.setSizePolicy(sizePolicy)
        self.numSweepsButton.clicked.connect(self.buttonClicked)
        grid.addWidget(self.numSweepsLabel, 6, 0)
        grid.addWidget(self.numSweepsEdit, 6, 1)

        #############  Start Sweep Button #################
        self.startSweepButton = QtGui.QPushButton('Start Sweep!')
        self.startSweepButton.clicked.connect(self.buttonClicked)
        grid.addWidget(self.startSweepButton, 7, 0)

        ##############################################
        #############  Overall Layout ################
        ##############################################

        self.statusBar()

        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Keithley Controller')
        self.show()


    def buttonClicked(self):

        sender = self.sender()

        if sender.text() == "reset":
            self.keithley.reset()
            self.keithley.run_start_up_commands()
            self.keithley.set_output_off()
            self.output.setCheckState(False)
            self.trigLabel.setText('Num Trigs: %s' %1)
            self.statusBar().showMessage("Output Off")

        if sender.text() == "num_trigs":
            self.keithley.set_num_triggers(int(self.trigEdit.text()))
            response = self.keithley.get_num_triggers()
            self.trigLabel.setText('Num Trigs: %s' %response)
            self.trigEdit.setText('')

         ######## Sweep Parameter Buttons ########

        if sender.text() == "Start Sweep!":
            start = int(self.startEdit.text())
            stop = int(self.stopEdit.text())
            step = float(self.stepEdit.text())
            num_sweeps = int(self.numSweepsEdit.text())
            sweep_data = self.keithley.sweep(start=start,  stop=stop,
                                        step=step, num_sweeps=num_sweeps)
            print(sweep_data[0])
            if sweep_data != None:
                self.a0.setData(sweep_data[0], sweep_data[1])
                self.a1.setData(sweep_data[1], sweep_data[2])

    def toggleOutput(self, state):

        if state == QtCore.Qt.Checked:
            self.keithley.set_output_on()
            self.statusBar().showMessage("Output On")
        else:
            self.keithley.set_output_off()
            self.statusBar().showMessage("Output Off")

    def setTrig(self):
        self.keithley.set_num_triggers(int(self.trigEdit.text()))
        response = self.keithley.get_num_triggers()
        self.trigLabel.setText('Num Trigs: %s' %response)
        self.trigEdit.setText('')

    """  Make sure to close the serial connection before exit """
    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.keithley.set_output_off()
            time.sleep(.25)
            self.keithley.close_serial()
            time.sleep(.25)
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':

    # if len(sys.argv) > 1:
    #     port = float(sys.argv[1])
    # else:
    #     print("Need to specify port for the SourceMeter.")
    #     print("Something like: python keithley_gui.py port_for_keithley")
    #     sys.exit()
    app = QtGui.QApplication(sys.argv)
    ex = Keithley_GUI(port, connected=True)  ##### CHANGE THIS TO TRUE!!!
    sys.exit(app.exec_())
