#!/usr/bin/python

################################################################################
# Filename: recompile.py
#
# Description:
# Recompiles the gcode program to reduce noise
################################################################################

import sys
from scipy.io import wavfile
import numpy as np
import pylab
import math

def unpickle(time_mapping_file):
  with open(time_mapping_file) as file:
    ret = []
    for line in file:
      s = line.split(",")
      ret.append((s[0], s[1], s[2], s[3]))
  return ret

def find_chatter(freq_power_map, frequencies, timestamps):
  ret = []
  freq_low = 1
  freq_high = 2500
  start_up_time = 20
 # print(freq_power_map)
 # print(len(timestamps))
  max_list = []
  for i in range(0, len(timestamps)):
    t = timestamps[i]
    #print(t)
    if(t > start_up_time):
      power_map = freq_power_map[i]
      #max_list.append(max(power_map))
      local_max_pwr  = 0
      local_max_freq = 0
      high_chatter_freq = 0
      #print(len(frequencies),len(power_map))
      for j in range(0, len(frequencies)):
        #if(local_max_list < power_map[j]):
         # local_max_list = power_map[j]
        if(frequencies[j] > freq_high):
          break
        if(frequencies[j] > freq_low):
          #print(frequencies[j],power_map[j])
          #print(local_max_list)
          if(local_max_pwr < power_map[j]):
            local_max_pwr = power_map[j]
            local_max_freq = frequencies[j]
          if(power_map[j] > 100):
            high_chatter_freq += 1
            
      if(high_chatter_freq >= 1):
        ret.append(t)
        #print(t)
  return ret

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
  temp = gcode_file_name.split(".min")
  temp = temp[0]+"_recompiled.min"
  new_gcode = open(temp, "w+")
  time_index = 0
  t = chatter_points[time_index]
  #print(chatter_points)
  #print(len(chatter_points))
  print("1.0 < 2.0", 1.0 < 2.0)
  for s, e, f, i in g_code:
    #print(t,float(s),float(e))
    print("t <=float(e))",float(t)<float(e))
    print("t >= float(s)", float(t)>float(s))
    while(t <= float(s) and time_index < len(chatter_points)):
      time_index += 1
      if(time_index < len(chatter_points)):
        t = chatter_points[time_index]
    if (float(t) >= float(s) and float(t) <= float(e)):
      new_feed = "F%d\r\n"%(int(math.floor(float(f)*0.5)))
      new_gcode.write(new_feed)
      time_index +=1
      print("Yo new time index")
    new_gcode.write(i)

  new_gcode.close()
recompile(str(sys.argv[1]),"chatter_test","gcode_time")
#unpickle("gcode_time")
