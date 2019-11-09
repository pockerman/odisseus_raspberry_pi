#!/bin/bash
clear
# Try to identify whether we are on Raspberry Pi or not
# source the /etc/os-release values
# This may not be the best option
. /etc/os-release
echo "System name $NAME"
echo "Select the tests you want to run:

1. Propulsion tests
2. IR tests
3. Ultrasound tests
4. Camera tests
5. Master process tests
6. All tests
0. Quit
"

read  -p "Enter option [0-6] > "

if [[ "$REPLY" =~ ^[0-6]$ ]]; then
	if [[ "$REPLY" == 0 ]]; then
		echo "Terminating program"
		exit 
	fi
	if [[ "$REPLY" -eq 1 ]]; then
		echo "Running Propulsion tests"	
		python3 run_tests.py "PLATFORM=$NAME" "ID=$REPLY"
		exit 0
	fi
	if [[ "$REPLY" -eq 2 ]]; then
		echo "Running IR tests..."
		echo "This is not enabled yet"	
		python3 run_tests.py PLATFORM=$NAME ID=$REPLY
		exit 0
	fi
	if [[ "$REPLY" -eq 3 ]]; then
		echo "Ultrasound tests..."
		python3 run_tests.py PLATFORM=$NAME ID=$REPLY
		exit 0
	fi
	if [[ "$REPLY" -eq 4 ]]; then
		echo "Camera tests..."
		python3 run_tests.py PLATFORM=$NAME ID=$REPLY
		exit 0
	fi
	if [[ "$REPLY" -eq 5 ]]; then
	  echo "Master process tests..."
	  python3 run_tests.py PLATFORM=$NAME ID=$REPLY
	  exit
	fi
	if [[ "$REPLY" -eq 6 ]]; then
		echo "Running all tests..."
		python3 run_tests.py PLATFORM=$NAME ID=$REPLY
		exit 0
	fi
else
	echo "Unknown test type ${REPLY} was selected" >&2
	exit 1
fi
