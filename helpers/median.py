import sys
import os
import shutil
import h5py
import scipy.signal as sig

FILTER_KERNEL_SIZE = 3

if __name__ == '__main__':

    # Read input arguments to get path of file name
    try:
        inputPath = sys.argv[1]
    except:
        print 'No input file path given'
        sys.exit(1)

    # Extract folder, file base, and extension from input path
    inputFolder, inputName = os.path.split(inputPath)
    inputBase, inputExt = os.path.splitext(inputName)

    with h5py.File(inputPath, 'r') as inputFile:

        # Get projection data from input file
        projections = inputFile['ITKImage/0/VoxelData'][:]

    # Filter each projection
    filteredProjections = sig.medfilt(projections, kernel_size=FILTER_KERNEL_SIZE).astype('int16')

    # Formulate output path and copy input file to output path
    outputPath = os.path.join(inputFolder, inputBase + '.medfilt' + inputExt)
    shutil.copyfile(inputPath, outputPath)

    # Open output file and save out projections
    with h5py.File(outputPath, 'r+') as outputFile:

        # Write filtered projections to output file voxel data
        voxelData = outputFile['ITKImage/0/VoxelData']
        voxelData[...] = filteredProjections
