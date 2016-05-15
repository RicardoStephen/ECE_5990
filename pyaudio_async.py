#!/usr/local/bin/python3

# http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed

import pyaudio
import wave
import time

CHUNK = 2**12
FORMAT=pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
TIMESTAMP = str(int(time.time()))
WAVE_OUTPUT_FILENAME = "audio/async"+TIMESTAMP+".wav"

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE)

end_signal = 0

def callback(in_data, frame_count, time_info, status):
    global end_signal
    print("Callback")
    wf.writeframes(in_data)
    if(end_signal == 1):
        wf.close()
        exit()
    else:
        return(in_data, pyaudio.paContinue)

p=pyaudio.PyAudio()

inStream = p.open(format = FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK,
                  stream_callback=callback)

while True:
    try:
        continue
    except KeyboardInterrupt:
        end_signal = 1
