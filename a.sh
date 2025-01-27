#!/bin/bash

# Loop over temperature values from 2 to 7 with an interval of 0.1
for temp in $(seq 2 0.1 7)
do
    # Set times based on the temperature range
    if (( $(echo "$temp >= 4" | bc -l) )) && (( $(echo "$temp < 5" | bc -l) )); then
        times=10000000
    else
        times=1000000
    fi

    # Call the Python script with the current temperature and times
    echo "python run.py --n_images 100 --times $times --temp $temp"
done





# python run.py --times 1000000 --n_images 100 --temp 7