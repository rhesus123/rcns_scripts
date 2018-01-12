#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --array=1-30
#SBATCH --job-name=fcount
#SBATCH --time 4:00:00
#SBATCH --mem-per-cpu=4000
#SBATCH --cpus-per-task=4
#SBATCH -o log.%a
#SBATCH -e err.%a

export PATH=/home/oqqn0bf/.local/bin:$PATH

cd /scratch/oqqn0bf/stanford_rnaseq/bams
BAM=`ls *.bam | head -n $SLURM_ARRAY_TASK_ID | tail -n 1`

featureCounts -t gene -a /scratch/oqqn0bf/genomes/grch38/Homo_sapiens.GRCh38.91.gff3 -g Name -f -C -T 4 -o ../tables/${BAM%bam}tsv $BAM
