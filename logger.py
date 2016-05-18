#!/usr/bin/python

import serial
import time
from log_init import *

# initialize files and ports
dev_file = openDevFile()
host_file = openHostFile()
dev_serial = openDevSerial()
host_serial = openHostSerial()

# Read from cnc mill for filename
printf('Reading from CNC mill\n')
flag = True
while flag:
    buff = dev_serial.read(num_chars)
    if(len(buff) > 0):
        print(buff)
        dev_file.write(buff)
        host_serial.write(buff)
        flag = False

# Forward instructions to mill
print('Forwarding instructions from CNC computer\n')
while not end_signal:
    try:
        buff = host_serial.read(num_chars)
        print(buff)
        host_file.write(buff)
        dev_serial.write(buff)
    except KeyboardInterrupt:
        dev_serial.close()
        host_serial.close()
        dev_file.close()
        host_file.close()
        exit()
