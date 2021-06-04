import numpy as np
import time

# this is not used in the current demo3.py. Instead, all helper methods are self contained in the main file.

def setUpDevices(g):

    time.sleep(0.1)
    return [1,2,3,4]

def createEncodingMatrix(maxdevices, threshold):
    return np.random.rand(threshold,threshold)

def getSpeed(deviceNumber):
    return 1

def powerIteration(devices, nIterations, s, runHetero):
    if(runHetero):
        time.sleep(np.random.normal(.196,.01))
    else:
        time.sleep(np.random.normal(1.05,.01))
    return 1

def generatePowerIterationData(n):
    return [1,2]
