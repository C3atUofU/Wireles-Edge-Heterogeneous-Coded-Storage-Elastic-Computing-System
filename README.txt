==== INTRO ====

This code was primarily authored by Merek Goodrich as a student at the University of Utah and member of the Computing, Caching, and Communication (C^3) Lab. This project was overseen by Professor Mingyue Ji.

==== PURPOSE ====

The purpose of this code is to be able to perform coded elastic computing on a set of 4 raspberry pis. This set of four raspberry pis is heterogeneous in computation speed. The task this network will perform is power iteration.

==== FOLDER ORGANIZATION ====

This repository is organized into 4 main folders. They are demos, helpers, unused, and tools.

Demos is the main folder of the repository, and contains all of the "main" methods. The files in this folder provide the greatest high-level view of the entire program. 

Helpers is the folder which contains all of the more nitty-gritty methods which make the demos work. This folder is the "how" of demos.

Tools is not used by the main threads, but contains useful scripts that helped to characterize certain aspects of the network, such as timing.

Unused was either code that was discarded from the project or code that was used only as example code. This code is strictly not a part of the project.

==== DEMOS ====

There are three demos included in this repo. They are numbered from 1 to 3. Demo 1 is the most simple, and each demo gets increasingly more complicated.

In order to use the demos, the user will need to do the following setup steps:
    1) Have three or more python 3.4 capable devices.
    2) Set up each device to have a static IP address which will correspond to the IPs found on line 27 of demo 1, or else modify this line to match the IP address of the worker devices.
    3) Ensure that python is installed on all devices with the following libraries included:
        a. numpy
        b. sys
        c. time
        d. selectors
        e. socket
        f. pickle
        g. types
        h. queue
        i. threading
        j. os
        k. matplotlib
    4) Run the program `python3 helpers/node.py` on each of the worker nodes.
    5) Run the desired demo in demos/ on the master node.
    6) Make sure all devices are connected on the same network.

DEMO 1

Demo 1 performs a simple matrix multiplication across 1-4 worker nodes. It generates the data, then encodes the data based on the number of devices the user specifies. It then sends it to each worker node using a websocket protocol. The worker nodes will be running the program "node.py" on each device, which will wait to receive a muliply command, then perform the multiplication, then send the result back to the master node. The master node will then reassemble the received data, compare the result to the expected result, then run the same test with preemption.

The expected use of demo1 follows this syntax:
    python3 demo1.py <number of requested nodes> <recovery threshold> <matrix size>
where number of requested nodes is the number of worker nodes used (must be less than or equal to 4), recovery threshold is the minimum number of non-preempted devices required to guarantee correct completion of the multiplication (must be greater than 1 and less than or equal to 4), and matrix size is the size of the matrix that will be generated and multiplied.

DEMO 2

Demo 2 performs a power iteration using the network.  It first creates a matrix with known eigenvalues and eigenvectors, then runs power iteration a number of times. Efficiency versus uncoded network is given as a result.

DEMO 3

Demo 3 performs a power iteration on the network with heterogeneous encoding capabilities. The intent of this code is that devices 0 and 1 will be lower performance devices than devices 2 and 3. In the case we used, the slow devices were raspberry pi 3s and the fast devices were raspberry pi 4s. 

In demo 3, 4 different cases are run with various device combinations and heterogeneous encoding. The cases are tasked with performing a power iteration to a given accuracy (10^-8) and timed. The four cases tested are 1) 2 slow devices with no heterogeneous encoding, 2) 2 slow devices and 2 fast devices with no heterogeneous encoding, 3) 2 fast devices with no heterogeneous encoding, and 4) 2 slow devices and 2 fast devices with heterogeneous encoding. Each of these cases runs power iteration on the same matrix, and timings are taken. A visual output is given when all the cases have completed.

The expected use of demo3 follows this syntax:
    python3 demo3.py
All of the parameters in this demo are hard coded. The matrix size can be modified in this code by changing the value of the variable n in main.

==== HELPERS ====

node.py

The node object is the main helper function which is used throughout all of the demos. The node object represents a worker node. It has many capabilities including:
    1) sendingLoop: runs on a thread and sends data on a queue to the master node
    2) receivingLoop: runs on a thread and waits for master node to send a command
    3) multLoop: completes matrix multiplication when there is a job available
    4) matrixSplit: partitions a matrix M into n even parts
    5) preempt: stops all sending and multiplication. Keeps receiving running for restart signals
    6) restart: undo preemption by restarting sending and multiplication loops
    7) quit: end the program on this node

client.py

This is the client communication object which will run on the worker node. Make sure that the IP address in this file is up-to-date

server.py

This is the server communication object which runs on the worker node

masterServer.py

This is the server communication object which runs on the master node. Make sure that the IP address in this file is up-to-date.

masterClient.py

This is the client communication object which runs on the master node.

matrixSplit.py

powerIteration.py

This program contains the most basic power iteration program. It takes a matrix and the number of iterations to run and estimates the greatest eigenvalue and its corresponding eigenvector.

==== TOOLS ====

testSpeed.py

When using the heterogenous encoding, each device speed must be known. This program is the way that the relative speed of each device was measured.

dataPlotter.py

This simple program was used to turn .csv files containing raw data from demo 3 into matplotlib.pyplot figures.

matrixMultBaseline.py

This program was used to help determine the size of matrices used in the demo applications. The devices used as worker nodes had specific limitations on RAM that were a large consideration.

beowulf.txt

This is a simple .txt file which was used in early stages to test the node-to-node communication.

==== UNUSED ====

wakeOnLan.sh and macAddresses.wol

This was a script which was written in hopes of setting up the worker nodes to wake-on-lan. Upon reaching multi-user stage, the worker nodes would then automatically run the nodeService as a systemctl service, which would greatly decrease the amount of setup needed to run a single application. Unfortunately, the boards which were used did not have the hardware capabilities to support wake-on-lan magic packets. Those interested with capable hardware could certainly take advantage of this script. The only requirement would be that the master node would need to have the linux package wakeonlan installed. This can be done (on debain distributions) by running the command 
    sudo apt install wakeonlan

The file macAddresses.wol is a text file which contains the mac addresses of all the worker nodes. These mac addresses are necessary for the wake-on-lan protocol to be completed.

The expected syntax of running this command is
    sudo wakeOnLan.sh <path/to/macAddresses.wol>
