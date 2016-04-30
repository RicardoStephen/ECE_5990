#!/usr/local/bin/python3

################################################################################
# Filename: host_logger.py
#
# Description:
# Opens the host port and writes data to it from a log file. Then, reads from
# the host port and stores in data in another log file.
################################################################################

import serial
import time

# test parameters
host_name = '/dev/cu.usbserial'
devlogfile_name = 'log/dev_log_TODO.txt' # TODO
hostlogfile_name = 'log/host_log_' + time.time() + '.txt'
num_chars = 100

# configuration
baudrate = 115200
xonxoff = False # software flow control
rtscts = False # hardware flow control
timeout = 1 # seconds

# initialize host
try:
    host_serial = serial.Serial(port=host_name, baudrate=baudrate, xonxoff=xonxoff,
                                rtscts=rtscts, timeout=timeout)
except serial.SerialException as se:
    print(se)
    exit()

# open file
devlogfile = open(devlogfile_name, 'r')
hostlogfile = open(hostlogfile_name, 'a')

# test device
data = devlogfile.read()
try:
    host_serial.write(data)
except serial.SerialTimeoutException as ste:
    print(ste)

while True:
    try:
        buff = host_serial.read(num_chars)
        hostlogfile.write(buff)
        print(buff)
    except KeyboardInterrupt:
        host_serial.close()
        devlogfile.close()
        hostlogfile.close()
        print('DONE')

