#!/usr/bin/python
# This is the main gcode parser for the project.
# Rev. 1.0 will take in static Gcode files and parse them
# Rev. 2.0 will take in the Gcode dynamically via Serial
#


import sys, fileinput, math, re
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import cm, colors, patches


prevX          = float(0.0)
prevY          = float(0.0)
prevZ          = float(0.0)
globalX        = float(0.0)
globalY        = float(0.0)
globalZ        = float(0.0)
globalI        = float(0.0)
globalJ        = float(0.0)
feedRate       = 0
spindleSpeed   = 0
toolNum        = 19
toolSize       = 0
rapid          = 100
toolChangeTime = 5/60
def parseM(line, index):
    index += 1
    return index

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
movementType = ''

def parseLine(line):
    i = 0
    while( i < len(line)):
        #print("This is the index Value: %d\n") % i
        a = str(line[i][0]).split()[0]
        #print("a: %s\n") % a
        if( a in validCmds):
            #print("Is a valid cmd: %s\n") % a
            i = validCmds[a](line,i)
        elif( a[0] in validDirections and re.match(r"^([-]?\d+\.?\d+)$",line[i][1:]) is not None):
            i = validGCmds[movementType](line,i)
        else:
            i += 1
plot_scale = 1

def calc_line(x1, y1, x2, y2):
    if(x2 - x1 == 0):
        slope = float("inf")
    else:
        slope = (y2-y1)/(x2-x1)
    intercept = y2 - slope*x2
    return (slope, intercept)
    
#returns the distance between point 1 and point 2
def calcDistance(x1, y1, z1, x2, y2, z2):
    global plot_scale
    return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def calcTime(distance, feedRate):
    if(feedRate == 0):
        return 0
    return distance/feedRate

def point_under(point, line):
    slope, intercept = line
    if(slope != float("inf")):
        return point[0]*slope + intercept > point[1]
    else:
        return point[0] < intercept

def point_over(point, line):
    slope, intercept = line
    if(slope != float("inf")):
        return point[0]*slope + intercept < point[1]
    else:
        return point[0] > intercept

def law_of_cosines(A_X, A_Y, B_X, B_Y, C_X, C_Y):
    #CNC doesn't do 3D arcs
    a = calcDistance(B_X, B_Y, 0, C_X, C_Y, 0)
    b = calcDistance(A_X, A_Y, 0, C_X, C_Y, 0)
    c = calcDistance(A_X, A_Y, 0, B_X, B_Y, 0)
    angle = math.acos((b*b+ b*b - a*a)/(2*b*b))
    if(point_over([B_X, B_Y], calc_line(C_X, C_Y, A_X, A_Y))):
        angle = 2*math.pi-angle
    return (angle,angle*b)

def drawArc():
    global  globalX,  globalY, globalZ, globalI, globalJ, prevX, prevY
    center = [prevX + globalI, prevY+globalJ]
    radius = calcDistance(globalX, globalY, globalZ, center[0], center[1], prevZ)
    (angle, length) = law_of_cosines(center[0], center[1], globalX, globalY, prevX, prevY)
    #Slope is just really globalJ/globalY
    return (center, radius, angle, length)

def parseFile(fileName):
    with open(fileName) as file:
        global plot_scale
        global  globalX,  globalY, globalZ, globalI, globalJ, feedRate, spindleSpeed, toolNum, toolSize, rapid
        global prevX, prevY, prevZ
        total_time = 0
        lineNum    = 0
        text       = ''
        count      = 0
        add        = ''
        prevTool   = 19
        first_time = 1
        arcs       = []
        lines      = []
        fig = plt.figure()
        ax = p3.Axes3D(fig)
        for line in file:
            lineNum  += 1
            gcode     = line.upper().split()
            parseLine(gcode)
            time       = 0
            local_feed = feedRate
            distance   = 0
            if(movementType == 'G02' or movementType == 'G2'):
                center, radius, angle, length = drawArc()
                distance                      = length
                arcs.append(((globalX,globalY,globalZ),(prevX,prevY,prevZ),radius))
            elif(movementType == 'G03' or movementType == 'G3'):
                center, radius, angle, length = drawArc()
                distance                      = length
                arcs.append(((prevX,prevY,prevZ),(globalX, globalY, globalZ), radius))
            elif(movementType == 'G00' or movementType == 'G0'):
                distance = calcDistance(globalX, globalY, globalZ, prevX, prevY, prevZ)
                lines.append(((prevX, prevY, prevZ), (globalX, globalY, globalZ)))
                local_feed = rapid
                line1 = [(prevX, prevY), (globalX, globalY)]
                (line1_xs, line1_ys) = zip(*line1)
                if(first_time == 0):
                    ax.plot((prevX, globalX), (prevY, globalY), (prevZ, globalZ))
                else:
                    first_time -= 1
            elif(movementType == 'G01' or movementType == 'G1'):
                distance = calcDistance(globalX, globalY, globalZ, prevX, prevY, prevZ)
                lines.append(((prevX, prevY, prevZ), (globalX, globalY, globalZ)))
                line1 = [(prevX, prevY), (globalX, globalY)]
                (line1_xs, line1_ys) = zip(*line1)
                if(first_time == 0):
                    ax.plot((prevX, globalX), (prevY, globalY), (prevZ, globalZ))
                else:
                    first_time -= 1
            if(prevTool != toolNum):
                total_time += toolChangeTime
                prevTool    = toolNum
            time  = calcTime(distance, local_feed)
            total_time += time
            prevX = globalX
            prevY = globalY
            prevZ = globalZ

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Test')

        plt.show()
parseFile(str(sys.argv[1]))
