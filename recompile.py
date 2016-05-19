#!/usr/bin/python

################################################################################
# Filename: recompile.py
#
# Description:
# Recompiles the gcode program to reduce noise
################################################################################

from scipy.io import wavfile
import numpy as np
import pylab

def unpickle(time_mapping_file):
  with open(time_mapping_file) as file:
    ret = []
    for line in file:
      s = line.split(",")
      ret.append((s[0], s[1], s[2], s[3]))
    print(ret)
  return ret
def find_chatter(freq_power_map, frequencies, timestamps):
  ret = []
  freq_low = 1
  freq_high = 2000
  for i in range(0, len(timestamps)):
    t = timestamps[i]
    if(t > 0.5):
      power_map = freq_power_map[i]
      high_chatter_freq = 0
      for j in range(0, len(frequencies)):
        if(frequencies[j] > freq_high):
          break
        if(frequencies[j] > freq_low):
          if(power_map[j] > 150):
            #print(power_map[j])
            #print("Found some high frequencies",power_map[i],frequencies[i])
            high_chatter_freq += 1
      if(high_chatter_freq >= 5):
        ret.append(t)
        print("Adding new timestamp to high_freq chart:",t)
        print("high chatter_freq:",high_chatter_freq)
  return ret
#def corrrespond_instruction_to_timestamp()

def recompile(wav_file_name, gcode_file_name, time_mapping_file):
  #Start stepping through the wave Filename
  #Can you identify times when the noise is above a certian threshold in
  #the audio_recording file

  #time_mapping_file will basically be the timestamp->gcode mapping
  #g_code_file format is list containing (time_start, time_end, instruction, feedRate)
  g_code  = unpickle(time_mapping_file)
  fs,data = wavfile.read(wav_file_name)
  Pxx, f, t, plot = pylab.specgram(
    data,
    NFFT=4096,
    Fs=fs,
    detrend=pylab.detrend_none,
    window=pylab.window_hanning,
    noverlap=int(4096*0.5))
  #chatter_points contains a list of time_stamps that relate to the chatter heard
  chatter_points = find_chatter(Pxx, f, t)
  for t in chatter_points:
    for s, e, i, f in g_code:
      print(s,e,i)
      if( t >=float(s) and t <= float(e)):
        print("Should modify this instruction:",i,f)
        print("New feedRate:",f*0.5)
        print("Index of the instruction", g_code.index((s,e,i,f)))


recompile("audio/demo.wav","fake","gcode_time")
#unpickle("gcode_time")
