#!/usr/bin/python
# This is the main gcode parser for the project.
# Rev. 1.0 will take in static Gcode files and parse them
# Rev. 2.0 will take in the Gcode dynamically via Serial
#


import sys, fileinput, math, re, turtle

prevX        = float(0.0)
prevY        = float(0.0)
prevZ        = float(0.0)
globalX      = float(0.0)
globalY      = float(0.0)
globalZ      = float(0.0)
globalI      = float(0.0)
globalJ      = float(0.0)
feedRate     = 0
spindleSpeed = 0
toolNum      = 0
toolSize     = 0
def parseM(line, index):
    index += 1
    return index
    '''
    #print("Found a valid G cmd: %s. Index: %d\n") % (line, index)
    if(not line[index][0] == 'M'):
        exit(1)
    index += 1
    if(line[index-1] in validMCmds):
        index = validMCmds[line[index-1]](line, index)
    return index
    '''
def parseX(line, index):
    global globalX
    if(not line[index][0] == 'X'):
        exit(1)
    prevX = globalX
    globalX = float(line[index][1:])
    #print("Parsing X: %f\n") % globalX
    index += 1
    return index

def parseY(line, index):
    global globalY
    if(not line[index][0] == 'Y'):
        exit(1)
    prevY = globalY
    globalY = float(line[index][1:])
    #print("Parsing Y: %f\n") % globalY
    index += 1
    return index

def parseZ(line, index):
    global globalZ
    if(not line[index][0] == 'Z'):
        exit(1)
    prevZ = globalZ
    globalZ = float(line[index][1:])
    #print("Parsing Z: %f\n") % globalZ
    index += 1
    return index

def parseI(line, index):
    global globalI
    if(not line[index][0] == 'I'):
        exit(1)
    globalI = float(line[index][1:])
    #print("Parsing Z: %f\n") % globalZ
    index += 1
    return index
def parseJ(line, index):
    global globalJ
    if(not line[index][0] == 'J'):
        exit(1)
    globalJ = float(line[index][1:])
    #print("Parsing Z: %f\n") % globalZ
    index += 1
    return index

def parseG0(line, index):
    #print("Parsing a g0. Here is the line:%s. Index: %d\n") % (line, index)
    while(index < len(line) and not (line[index] in validCmds)):
        index = validDirections[line[index][0]](line, index)
    return index


def parseG1(line, index):
    #print("Parsing a g1. Here is the line:%s. Index: %d\n") % (line, index)
    while(index < len(line) and not (line[index][0] in validCmds)):
        index = validDirections[line[index][0]](line, index)
    return index

#Circular Move CCW
def parseG2(line, index):
    while(index < len(line) and not (line[index][0] in validCmds)):
        index = validDirections[line[index][0]](line, index)
    return index
#Circular Move CW: IJ=centerpoint, XY = endpoints
def parseG3(line, index):
    while(index < len(line) and not (line[index][0] in validCmds)):
        index = validDirections[line[index][0]](line, index)
    return index

def parseG(line, index):
    global movementType
    #print("Found a valid G cmd: %s. Index: %d\n") % (line, index)
    if(not line[index][0] == 'G'):
        exit(1)
    index += 1
    if(line[index-1] in validGCmds):
        movementType = line[index-1]
        index = validGCmds[line[index-1]](line, index)
    return index

def parseT(line, index):
    global toolNum
    if(not line[index][0] == 'T'):
        exit(1)
    if(len(line[index]) == 1):
        toolNum = int(line[index+1])
        index += 2
    else:
        toolNum = int(line[index][1:])
        index += 1
    return index
#assume its in the format for now: S#####
def parseSpindle(line, index):
    global spindleSpeed
    #print("Found a valid spindle: Here is the line: %s\n") % line
    #If this happens, throw an error
    if(not line[index][0] == 'S'):
        exit(1)
    if(len(line[index]) == 1):
        spindleSpeed = int(line[index+1])
        index += 2
    else:
        spindleSpeed = int(line[index][1:])
        index += 1
    #print("Here is the new spindleSpeed: %s\n") % spindleSpeed
    return index

