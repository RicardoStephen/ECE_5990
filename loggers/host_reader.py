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
host_name = '/dev/tty.usbserial-FT9AJZ8W'
num_chars = 100 # TODO
hostlogfile_name = 'log/host_log_' + str(int(time.time())) + '.txt'

# configuration
baudrate = 9600
xonxoff = True # software flow control
rtscts = False # hardware flow control
timeout = 1 # seconds

# initialize host
host_serial = serial.Serial(port=host_name, baudrate=baudrate, xonxoff=xonxoff,
                            rtscts=rtscts, timeout=timeout, parity=serial.PARITY_EVEN,
                            bytesize=serial.SEVENBITS,
                            stopbits=serial.STOPBITS_TWO)


# open file
hostlogfile = open(hostlogfile_name, 'wb')

# test device
try:
    data = '(RUB2.MIN)'
    host_serial.write(str.encode(data))
    print('Done writing\n')
except serial.SerialTimeoutException as ste:
    print(ste)

while True:
    try:
        buff = host_serial.read(num_chars)
        hostlogfile.write(buff)
        print(buff)
    except KeyboardInterrupt:
        host_serial.close()
        hostlogfile.close()
        print('Done')

