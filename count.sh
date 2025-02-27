#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <root_directory>"
    exit 1
fi

root_dir="$1"

for dir in "$root_dir"/*/ ; do
    if [ -d "$dir" ]; then
        count=$(ls -l "$dir" | wc -l)
        echo "$(basename "$dir"): $count"
    fi
done


# 10000_23_128_-1: 49
# 10000_23_128_1: 49
# 10000_23_16_1: 49

# max
# python run.py --J 1 --n_images 100000 --times 10000000 --temp 2.0 --N 32  # 24.5 hrs
# python run.py --J 1 --n_images 100000 --times  2000000 --temp 2.0 --N 16  # 5 hrs
# python run.py --J 1 --n_images 100000 --times   200000 --temp 2.0 --N  8  # 30 mins

# min
# python run.py --J 1 --n_images 100000 --times 500000 --temp 2.0 --N 32  # 1.25 hrs
# python run.py --J 1 --n_images 100000 --times 100000 --temp 2.0 --N 16  #  15 mins
# python run.py --J 1 --n_images 100000 --times  10000 --temp 2.0 --N  8  #  1.5 mins





