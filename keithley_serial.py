#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import serial

"""
Open a port for serial communication with the Keithley.
Returns: serial object
"""
def start_serial(port='/dev/tty.KeySerial1'):

    # Configure the serial connections.
    # These are specific to the Keithley 2400 SourceMeter.
    # This device is configurable, but these are default (except for BAUD).
    # Using a carriage return only for termination.
    try:
        ser = serial.Serial(
            port=port,
            baudrate=57600,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE
        )

        # Need to set the "request to send" pin low
        ser.setRTS(False)

        return ser
    except:
        print("Some went wrong...")

def write(ser, command):
    ser.write(command + '\r')

def open_serial(ser):
    ser.open()

def close_serial(ser):
    ser.close()

def read(ser):
        out = []
        terminated = False
        while ser.inWaiting() > 0 or not terminated:
            data = str(ser.read(1))
            if data == '\r':
                out.append('\n')
                terminated = True
            else:
                out.append(data)

        if out != '':
            return ' '.join(out)
        else:
            return ''

def write_and_read(ser, command, pause=.25):
    write(ser, command)
    time.sleep(pause)
    return read(ser)
