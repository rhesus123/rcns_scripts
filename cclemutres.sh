#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --job-name=mutval
#SBATCH --time 1:00:00
#SBATCH --array=1-100
#SBATCH -o log.%a
#SBATCH -e err.%a

GENES=`ls input* | head -n $SLURM_ARRAY_TASK_ID | tail -n 1`

for g in `cat $GENES`
do
   ./powermw onegroup $g snv.ccle.tsv exp.ccle.tsv ccle_res/$g.ccle.tsv
done
