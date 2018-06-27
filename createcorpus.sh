#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --array=46-50,53,55-58,60,62,63,64,67-71,73,75-78,80,81,83
#SBATCH --job-name=ccrp
#SBATCH --time 4-00
#SBATCH --mem-per-cpu=80000
#SBATCH -o log.%a
#SBATCH -e err.%a

XML=`ls *.gz | head -n $SLURM_ARRAY_TASK_ID | tail -n 1`

python extracttext.py $XML >${SLURM_ARRAY_TASK_ID}.txt
