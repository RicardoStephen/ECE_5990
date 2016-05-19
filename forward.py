#!/usr/bin/python

################################################################################
# forward.py
# Forwards packets from the CNC computer to the CNC mill and starts the mike to
# record the resulting audio.
# Note: Must configure parameters like filename and serial port in log_init.py
################################################################################

import serial
import pyaudio
import wave
import time
from log_init import *
from spectrogram import generateSpecgram
from gcode_parser import parseFile
import pylab
import matplotlib.pyplot as plt

# initialize files and ports
wf = openWf()
dev_file = openDevFile()
host_file = openHostFile()
dev_serial = openDevSerial()
host_serial = openHostSerial()

# audio record callback
end_signal = False
audio_end = False
def callback(in_data, frame_count, time_info, status):
    global end_signal
    wf.writeframes(in_data)
    if end_signal:
        wf.close()
        inStream.close()
        audio_end = True
        return (in_data, pyaudio.paComplete)
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
        infile_name = buff[buff.find("(")+1:buff.find(")")]
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

while not audio_end:
    continue

# generate the spectrogram
generateSpecgram(WAVE_OUTPUT_FILENAME)

# generate the gcode plot
parseFile(HOST_FILENAME)

# wait for exit
while True:
    try:
        continue
    except KeyboardInterrupt:
        pylab.close('all')
        plt.close('all')
        exit()

