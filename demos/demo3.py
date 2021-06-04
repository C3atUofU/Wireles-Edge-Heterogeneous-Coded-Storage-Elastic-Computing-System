import numpy as np
import matplotlib.pyplot as plt
import time
import csv

TARGET_ACCURACY = 1e-8

DEVICE_SPEEDS =  [0.035, 0.035, 0.149, 0.149]

def power_iteration(A, actual, computationSpeed):
    # Ideally choose a random vector
    # To decrease the chance that our vector
    # Is orthogonal to the eigenvector
    b_k = np.random.rand(A.shape[1])

    i = 0;
    accuracy = []
    t_a = []
    tz = time.time()
    while abs(getEigenval(b_k,A)-actual) > TARGET_ACCURACY:
        start = time.time()
        # calculate the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)

        # calculate the norm
        b_k1_norm = np.linalg.norm(b_k1)

        # re normalize the vector
        b_k = b_k1 / b_k1_norm
        i = i+1
        accuracy.append(abs(getEigenval(b_k,A)-actual))
        t_a.append(time.time() - tz)
        end = time.time()
        worktime = end - start
        sleepTime = worktime * (1/computationSpeed - 1)
        time.sleep(sleepTime)

    print("Number of iterations: " + str(i))
    print("Actual:     " +str(actual))
    print("Calculated: " +str(getEigenval(b_k,A)))
    return accuracy, t_a

def getEigenval(x, M):
    # use the Rayleigh quotient to get the eigenvalue of a given vector and matrix
    return (np.matmul(np.transpose(x),np.matmul(M,x))) / (np.matmul(np.transpose(x),x))

def randomInvertibleMatrix(size):
    tolerance = 1e-12
    while True:
        A = np.random.rand(size,size)
        B = np.matmul(A, np.transpose(A))
        error = abs(np.matmul(B,np.linalg.inv(B)) - np.identity(size))
        if all(x < tolerance for row in error for x in row):
            return B

# Inputs: 
    # matrix A
    # actual max eigenval x
    # number of pi 4s n4 
    # number of pi 3s n3
    # whether to use encoding scheme encodingScheme
def runPowerIteration(A, x, n3, n4, encodingScheme=False):

    if n3 == 2 and n4 == 0:
        return compute(A, x, DEVICE_SPEEDS[0]/.5)
    if n3 ==2 and n4 == 2 and not encodingScheme:
        return compute(A, x, DEVICE_SPEEDS[0]/.25)
    if n3 == 0 and n4 == 2:
        return compute(A, x, DEVICE_SPEEDS[3]/.5)
    if n3 == 2 and n4== 2 and encodingScheme:
        return compute(A, x, DEVICE_SPEEDS[0]/.095)

def myAdd(a,b):
    if len(a) > len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b

    return c

def main():
    n = 125

    # generate eigenvalues and vectors
    # we know the eigenvalues and vectors of the matrix we will be using
    # because we generate the matrix using them
    # this is done so that we have an absolute accuracy metric

    # contains eigenvectors
    V = randomInvertibleMatrix(n)

    # contains eigenvals
    D = np.zeros((n,n))
    eigenMax = 0.0
    for i in range(n):
        for j in range(n):
            if i == j:
                D[i,j] = np.random.rand()
                if D[i,j] > eigenMax:
                    eigenMax = D[i,j]
    
    # construct the matrix M
    M = np.matmul(V, np.matmul(D, np.linalg.inv(V)))

    #input("Setup complete. Press enter when you are ready to run the test.")

    # these measurements are very noisy, so add an averaging filter.

    print("Case 1: 2 pi3s, no encoding")
    start = time.time()
    r1,t1 = runPowerIteration(M, eigenMax, 2, 0, encodingScheme=False)
    end = time.time()
    print("Time (s): " + str(end - start))

    # Run the case with 2 pi 3s, 2 pi 4s, and no encoding
    print("Case 2: 2 pi3s, 2 pi4s, no encoding")
    start = time.time()
    r2,t2 = runPowerIteration(M, eigenMax, 2, 2, encodingScheme=False)
    end = time.time()
    print("Time (s): " + str(end - start))

    # Run the case with 2 pi 4s
    print("Case 1: 2 pi4s, no encoding")
    start = time.time()
    r3,t3 = runPowerIteration(M, eigenMax, 0, 2, encodingScheme=False)
    end = time.time()
    print("Time (s): " + str(end - start))

    # Run the case with 2 pi 4s, 2 pi 3s, and encoding
    print("Case 1: 2 pi3s, 2 pi4s, encoding")
    start = time.time()
    r4,t4 = runPowerIteration(M, eigenMax, 2, 2, encodingScheme=True)
    end = time.time()
    print("Time (s): " + str(end - start))

    # plot the results 
    plt.plot(t1,r1, label="2x Pi3, no encoding")
    plt.plot(t2, r2, label="2x Pi3, 2x Pi4, no encoding")
    plt.plot(t3, r3, label="2x Pi4, no encoding")
    plt.plot(t4, r4, label="2x Pi3, 2xPi4, encoding")
    plt.yscale('log')
    plt.xlabel("Time (s)")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.show()

    # export the csv
    with open("/home/merek/devel/fl/cec_data.csv", mode='w') as outfile:
        w = csv.writer(outfile)
        w.writerow(np.array(t1))
        w.writerow(np.array(r1))
        w.writerow(np.array(t2))
        w.writerow(np.array(r2))
        w.writerow(np.array(t3))
        w.writerow(np.array(r3))
        w.writerow(np.array(t4))
        w.writerow(np.array(r4))
    return t1[len(t1)-1],t2[len(t2)-1],t3[len(t3)-1],t4[len(t4)-1]

if __name__ == "__main__":
    t = [0,0,0,0]
    for i in range(1):
        t0,t1,t2,t3 = main()
        t[0] += t0
        t[1] += t1
        t[2] += t2
        t[3] += t3

    print(t)

