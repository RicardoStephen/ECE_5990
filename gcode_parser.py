#!/usr/bin/python
# This is the main gcode parser for the project.
# Rev. 1.0 will take in static Gcode files and parse them
# Rev. 2.0 will take in the Gcode dynamically via Serial
#


import sys, fileinput, math

globalX      = 0
globalY      = 0
globalZ      = 0
feedRate     = 0
spindleSpeed = 0
toolNum      = 0
toolSize     = 0
def parseM(line, index):
    #print("Found a valid m: Here is the line: %s\n") % line
    index += 1
    return index
def parseG(line, index):
    print("Found a valid G cmd: Here is the line: %s\n") % line
    index += 1
    return index

def parseT(line, index):
    toolNum = line[1:]
    index += 1
    return index
#assume its in the format for now: S#####
def parseSpindle(line, index):
    #print("Found a valid spindle: Here is the line: %s\n") % line

    #If this happens, throw an error
    if(not line[index][0] == 'S'):
        exit(1)
    if(len(line[index]) == 1):
        spindleSpeed = line[index+1]
        index += 2
    else:
        spindleSpeed = line[index][1:]
        index += 1
    print("Here is the new spindleSpeed: %s\n") % spindleSpeed
    return index
def parseFeed(line, index):
    #print("Found a valid feedRate: Here is the line: %s\n") % line
    if(not line[index][0] == 'F'):
        exit(1)
    if(len(line[index]) == 1):
        feedRate = line[index+1]
        index += 2
    else:
        feedRate = line[index][1:]
        index += 1
    print("Here is the new feedrate: %s\n") % feedRate
    return index

def parseComment(line, index):
    #print("Found a comment: %s\n") % line[index:]
    i = index
    while ( i < len(line)):
        i += 1
        if ')' in line[i-1]:
            #print("Found end of the comment: %s\n") % line[i-1]
            return i
validCmds = {'G':parseG, 'M':parseM, 'T':parseT, 'S':parseSpindle, 'F':parseFeed, '(': parseComment}
#Movement Type:
#Sticks with whatever the last movement type was
#So if the last command to specify movement was g1
#Then an X____Y____ will really mean: G1 X______Y_____
movementType = 0


def parseLine(line):
    i = 0
    while( i < len(line)):
        #print("This is the index Value: %d\n") % i
        a = str(line[i][0]).split()[0]
        if( a in validCmds):
            #print("Is a valid cmd: %s\n") % a
            i = validCmds[a](line,i)
        else:
            i += 1




def parseFile(fileName):
    with open(fileName) as file:
        text=''
        count=0
        add=''
        for line in file:
            gcode = line.split()
            parseLine(gcode)

parseFile(str(sys.argv[1]))


