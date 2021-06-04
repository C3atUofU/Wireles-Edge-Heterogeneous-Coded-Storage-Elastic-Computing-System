import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
import os

def main():
    if(len(sys.argv) != 2):
        print("Use: python dataPlotter <path/to/cec_data.csv")
        return

    inpath = os.path.abspath(sys.argv[1])

    # Open the csv file that contains the data.
    # The data is arranged like this:
    # t1
    # r1
    # t2
    # r2
    # t3
    # r3
    # t4
    # r4
    # each of these is a separate array because they may not be the same length.
    # t1 is the time array for the first run, where t1[n] is the time in seconds after the nth power iteration.
    # r1 is the accuracy array for the first run, where r1[n] is the accuracy of the eigenvalue after the nth power iteration.
    with open(inpath) as infile:
        cr = csv.reader(infile,delimiter=',')
        i = 0
        for row in cr:
            if i == 0:
                t1 = np.array(row).astype(float)
            elif i == 1:
                r1 = np.array(row).astype(float)
            elif i == 2:
                t2 = np.array(row).astype(float)
            elif i == 3:
                r2 = np.array(row).astype(float)
            elif i == 4:
                t3 = np.array(row).astype(float)
            elif i == 5:
                r3 = np.array(row).astype(float)
            elif i == 6:
                t4 = np.array(row).astype(float)
            elif i == 7:
                r4 = np.array(row).astype(float)
            print(i)
            i += 1

    # plot the results 
    plt.plot(t1,r1, label="2x Pi3, no encoding")
    plt.plot(t2, r2, label="2x Pi3, 2x Pi4, no encoding")
    plt.plot(t3, r3, label="2x Pi4, no encoding")
    plt.plot(t4, r4, label="2x Pi3, 2xPi4, encoding")
    plt.yscale('log') # log scale on y axis
    plt.xlabel("Time (s)")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
