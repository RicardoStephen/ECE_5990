#!/usr/bin/python

import serial
import pyaudio
import wave
import time
from log_init import *

# initialize files and ports
wf = openWf()
dev_file = openDevFile()
host_file = openHostFile()
dev_serial = openDevSerial()
host_serial = openHostSerial()

# audio record callback
end_signal = False
def callback(in_data, frame_count, time_info, status):
    global end_signal
    wf.writeframes(in_data)
    if end_signal:
        wf.close()
        print('Done')
        exit()
    else:
        return(in_data, pyaudio.paContinue)

p=pyaudio.PyAudio()

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

# Start recording audio
print('Starting to record audio')
inStream = p.open(format = FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output = True,
                  frames_per_buffer=CHUNK,
                  stream_callback=callback)
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
        end_signal = True
