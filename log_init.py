#!/usr/bin/python

################################################################################
# Filename: dev_logger.py
#
# Description:
# Opens the device serial port and logs any data collected from it.
################################################################################

import serial
import pyaudio
import wave
import time

# file parameters
TIMESTAMP = str(int(time.time()))
WAVE_OUTPUT_FILENAME = "audio/async_"+TIMESTAMP+".wav"
DEV_FILENAME = 'log/connect_dev_'+TIMESTAMP+'.txt' # cnc computer
HOST_FILENAME = 'lgo/connect_host_'+TIMESTAMP+'.txt' # cnc mill
DEV_NAME = '/dev/tty.usbserial-FT9AJZ83'
HOST_NAME = '/dev/tty.usbserial-FT9AJZ8W'

# audio parameters
CHUNK = 2**12
FORMAT=pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SAMPLEWIDTH = 2

# serial parameters
SERIAL_BUFFER = 100
BAUDRATE = 9600
XONXOFF = True # software flow control
RTSCTS = False # hardware flow control
TIMEOUT = 1
PARITY = serial.PARITY_EVEN
BYTESIZE=serial.SEVENBITS
STOPBITS=serial.STOPBITS_TWO

def openWf():
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLEWIDTH)
    wf.setframerate(RATE)
    return wf

def openDevFile():
    return open(DEV_FILENAME, 'wb')

def openHostFile():
    return open(HOST_FILENAME, 'wb')

def openDevSerial():
    return serial.Serial(port=DEV_NAME, baudrate=BAUDRATE, xonxoff=XONXOFF,
                         rtscts=RTSCTS, timeout=TIMEOUT, parity=PARITY,
                         bytesize=BYTESIZE, stopbits=STOPBITS)
def openHostSerial():
    serial.Serial(port=HOST_NAME, baudrate=BAUDRATE, xonxoff=XONXOFF,
                  rtscts=RTSCTS, timeout=TIMEOUT, parity=PARITY,
                  bytesize=BYTESIZE, stopbits=STOPBITS)
