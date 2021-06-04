# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
import types
import threading
import sys
import numpy as np
from client import *
from server import *
# Add the folders above
sys.path.append('../')
#import node_client.py

# The max number of devices in the network
MAX_DEVICES = 6

# Enumerate the message types
from enum import IntEnum
class Message(IntEnum):
    PREEMPT = 1
    RESTART = 2
    MATRICES = 3
    PING = 4
    PONG = 5
    RESPONSE = 6

class Node:

    # Constructor
    def __init__(self):

        # Get the device's IP address.
        f = open("/opt/cec/ip.txt", "r")
        self._ipAddr = f.read().replace('\n','')
        
        # Get rid of the periods, cast to int
        #self._ipAddr = int(ipAddr.replace('.', ''))

        # Set a variable that will keep track of whether or not we have work to do
        self._matrixReady = False

        # Determine the node index based on the ip address.
        if(self._ipAddr == "10.0.0.97"):
            self._nodeID = 0; # desktop
        if(self._ipAddr == "10.0.0.176"):
            self._nodeID = 1;
        if(self._ipAddr == "10.0.0.159"):
            self._nodeID = 2;

        # This queue holds information that we need to send
        self._sendingQueue = queue.Queue(maxsize = 40)

        # hold the response data from one node
        self._responseData = np.empty(1, dtype=object)
        self._receivedResponse = np.zeros((6,1))

        # Signal a preempt
        self._preempted = False;
        self._quit = False;

        # Threads for sending and receiving information from the other nodes
        self._sendingThread = threading.Thread(target=self.sendingLoop, daemon=False)
        self._sendingThread.start()
        self._receivingThread = threading.Thread(target=self.receivingLoop, daemon=False)
        self._receivingThread.start()

        # Thread for doing the matrix multiplication work
        self._multThread = threading.Thread(target=self.multLoop, daemon=True)
        self._multThread.start()

        # The _partitions object keeps track of the partitions of the matrix.
        # Each element in the array corresponds to the index the partition ends on
        self._partitions = []

    def sendingLoop(self):
        while(not self._preempted):
            # if there is something to be sent, then send it
            if(not self._sendingQueue.empty()):
                print("Sending...")
                print("Time: " + str(time.time()))
                data = self._sendingQueue.get()
                if(not self._ipAddr == "10.0.0.97"):
                    client(data, "10.0.0.97")
            time.sleep(1)
        print("Sending thread exited successfully.")

    # These are the types of messages that could be sent and need to be handled:
        # Preempt
        # Restart
        # Matrices
        # ping
        # shut down?
    def receivingLoop(self):
        print("starting receiving loop")
        # this thread stays alive the whole time, even if preempted. 
        while(not self._quit):
            item = server(str(self._ipAddr))
            if(item.messageType == Message.PING):
                # Send a response to the master node
                print("Received a ping from master. Sending pong...")
                self._sendingQueue.put(types.SimpleNamespace(messageType = Message.PONG))
            elif(item.messageType == Message.PREEMPT):
                print("Received a preempt from master. Calling preempt..")
                self.preempt()
            elif(item.messageType == Message.RESTART):
                print("Received a restart command from master. Calling restart...")
                self.restart()
            elif(item.messageType == Message.MATRICES):
                print("Received matrix message.")
                print("Time: " + str(time.time()))

                print("Updating based on recieved information...")

                print("Shape of received item:")
                print(np.array(item.data).shape)
                print("Item:")
                print(item.data)
                self._x = item.data[:int(len(item.data)/2),:]
                self._matrix = item.data[int(len(item.data)/2):,:]
                self._matrixReady = True

            elif(item.messageType == Message.RESPONSE):
                print("Received response from worker.")
                print(item.data)
                self._responseData = item.data
                self._receivedResponse[item.deviceId] = 1
                time.sleep(1)
            else:
                print("WARNING: Received an unknown command from master node: " + str(item.messageType.name))

    def multLoop(self):
        while(not self._preempted):
            
            # Wait until there is a matrix to be multiplied.
            if(self._matrixReady):

                # Compute the matrix multiplication, then add it to the sending queue
                print(self._matrix.shape)
                print(self._x.shape)
                self._sendingQueue.put(types.SimpleNamespace(messageType=Message.RESPONSE, deviceId=self._nodeID, data=np.matmul(self._x,np.transpose(self._matrix))))
                print("Matrix multiplication complete.")
                print("Time: " +str(time.time()))
                self._matrixReady = False
            else:
                time.sleep(1)
        print("Matrix multiplication thread exited successfully.")

    # This script will take a matrix and divide it into n parts.
    # It will make the parts as evenly sized as possible while still maintaining the rows and columns.
    def matrixSplit(self, n):

        diff = 0
        fraction = len(self._matrix)/n
        self._partitions = []
        for i in range(0,n):
            split  = round(fraction + diff)
            self._partitions.append(split)
            diff = diff + fraction - split

        part = np.zeros(n)
        for i in range(0,n):
            part[i] = np.sum(self._partitions[:i+1])

        self._partitions = np.array(part, dtype=np.uint)
        newMatrix = np.array([], dtype=object)
        for i in range(0,len(self._partitions)):
            if(i==0):
                #print("index: " +str(self._partitions[i]))
                #print("sub matrix: " +str(self._matrix[:self._partitions[i]]))
                np.append(newMatrix, self._matrix[:self._partitions[i]])
            else:
                #print("index: " +str(self._partitions[i]))
                #print("sub matrix: " +str(self._matrix[self._partitions[i-1]:self._partitions[i]]))
                np.append(newMatrix, self._matrix[self._partitions[i-1]:self._partitions[i]])

        print("newmatrix:")
        print(newMatrix)

    def addMatrix(self, matrix):
        self._matrix = matrix


    # Matrix is the original data, partitioned into l partitions
    # where l is the recovery threshold, ie minimum number of machines
    # n is the number of machines to send to
    def distributeData(self,matrix,n):

        l = len(matrix)

        # generate a full rank matrix
        # l should always be less than or equal to n
        A = generateMatrixOfRank(l,n,l) 

        # For each machine in the system, send them their data, which is (matrix*dist_mat)[i] 
        # where i is the index of the machine
        
        result = np.matmul(matrix, dist_mat)
        for i in range(0, MAX_DEVICES):
            # send to device i result[i]
            i;

    # This function isn't being used right now, but it may be in use for milestone 2
    def generateMatrixOfRank(self,rows,columns,r):
        assert rows >= r and columns >= r

        # this is a python do while
        while(True):

            A = np.random.rand(rows,columns)
            if(np.linalg.matrix_rank(A) == r):
                break

        return A

    # Preempt this node
    def preempt(self):
        self._preempted = True
        print("Node preempted. Stopping sending and multiplying...")
        time.sleep(1)

    # Restart this node after preemption
    def restart(self):
        self._preempted = False

        print("Node restarted. Beginning sending and multiplying...")

        # Restart the stopped threads
        self._sendingThread = threading.Thread(target=self.sendingLoop, daemon=False)
        self._sendingThread.start()
        self._multThread = threading.Thread(target=self.multLoop, daemon=True)
        self._multThread.start()
        
    def quit(self):
        self._quit = True
        self._preempted = True
        time.sleep(1)



if (__name__ == "__main__"):
    node = Node()
    node.addMatrix(np.random.rand(20,20))
    node.matrixSplit(100)

