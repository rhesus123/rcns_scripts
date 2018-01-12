#!/bin/bash

#SBATCH -A biomarker_1
#SBATCH --array=1-30
#SBATCH --job-name=align
#SBATCH --time 1-10
#SBATCH --mem-per-cpu=8000
#SBATCH --cpus-per-task=4
#SBATCH -o log
#SBATCH -e err

export PATH=$PATH:/home/oqqn0bf/.local/bin

cd /scratch/oqqn0bf/stanford_rnaseq/fastq
FQ1=`ls *R1_001.fastq.gz | head -n $SLURM_ARRAY_TASK_ID | tail -n 1`
FQ2=${FQ1%R1_001.fastq.gz}R2_001.fastq.gz

hisat2 -p 4 -x /scratch/oqqn0bf/genomes/grch38/hisat2index -1 $FQ1 -2 $FQ2 | samtools view -b - >raw.${SLURM_ARRAY_TASK_ID}.bam
samtools sort -@ 4 -T tmp.${SLURM_ARRAY_TASK_ID} -o ${FQ1%%_S*_R1_001.fastq.gz}.bam raw.${SLURM_ARRAY_TASK_ID}.bam 
samtools index ${FQ1%%_S*_R1_001.fastq.gz}.bam
rm raw.${SLURM_ARRAY_TASK_ID}.bam 
