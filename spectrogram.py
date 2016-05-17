# http://dsp.stackexchange.com/questions/10743/generating-spectrograms-in-python-with-less-noise

import scipy.io
import numpy as np
import pylab

fs,data=wavfile.read('audio/test2.wav')
channels = [np.array(data[:, 0]), np.array(data[:,1])]

Pxx, f, t, plot = pylab.specgram(
 channels[0],
 NFFT=4096,
 Fs=fs,
 detrend=pylab.detrend_none,
 window=pylab.window_hanning,
 noverlap=int(4096*0.5))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

while True:
 try:
  continue
 except KeyboardInterrupt:
  exit()

