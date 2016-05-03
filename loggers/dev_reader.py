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
device_name = '/dev/tty.usbserial-FT9AJZ8W'
logfile_name = 'log/dev_log_' + str(int(time.time())) + '.txt'
num_chars = 100

# configuration
baudrate = 9600
xonxoff = True # software flow control
rtscts = False # hardware flow control
timeout = 1 # seconds

# initialize host
dev_serial = serial.Serial(port=device_name, baudrate=baudrate, xonxoff=xonxoff,
                           rtscts=rtscts, timeout=timeout, parity=serial.PARITY_EVEN,
                           bytesize=serial.SEVENBITS,
                           stopbits=serial.STOPBITS_TWO)

# open file
logfile = open(logfile_name, 'wb')

# test device
while True:
    try:
        buff = dev_serial.read(num_chars)
        print(buff)
        logfile.write(buff)
    except KeyboardInterrupt:
        dev_serial.close()
        logfile.close()
        print('Done')


