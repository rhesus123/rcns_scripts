#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --job-name=mutval
#SBATCH --time 16:00:00
#SBATCH --array=1-100
#SBATCH -o log.%a
#SBATCH -e err.%a

GENES=`ls input* | head -n $SLURM_ARRAY_TASK_ID | tail -n 1`

for g in `cat $GENES`
do
   ./powermw onegroup $g mut.3.1.12.tsv exp.3.1.tsv results/$g.tcga.tsv
   ./powermw onegroup $g mut.3.2.12.tsv exp.3.2.tsv results/$g.meta.tsv
done
