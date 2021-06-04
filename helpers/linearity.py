import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt


# Values lower than these gain std. dev. the low cutoff or higher than the high cutoff are bad pixels.
LOW_GAIN_CUTOFF = -1.3
HIGH_GAIN_CUTOFF = 3

# Similar for linearity. These constants can be adjusted as needed. 
LOW_LIN_CUTOFF = -2 
HIGH_LIN_CUTOFF = 2.05


# Find any pixels that are stuck at zero. Return a tuple containing their locations.
def getZeroPixels(imgStack):

    avgImg = np.mean(imgStack, axis=0)
    zeroGainPixels = np.where(avgImg == 0)
    
    print "Zero pixel count:", len(zeroGainPixels[0])

    return zip(zeroGainPixels[1], zeroGainPixels[0])

# Find any pixels that are stuck at high. Return a tuple containing their locations.
def getHighPixels(imgStack):
    
    maxValue = np.iinfo(imgStack.dtype).max
    avgImg = np.mean(imgStack, axis=0)
    maxGainPixels = np.where(avgImg == maxValue)

    print "High pixel count:", len(maxGainPixels[0])

    return zip(maxGainPixels[1], maxGainPixels[0])

# Take a single stack and find the low and high pixels. Return a tuple containing their locations.
def getBadGainPixels(imgStack):

    avgImg = np.mean(imgStack, axis=0)
    normalImg = (avgImg - avgImg.mean()) / avgImg.std()

    lowPixelLocations = np.where(normalImg <  LOW_GAIN_CUTOFF)
    highPixelLocations = np.where(normalImg > HIGH_GAIN_CUTOFF)

    normalNoOutliers = normalImg[abs(normalImg - np.mean(normalImg)) < 5*np.std(normalImg)]
    hist = np.histogram(normalImg,bins=10,range=(normalNoOutliers.min(),normalNoOutliers.max()))
    bins = hist[1] 
    pixelsInBins = hist[0] 
    
    # use this to visualize results in development
    #plt.hist(normalNoOutliers,bins='auto')
    #plt.xlabel("Std. Dev.")
    #plt.ylabel("Count")
    #plt.title("Variance in gain")
    #plt.show()
 
    print "Low gain pixel count:", lowPixelLocations[1].shape[0]
    print "High gain pixel count:", highPixelLocations[1].shape[0]

    # Use this to visualize results in development
    #plt.subplot(1,2,1)
    #plt.scatter(lowPixelLocations[1],lowPixelLocations[0], s=1, c='red')
    #plt.imshow(avgImg)
    #plt.title("Low Pixels")
    
    #plt.subplot(1,2,2)
    #plt.scatter(highPixelLocations[1],highPixelLocations[0], s=1, c='red')
    #plt.imshow(avgImg)
    #plt.title("High Pixels")
        
    #plt.show()

    return zip(lowPixelLocations[1], lowPixelLocations[0]), zip(highPixelLocations[1], highPixelLocations[0]), bins, pixelsInBins
        
# Takes two stacks and finds pixels that are non-linear in gain. Return their locations.
def getNonLinearPixels(lowDose, highDose):
    
    diffImg = np.mean(highDose - lowDose, axis=0)
    normalImg = (diffImg - diffImg.mean()) / diffImg.std()
    
    nonLinearMask = np.logical_or(normalImg > HIGH_LIN_CUTOFF, normalImg < LOW_LIN_CUTOFF)
    nonLinearPixelLocations = np.where(nonLinearMask)

    # Use this to visualize results in development
    #plt.subplot(1,2,1)
    #plt.scatter(nonLinearPixelLocations[1],nonLinearPixelLocations[0],s=1,c='red')
    #plt.imshow(normalImg)
    #plt.title("Non-linear Pixels")
    #plt.subplot(1,2,2)
    #plt.imshow(normalImg)
    #plt.title("Normalized Difference")
    #plt.show()
    
    normalNoOutliers = normalImg[abs(normalImg - np.mean(normalImg)) < 5*np.std(normalImg)]
    hist = np.histogram(normalImg,bins=10,range=(normalNoOutliers.min(),normalNoOutliers.max()))
    bins = hist[1]
    pixelsInBins = hist[0]

    print "Non-linear pixel count:", len(nonLinearPixelLocations[0]) 

    # use this to visualize results in development
    #plt.hist(normalNoOutliers,bins='auto')
    #plt.xlabel("Std. Dev.")
    #plt.ylabel("Count")
    #plt.title("Variance in linearity")
    #plt.show()

    # As far as I can tell, linearity catches all bad pixels. If this changes, we can implement an intersection script to catch these cases.
    print "Total bad Pixels:", len(nonLinearPixelLocations[0])

    return zip(nonLinearPixelLocations[1], nonLinearPixelLocations[0]), bins, pixelsInBins

