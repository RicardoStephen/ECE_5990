#!/usr/bin/python

import serial
import pyaudio
import wave
import time
from log_init import *

# initialize files and ports
wf = openWf()
dev_file = openDevFile()
dev_serial = openDevSerial()

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
        infile = open('programs/'+buff[buff.find("(")+1:buff.find(")")], 'wb')
        dev_file.write(buff)
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
# Send instructions to device
print("Sending instructions to device\n")
for line in infile:
    dev_serial.write(line)
infile.close()
print("Done sending instructions")
# wait for exit
while not end_signal:
    try:
        continue
    except KeyboardInterrupt:
        dev_serial.close()
        end_sidgnal = True
