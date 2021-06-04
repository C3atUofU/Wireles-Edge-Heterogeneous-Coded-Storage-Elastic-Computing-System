import numpy as np
import time

if __name__ == "__main__":
    start = time.time()

    for i in range(1000):
        a = np.random.rand(100,100)
        b = np.random.rand(100,100)
        np.matmul(a,b)

    end = time.time()
    diff = end - start
    print("Time: " + str(diff))
