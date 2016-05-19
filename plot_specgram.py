#!/usr/bin/python

################################################################################
# spectrogram.py wavfilename
# Generates a spectrogram with the given wav file
#
# Reference:
# http://dsp.stackexchange.com/questions/10743/generating-spectrograms-in-python-with-less-noise
################################################################################

import pylab
from spectrogram import generateSpecgram
import sys

print("Trying to generate the specgram.")
generateSpecgram(str(sys.argv[1]))

while True:
 try:
  continue
 except KeyboardInterrupt:
  pylab.close('all')
  exit()
