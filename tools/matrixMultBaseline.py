import numpy as np
import matplotlib.pyplot as plt
import time

if(__name__ == "__main__"):

    # First generate some random matrices
    smallMatrix1 = np.random.rand(100,100)
    smallMatrix2 = np.random.rand(100,100)

    mediumMatrix1 = np.random.rand(1000,1000)
    mediumMatrix2 = np.random.rand(1000,1000)

    largeMatrix1 = np.random.rand(10000,10000)
    largeMatrix2 = np.random.rand(10000,10000)

    
    # First do the small matrix mult, then time it

    start = time.process_time()
    np.matmul(smallMatrix1,smallMatrix2)
    stop = time.process_time()
    t1 = stop - start
    print(t1)

    # Now the medium matrices

    start = time.process_time()
    np.matmul(mediumMatrix1,mediumMatrix2)
    stop = time.process_time()
    t2 = stop - start
    print(t2)

    # Now the large matrices

    start = time.process_time()
    np.matmul(largeMatrix1,largeMatrix2)
    stop = time.process_time()
    t3 = stop - start
    print(t3)

    # plot the comp time vs matrix size
    elm = [100**2,1000**2,10000**2]
    plt.plot(elm,[t1,t2,t3])
    plt.title("Computation time vs. matrix size")
    plt.xlabel("Matrix size")
    plt.ylabel("Computation time (s)")
    plt.show()
