#!/bin/bash
# Try to identify whether we are on Raspberry Pi or not
# source the /etc/os-release values
# This may not be the best option
. /etc/os-release
echo "System name $NAME"
echo "Select the tests you want to run"
echo "(0-->All tests)"
echo "(1-->Propulsion tests)"
echo "(2-->IR tests)"
read  -p "Enter option >" option 

if [ "$option" -eq 0 ]; then
	echo "Running all tests"
	python3 run_tests.py PLATFORM=$NAME ID=0
	exit 0
elif [ "$option" -eq 1 ]; then
	echo "Running Propulsion tests"	
	python3 run_tests.py PLATFORM=$NAME ID=1
	exit 0
else
	echo "Unknown test type ${option} was selected"
	exit 1
fi
