#!/usr/bin/python

import sys
from gcode_parser import parseFile
import matplotlib.pyplot as plt

parseFile(str(sys.argv[1]))

while True:
    try:
        continue
    except KeyboardInterrupt:
        plt.close('all')
        exit()
