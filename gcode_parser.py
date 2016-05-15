#!/usr/bin/python
# This is the main gcode parser for the project.
# Rev. 1.0 will take in static Gcode files and parse them
# Rev. 2.0 will take in the Gcode dynamically via Serial
#


import sys, fileinput, math, re
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    #return math.hypot(plot_scale*(x2 - x1),plot_scale*(y2 - y1))
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
    print("A: (%f,%f)\tB: (%f,%f)\tC: (%f,%f)") % (A_X, A_Y, B_X, B_Y, C_X, C_Y)
    #CNC doesn't do 3D arcs
    a = calcDistance(B_X, B_Y, 0, C_X, C_Y, 0)
    b = calcDistance(A_X, A_Y, 0, C_X, C_Y, 0)
    c = calcDistance(A_X, A_Y, 0, B_X, B_Y, 0)
    #return cosine^-1(b^2+c^2-a^2/(2bc))
    print("A: %f B: %f C:%f") %(a,b,c)
    angle = math.acos((b*b+ b*b - a*a)/(2*b*b))
    if(point_over([B_X, B_Y], calc_line(C_X, C_Y, A_X, A_Y))):
        print("The point is over the line!!!!!!!\n\n")
        angle = 2*math.pi-angle
    #print("The Angle returned is: %f") %(angle)
    return (angle,angle*b)
def drawArc():
    global  globalX,  globalY, globalZ, globalI, globalJ, prevX, prevY
    #print("globalX: %f,  globalY:%f, globalZ:%f, globalI:%f, globalJ:%f, prevX:%f, prevY:%f") % (globalX,  globalY, globalZ, globalI, globalJ, prevX, prevY)
    center = [prevX + globalI, prevY+globalJ]
    radius = calcDistance(globalX, globalY, globalZ, prevX, prevY, prevZ)
    (angle, length) = law_of_cosines(center[0], center[1], globalX, globalY, prevX, prevY)
    #print("The Arc length is %f") % a
    #Slope is just really globalJ/globalY
    return (center, radius, angle, length)
def arc_patch(center, radius, theta1, theta2, ax=None, resolution=50, **kwargs):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    # generate the points
    theta = np.linspace(np.radians(theta1), np.radians(theta2), resolution)
    points = np.vstack((radius*np.cos(theta) + center[0],
                        radius*np.sin(theta) + center[1]))
    # build the polygon and add it to the axes
    poly = mpatches.Polygon(points.T, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly
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
        fig, ax = plt.subplots()
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
            time = 0
            local_feed = feedRate
            if(movementType == 'G02' or movementType == 'G2'):
                center, radius, angle, length = drawArc()
                distance = length
                arc_patch(center, radius, 180, 90, ax=ax, fill = 'false',color='green')
            elif(movementType == 'G03' or movementType == 'G3'):
                center, radius, angle, length = drawArc()
                distance = length
                arc1 = mpatches.Arc(center, math.fabs(prevX-globalX), math.fabs(prevY-globalY), math.degrees(angle), 90, 180, color='pink')
                ax.add_patch(arc1)
                #arc_patch(center, radius, 180, 90, ax=ax, fill = 'false',color='yellow')
                #arc_patch(center, radius, 0, 0, ax=ax, color='blue')
            elif(movementType == 'G00' or movementType == 'G0'):
                distance = calcDistance(globalX, globalY, globalZ, prevX, prevY, prevZ)
                line1 = [(prevX, prevY), (globalX, globalY)]
                (line1_xs, line1_ys) = zip(*line1)
                ax.add_line(plt.Line2D(line1_xs, line1_ys, linewidth=2, color='blue'))
                local_feed = rapid
            else:
                distance = calcDistance(globalX, globalY, globalZ, prevX, prevY, prevZ)
                line1 = [(prevX, prevY), (globalX, globalY)]
                (line1_xs, line1_ys) = zip(*line1)
                ax.add_line(plt.Line2D(line1_xs, line1_ys, linewidth=2, color='red'))
                #line = plt.Line2D((globalX, globalY), (prevX, prevY), lw=2.5)
                #plt.gca().add_line(line)
            if(prevTool != toolNum):
                total_time += toolChangeTime
                prevTool    = toolNum
            time  = calcTime(distance, local_feed)
            print("Distance: %f Time: %f") % (distance, time)
            total_time += time
            prevX = globalX
            prevY = globalY
            prevZ = globalZ



        print("Total Time: %f") % total_time
        plt.autoscale(True, True, True)
        plt.axis('scaled')
        plt.show()
            #CCW Arc: I,J are centerpoints, globalX, globalY are endpoints
parseFile(str(sys.argv[1]))

#turtle.done()


