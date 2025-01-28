#!/bin/bash

# Directory setup
OUTPUT_DIR="/home/aritra/projects/metropolis/outputs"
ERROR_DIR="/home/aritra/projects/metropolis/errors"
mkdir -p "$OUTPUT_DIR" "$ERROR_DIR"

# Loop through temperatures
for temp in $(seq 2.0 0.1 2.5); do
  qsub <<< "#!/bin/bash
#PBS -N metropolis_job_${temp}
#PBS -l nodes=1:ppn=1
#PBS -o ${OUTPUT_DIR}/${temp}.out
#PBS -e ${ERROR_DIR}/${temp}.err

# Conda initialization
eval \"\$('/home/aritra/miniconda3/bin/conda' 'shell.bash' 'hook')\"

cd /home/aritra/projects/metropolis
conda activate metropolis
python run.py --n_images 100000 --times 10000000 --temp ${temp}"
done