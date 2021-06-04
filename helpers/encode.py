import numpy as np
import copy
import time
import itertools


# here is the encoding matrix, which is a constant throughout the lifetime of the network. This is large enough for our network
G = np.identity(L)

G_rand_gen =  np.array([[   0.8040,    0.5490,    0.8470,    0.2480,    0.4620,    0.0460,    0.3410,    0.7130,    0.8330,    0.2930],
    [0.0060,    0.4840,    0.1450,    0.6400,    0.2560,    0.5430,    0.0780,    0.1070,    0.1740,    0.9260],
    [0.1340,    0.0800,    0.8780,    0.8180,    0.7260,    0.5680,    0.2040,    0.1080,    0.4140,    0.4250],
    [0.3150,    0.4430,    0.0430,    0.9820,    0.7290,    0.0430,    0.6500,    0.6790,    0.6380,    0.3060],
    [0.8450,    0.0150,    0.3120,    0.1750,    0.5040,    0.0080,    0.5400,    0.9570,    0.7490,    0.7280],
    [0.4980,    0.5450,    0.1480,    0.3950,    0.9650,    0.2660,    0.1340,    0.7110,    0.8380,    0.5720],
    [0.4250,    0.5850,    0.9620,    0.2380,    0.8990,    0.6980,    0.7050,    0.5740,    0.2350,    0.0340],
    [0.8180,    0.1660,    0.0870,    0.4850,    0.3200,    0.6930,    0.2430,    0.1510,    0.1050,    0.0980],
    [0.7010,    0.2450,    0.4630,    0.7500,    0.0090,    0.9160,    0.6800,    0.1140,    0.9910,    0.0390],
    [0.0800,    0.2630,    0.1380,    0.6720,    0.6310,    0.3870,    0.3230,    0.9810,    0.0690,    0.0540]])

G = np.vstack((G,G_rand_gen))
DECODE = {}
NUM_MACHINES = 4;

def decode(M, G):

    if option != 'Uncoded':
        decode_sets = [frozenset(a) for a in list(itertools.combinations(range(1,NUM_MACHINES+1),L))]

        for currentSet in decode_sets:
            setList = list(currentSet)
            setList.sort()
            machines = np.array(setList).astype(int)
            H = np.linalg.inv(G[machines-1,:])  
            DECODE[currentSet] = {}

            for i in range(L):
                DECODE[currentSet][machines[i]] = H[:,i]  
    return DECODE
