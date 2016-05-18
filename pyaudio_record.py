#!/usr/bin/python

################################################################################
# pyaudio_record.py wavfilename
# Records audio from the microphone and saves it to the supplied wavefile
################################################################################

# http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed

import sys
import pyaudio
import wave
import time

CHUNK = 2**12
FORMAT=pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = str(sys.argv[1])

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE)

end_signal = 0

def callback(in_data, frame_count, time_info, status):
    global end_signal
    wf.writeframes(in_data)
    if(end_signal == 1):
        print("Done recording!")
        wf.close()
        exit()
    else:
        return(in_data, pyaudio.paContinue)

p=pyaudio.PyAudio()

print("Recording...")
inStream = p.open(format = FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK,
                  stream_callback=callback)

while not end_signal:
    try:
        continue
    except KeyboardInterrupt:
        end_signal = 1
