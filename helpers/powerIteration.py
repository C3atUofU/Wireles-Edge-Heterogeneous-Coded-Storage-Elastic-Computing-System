# Power iteration
# Author: MCG

import numpy as np

N_DEVICES = 1
RECOVERY_THRESHOLD = 1

# This function will do power iteration. It will call the functions in the Node class to perform the matrix multiplication.
def powerIteration(matrix, nIterations):
    v = np.random.rand(matrix.shape[1])

    for _ in range(nIterations):
        # Get the product using our algorithm
        tempVector = np.dot(matrix, v)

        norm = np.linalg.norm(tempVector)

        # decode the vector
        v = tempVector / norm
        print(v)

    return v

if(__name__ == "__main__"):
    v = powerIteration(np.array([[1, 2, 3],[1,4,9],[1,8,27]]),10)
    print("Final result: " + str(v))
