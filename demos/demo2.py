import numpy as np
import threading
import concurrent.futures
import copy
import time
import itertools
import sys

def powerIteration(matrix, vector, nIterations):
    v = np.random.rand(matrix.shape[1])

    for _ in range(nIterations):
        # Get the product using our algorithm
        tempVector = np.dot(matrix, v)

        norm = np.linalg.norm(tempVector)

        # decode the vector
        v = tempVector / norm
        print(v)

    return v

def slowMatrixMult(matrix, vector, speedFactor):
    assert speedFactor > 0
    assert speedFactor <=1

    # start a timer
    start = time.time()

    result = np.matmul(matrix,vector)

    # end the timer
    end = time.time()

    # calculate the time taken
    worktime = end - start

    # sleep some time to simulate the difference in computation power
    sleepTime = worktime * (1/speedFactor - 1)
    time.sleep(sleepTime)
    print("slept " + str(sleepTime) + " seconds")

    return result

def main(): # use: python3 milestone2Demo.py <matrix X> <number of machines P> <recovery threshold L> <predetermined generator matix G> <sequence of intput vecots w_t>
    
    # parse command line inputs
    #if(len(sys.argv) != 6):
        #print("Use: python3 milestone2Demo.py")
        #print("\t<matrix X>")
        #print("\t<number of machines P>")
        #print("\t<recovery threshold L>")
        #print("\t<predetermined generator matrix G>")
        #print("\t<sequence of input vectors w_t>")
        #exit()

    #X = sys.argv[1]
    #P = sys.argv[2]
    #L = sys.argv[3]
    #G = sys.argv[4]
    #w_t = sys.argv[5]

    #X = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1],[0,0,0],[1,2,1]]) # 9x3 matrix
    #w = np.array([[1],[2],[3]]) # 3x1 vector
    #P = 3
    #P_max = 3
    #L = 3
    #G = np.array(   [[ 1, 0, 0],
                     #[ 1, 2, 3],
                     #[ 1, 4, 9]])

    #print("Decoded matrix: " + str(decoded))

    #print("Result from basic multiplication: " + str(np.matmul(X,w)))

    input("\tPress enter when you are ready to run power iteration.")

    # Run the program with encoding
    print("3 nodes with encoding:")

    X = np.random.rand(4800,4800)
    w = np.random.rand(X.shape[1])
    P = 3
    L = 3
    G = np.random.rand(1600,1600)
    G_inv = np.linalg.inv(G)
    X_part = np.array([X[i:i+int(len(X)/L),:] for i in range(0,len(X), int(len(X)/L))])
    X_coded = np.zeros(X_part.shape)  # same shape as before
    # Code the x values using the G matrix
    for s in range(0,P):
        for k in range(0,L):
            X_coded[s] += G[s,k] * X_part[k]
    startTime = time.time()
    for i in range(100):

        # online computation, including multiplication
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(np.matmul, xpart, w) for xpart in X_coded]

        # gather all the vectors
        gathered = np.array([np.transpose(f.result()) for f in futures])
        concat = np.array(np.concatenate(gathered)).flatten()

        # Decode the matrix to obtain the result
        decoded = np.matmul(gathered, np.transpose(G_inv))

    endTime = time.time()
    totalTime2 = endTime - startTime
    print("\tTotal time: " + str(endTime - startTime))
    print("Percent of total uncoded version: " +str(totalTime2/totalTime1))

if __name__ == "__main__":
    main()
