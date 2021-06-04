import numpy as np
import sys

def main():

    if(len(sys.argv) != 3):
        print("use: split matrix <size of matrix> <number of splits>")

    try:
        sizeA = int(sys.argv[1])
        n = int(sys.argv[2])
    except:
        print("Inputs must be ints.")
        return

    A = np.random.rand(sizeA,sizeA)
    matrixSplit(A,n)

# This script will take a matrix and divide it into n parts.
# It will make the parts as evenly sized as possible while still maintaining the rows and columns.
def matrixSplit(matrix, n):

    diff = 0
    fraction = len(matrix)/n
    for i in range(0,n):
        split  = round(fraction + diff)
        print(split)
        diff = diff + fraction - split
        print(diff)

if(__name__ == "__main__"):
    main()
