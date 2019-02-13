#!/bin/bash

# Aligner script for the brown fat project
# Using a NUMA architect in HPC Miskolc

#SBATCH -A rbgma
#SBATCH --time=2:00:0
#SBATCH --job-name=rnaseq
#SBATCH -n 8
#SBATCH --mem-per-cpu=40000

cd /big/scratch/pez5mnr/brownfat/fastq

for FASTQ in `ls *.fastq.gz | tail -n +71`
do
  /big/scratch/pez5mnr/brownfat/programs/STAR --runThreadN 8 --genomeDir /big/scratch/pez5mnr/brownfat/genomes/starindex --readFilesIn $FASTQ --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate --outFileNamePrefix /big/scratch/pez5mnr/brownfat/bam/${FASTQ%fastq.gz}
done
