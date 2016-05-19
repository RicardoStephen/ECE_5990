# ECE_5990
ECE 5990 Final Project

Known Issues
  -Gcode Parsing
    -Does not handle M commands yet
    -Cannot handle the filename in the actual gcode program:
      ex) I$ FSOP2.min % will result in an error b/c the parser interprets the 'F' as a feedrate cmd