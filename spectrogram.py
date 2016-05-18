#!/usr/bin/python

# http://dsp.stackexchange.com/questions/10743/generating-spectrograms-in-python-with-less-noise

import sys
from scipy.io import wavfile
import numpy as np
import pylab

fs,data = wavfile.read(str(sys.argv[1]))
channels = [np.array(data[:, 0]), np.array(data[:,1])]

Pxx, f, t, plot = pylab.specgram(
 channels[0],
 NFFT=4096,
 Fs=fs,
 detrend=pylab.detrend_none,
 window=pylab.window_hanning,
 noverlap=int(4096*0.5))
pylab.ylabel('Frequency [Hz]')
pylab.xlabel('Time [sec]')
pylab.title('Spectrogram of CNC Noise')
pylab.show()

while True:
 try:
  continue
 except KeyboardInterrupt:
  pylab.close('all')
  exit()
