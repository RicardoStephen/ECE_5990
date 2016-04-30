#!/usr/local/bin/python3

################################################################################
# Filename: dev_logger.py
#
# Description:
# Opens the device serial port and logs any data collected from it.
################################################################################

import serial
import time

# test parameters
device_name = '/dev/cu.usbserial'
logfile_name = 'log/dev_log_' + time.time() + '.txt'
num_chars = 100

# configuration
baudrate = 115200
xonxoff = False # software flow control
rtscts = False # hardware flow control
timeout = 1 # seconds

# initialize host
try:
    dev_serial = serial.Serial(port=device_name, baudrate=baudrate, xonxoff=xonxoff,
                                rtscts=rtscts, timeout=timeout)
except serial.SerialException as se:
    print(se)
    exit()

# open file
logfile = open(logfile_name, 'a')

# test device
while True:
    try:
        buff = dev_serial.read(num_chars)
        logfile.write(buff)
        print(buff)
    except KeyboardInterrupt:
        dev_serial.close()
        logfile.close()
        print('DONE')


