#!/bin/bash

# check that the user sent in a path
if [$1 -eq ""]
then
	echo "Incorrect use."
	echo "Use: wakeOnLan.sh <path to mac addresses file>"
	exit 1
fi

echo "Sending packets to wake up devices..."
wakeonlan -f $1
echo "Sent."
