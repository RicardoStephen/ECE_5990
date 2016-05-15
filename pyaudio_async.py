# http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed

import pyaudio
import wave
import time

CHUNK = 2**12
FORMAT=pyaudio.paInt16
CHANNELS = 1
RATE = 2000
RECORD_SECONDS = 5
TIMESTAMP = str(int(time.time()))
WAVE_OUTPUT_FILENAME = "audio/async"+TIMESTAMP+".wav"

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE)

def callback(in_data, frame_count, time_info, status):
    print("callback")
    wf.writeframes(in_data)
    return(None, pyaudio.paContinue)

p=pyaudio.PyAudio()


inStream = p.open(format = FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK,
                  stream_callback=callback)

while True:
    try:
        continue
    except KeyboardInterrupt:
        wf.close()
        exit()



# def callback(in_data, frame_count, time_info, status):
#     print "callback"
#     audio = numpy.fromstring(in_data, dtype=numpy.int16)

#     return (audio, pyaudio.paContinue)

# p=pyaudio.PyAudio()


# inStream = p.open(format = FORMAT,
#                   channels=CHANNELS,
#                   rate=RATE,
#                   input=True,
#                   frames_per_buffer=CHUNK,
#                   stream_callback=callback)

# audio = numpy.empty((RATE / CHUNK * RECORD_SECONDS), dtype="int16")
# inStream.start_stream()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

# while True:
#     try:
#         1 + 1
#     except KeyboardInterrupt:
#         self.in
