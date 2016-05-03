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
device_name = '/dev/tty.usbserial-FT9AJZ83'
host_name = '/dev/tty.usbserial-FT9AJZ8W'
dev_filename = 'log/connect_dev_' + str(int(time.time())) + '.txt'
host_filename = 'log/connect_host_' + str(int(time.time())) + '.txt'
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
host_serial = serial.Serial(port=host_name, baudrate=baudrate, xonxoff=xonxoff,
                           rtscts=rtscts, timeout=timeout, parity=serial.PARITY_EVEN,
                           bytesize=serial.SEVENBITS,
                           stopbits=serial.STOPBITS_TWO)

# open file
dev_file = open(dev_filename, 'wb')
host_file = open(host_filename, 'wb')

# test device
flag = True
while flag:
    buffer = dev_serial.read(num_chars)
    if(len(buffer) > 0):
        print(buffer)
        dev_file.write(buffer)
        host_serial.write(buffer)
        flag = False

while True:
    try:
        print('From computer')
        buffer = host_serial.read(num_chars)
        print(buffer)
        host_file.write(buffer)
        dev_serial.write(buffer)
    except KeyboardInterrupt:
        dev_serial.close()
        host_serial.close()
        dev_file.close()
        host_file.close()
        print('Done')


