#!/bin/bash

# Directory setup
OUTPUT_DIR="/home/aritra/projects/metropolis/outputs"
ERROR_DIR="/home/aritra/projects/metropolis/errors"
mkdir -p "$OUTPUT_DIR" "$ERROR_DIR"

# Function to get base times based on N
get_base_time() {
  case $1 in
    128) echo 1000000 ;;
    64)  echo 500000 ;;
    32)  echo 500000 ;;
    16)  echo 100000 ;;
    8)   echo 10000 ;;
    *) echo "Invalid N value: $1"; exit 1 ;;
  esac
}

# Function to get times based on temperature and N
get_times() {
  local temp=$1
  local base_time=$2
  case $temp in
    4.5|4.6|4.7|5.5|5.6|5.7|5.8|5.9) echo $((2 * base_time)) ;;
    4.8|4.9|5.0) echo $((20 * base_time)) ;;
    5.1|5.2|5.3|5.4) echo $((4 * base_time)) ;;
    *) echo $base_time ;;
  esac
}

# Default values
temp_start=2.0
temp_end=7.0
temp_step=0.1
n_images=10000

# Read input arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --N) N="$2"; shift 2;;
    --J) J="$2"; shift 2;;
    --temp_start) temp_start="$2"; shift 2;;
    --temp_end) temp_end="$2"; shift 2;;
    --temp_step) temp_step="$2"; shift 2;;
    --n_images) n_images="$2"; shift 2;;
    *) echo "Unknown argument: $1"; exit 1;;
  esac
done

# Validate required arguments
if [[ -z "$N" || -z "$J" ]]; then
  echo "Usage: $0 --N <N> --J <J> [--temp_start <temp_start>] [--temp_end <temp_end>] [--temp_step <temp_step>] [--n_images <n_images>]"
  exit 1
fi

# Validate N value
if ! [[ "$N" =~ ^(8|16|32|64|128)$ ]]; then
  echo "Error: N must be one of 8, 16, 32, 64, or 128."
  exit 1
fi

# Get base time based on N
base_time=$(get_base_time "$N")

# Loop through temperatures
for temp in $(seq "$temp_start" "$temp_step" "$temp_end"); do
  times=$(get_times "$temp" "$base_time")  # Get --times for current temperature

  qsub <<< "#!/bin/bash
#PBS -N ${J}_${N}_${temp}
#PBS -l nodes=1:ppn=1
#PBS -o ${OUTPUT_DIR}/${temp}.out
#PBS -e ${ERROR_DIR}/${temp}.err

# Conda initialization
eval \"\$(/home/aritra/miniconda3/bin/conda shell.bash hook)\"

cd /home/aritra/projects/metropolis
conda activate metropolis
python run.py --J ${J} --n_images ${n_images} --times ${times} --temp ${temp} --N ${N}
"
done