def parseFeed(line, index):
    global feedRate
    #print("Found a valid feedRate: Here is the line: %s\n") % line
    if(not line[index][0] == 'F'):
        exit(1)
    if(len(line[index]) == 1):
        feedRate = float(line[index+1])
        index += 2
    else:
        feedRate = float(line[index][1:])
        index += 1
    return index

def parseComment(line, index):
    #print("Found a comment: %s\n") % line[index:]
    i = index
    while ( i < len(line)):
        i += 1
        if ')' in line[i-1]:
            #print("Found end of the comment: %s\n") % line[i-1]
            return i
validCmds       = {'G':parseG, 'M':parseM, 'T':parseT, 'S':parseSpindle, 'F':parseFeed,
            '(': parseComment}
validDirections = {'X': parseX, 'Y':parseY, 'Z': parseZ, 'I': parseI, 'J':parseJ}
validGCmds      = {  'G00':parseG0, 'G0': parseG0,
                'G01':parseG1, 'G1':parseG1,
                'G02':parseG2, 'G2':parseG2,
                'G03':parseG3, 'G3':parseG3}
'''
validMCmds      = {  'M03':parseM3, 'M3': parseM3,
                'M05':parseM5, 'M5':parseM5,
                'M06':parseM6, 'M6':parseM6,
                'M08':parseM8, 'M8':parseM8}
'''

#Movement Type:
#Sticks with whatever the last movement type was
#So if the last command to specify movement was g1
#Then an X____Y____ will really mean: G1 X______Y_____
movementType = 'G00'

def parseLine(line):
    i = 0
    while( i < len(line)):
        #print("This is the index Value: %d\n") % i
        a = str(line[i][0]).split()[0]
        print("a: %s\n") % a
        if( a in validCmds):
            #print("Is a valid cmd: %s\n") % a
            i = validCmds[a](line,i)
        elif( a[0] in validDirections and re.match(r"^([-]?\d+\.?\d+)$",line[i][1:]) is not None):
            i = validGCmds[movementType](line,i)
        else:
            i += 1
plot_scale = 100
#returns the distance between point 1 and point 2
def calcDistance(x1, y1, x2, y2):
    global plot_scale
    return math.hypot(plot_scale*(x2 - x1),plot_scale*(y2 - y1))
def calcExtent(pt1, pt2):
    radius
def drawArc(dir):
    radius = calcDistance(globalX, globalY, globalI, globalJ)
    print("Radius is: %d. Stating points are: %d,%d. End points are: %d, %d") % (radius, prevX, prevY, globalX, globalY)
    distancePoints = calcDistance(prevX, prevY, globalX, globalY)
    a = math.degrees(math.acos((2*(radius**2) - distancePoints**2)/(2*(radius**2))))
    if(dir == 1):
        turtle.circle(radius, a, 10)
    else:
        turtle.circle(radius, -a, 10)
def parseFile(fileName):
    with open(fileName) as file:
        global plot_scale
        lineNum = 0
        text=''
        count=0
        add=''
        for line in file:
            lineNum += 1
            gcode = line.upper().split()
            parseLine(gcode)
            if( lineNum == 20):
                print("\n\nTrying to match the z thing.\n\n")
            print("%d. Line: %s\n") % (lineNum, gcode)
            print("FeedRate: %d\t Spindle Speed: %d\t Tool Number:%d MovementType: %s\n") % (feedRate, spindleSpeed, toolNum, movementType)
            print("(%f,%f) (I,J)\n") %(globalI, globalJ)
            print("Location: (%f,%f,%f)\n") % (globalX, globalY, globalZ)
            #CCW Arc: I,J are centerpoints, globalX, globalY are endpoints
            '''
            if(movementType == 'G02' or movementType == 'G2'):
                #drawArc(1)
            elif(movementType == 'G03' or movementType == 'G3'):
                #drawArc(0)
            else:
                #turtle.goto(plot_scale*globalX, plot_scale*globalY)
            '''
parseFile(str(sys.argv[1]))
#turtle.done()