def main():
    
    if(len(sys.argv)!=3):
        print "Use: python BadPixelIdentifier <path to imageStack_60kV.h5> <path to imageStack_75kV.h5>"
        return

    with h5py.File(sys.argv[1], 'r') as input60kVFile, h5py.File(sys.argv[2],'r') as input75kVFile:
        stack60 = input60kVFile['ITKImage/0/VoxelData'][:]
        stack75 = input75kVFile['ITKImage/0/VoxelData'][:]
    
    # Check that the sizes are the same.
    assert stack60.shape == stack75.shape
    size = stack60.shape[1]*stack60.shape[2]

    # Call the helper functions and store the data 
    zeroGainPixels = getZeroPixels(stack60)
    maxGainPixels = getHighPixels(stack60)
    lowGainPixels,highGainPixels,bins_Gain,pixelsInBins_Gain = getBadGainPixels(stack60)
    nonLinearPixels,bins_Lin,pixelsInBins_Lin = getNonLinearPixels(stack60,stack75)

    deadPixelSet = set(zeroGainPixels + maxGainPixels + lowGainPixels + highGainPixels + nonLinearPixels)

    # Create an output file and add the information.
    # DEAD Pixels
    output = open("output.txt","w")
    output.write("==================Zero Pixels==================\n\n")
    line = "Pixels stuck at zero count: " + str(len(zeroGainPixels)) + "\n"
    output.write(line)

    # HIGH Pixels
    output.write("\n==================High Pixels==================\n\n")
    line = "Pixels stuck at high count: " +str(len(maxGainPixels)) +"\n"
    output.write(line)
    
    # GAIN Pixels
    output.write("\n==================Pixel Gain==================\n\n")
    output.write("Distribution of pixel gain:\n")
    for i in range(0,len(pixelsInBins_Gain)):
        line = "\t Pixels %.2f" % bins_Gain[i] + " std.dev. from mean: " + str(pixelsInBins_Gain[i]) + " (%.2f" % (pixelsInBins_Gain[i]*100/size) +"%)" +"\n"
        output.write(line)
    line = "\nLow cutoff: " + str(LOW_GAIN_CUTOFF) +"\n"
    output.write(line)
    line = "High cutoff: " + str(HIGH_GAIN_CUTOFF) +"\n"
    output.write(line)
    line = "Count of pixels below low cutoff: " + str(len(lowGainPixels))  + "\n"
    output.write(line)
    line = "Count of pixels above high cutoff: " + str(len(highGainPixels))+ "\n\n"
    output.write(line)
    line = "Total bad pixels from gain: " + str(len(lowGainPixels)+len(highGainPixels)) + "\n"
    output.write(line)

    # LINEAR Pixels
    output = open("output.txt","a")
    output.write("\n==================Pixel Linearity==================\n\n")
    output.write("Distribution of pixel gain:\n")
    output.write("\nDistribution of pixel linearity:\n")
    for i in range(0,len(pixelsInBins_Lin)):
        line = "\t Pixels " + str(bins_Lin[i]) + " std.dev. from slope: " + str(pixelsInBins_Lin[i]) + " (%.2f" % (pixelsInBins_Lin[i]*100/size) +"%)" +"\n"
        output.write(line)
    line = "\nLow cutoff: " + str(LOW_LIN_CUTOFF) +"\n"
    output.write(line)
    line = "High cutoff: " + str(HIGH_LIN_CUTOFF) +"\n"
    output.write(line)
    line = "Count of pixels outside linearity range: " + str(len(nonLinearPixels))  + "\n\n"
    output.write(line)

    # Write the type of dead pixels to the end of output.txt
    output = open("output.txt","a")

    output.write("==============Bad Pixel Locations==============\n\n")

    output.write("Location of zero pixels: \n")
    for pixel in zeroGainPixels:
        output.write(str(pixel) + "\n")

    output.write("Location of high pixels:\n")
    for pixel in maxGainPixels:
        output.write(str(pixel)+"\n")

    output.write("\nLocation of low gain pixels: \n")
    for pixel in lowGainPixels:
        output.write(str(pixel) + '\n')

    output.write("\nLocation of high gain pixels:\n")
    for pixel in highGainPixels:
        output.write(str(pixel) + '\n')

    output.write("\nLocation of non-linear pixels:\n")
    for pixel in nonLinearPixels:
        output.write(str(pixel) + '\n')

    # Write the dead pixels to deadPixMap.txt in the working directory.
    deadPix = open("deadPixMap.txt","w")
    for pixel in deadPixelSet:
        line = "[" + str(pixel[0]) + "," + str(pixel[1]) + "]"
        deadPix.write(line + '\n')
        
    print "Detailed statistics saved as output.txt."
    print "Importable dead pixel map saved as deadPixMap.txt."

if __name__ == '__main__':
    main()

