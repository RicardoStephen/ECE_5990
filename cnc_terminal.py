#!/usr/bin/python

################################################################################
# emulate.py
# 
# Note: Must configure parameters like filename and serial port in log_init.py
################################################################################

import serial
import time
#from log_init import *
DEV_NAME = '/dev/tty.usbserial-FT9AJZ8W'
# serial parameters
SERIAL_BUFFER = 100
BAUDRATE = 9600
XONXOFF = True # software flow control
RTSCTS = False # hardware flow control

TIMEOUT = 1
PARITY = serial.PARITY_EVEN
BYTESIZE=serial.SEVENBITS
STOPBITS=serial.STOPBITS_TWO
num_chars = 100
# initialize files and ports
#dev_file = openDevFile()
dev_serial = serial.Serial(port=DEV_NAME, baudrate=BAUDRATE, xonxoff=XONXOFF,
                         rtscts=RTSCTS, timeout=TIMEOUT, parity=PARITY,
                         bytesize=BYTESIZE, stopbits=STOPBITS, dsrdtr=True)
#dev_serial.dsrdtr = True
#dev_serial.setDSR(True)
print 'RI=%-5s - DSR=%-5s - CD=%-5s - CTS=%-5s' % (
            dev_serial.getRI(),
            dev_serial.dsrdtr,
            dev_serial.getCD(),
            dev_serial.getCTS(),
        )

# Read from cnc mill for filename
print('Reading from CNC mill\n')
flag = True
while flag:
    buff = dev_serial.read(num_chars)
    if(len(buff) > 0):
        print(buff)
        print('programs/'+buff[buff.find("(")+1:buff.find(")")])
        infile = open('programs/'+buff[buff.find("(")+1:buff.find(")")], 'r')
        #dev_file.write(buff)
        flag = False

# Send instructions to device
print("Sending instructions to device\n")
for line in infile:
    dev_serial.write(line)
infile.close()
print("Done sending instructions")
dev_serial.close()
