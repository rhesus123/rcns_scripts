#!/bin/bash

# RNA count script for the brown fat project
# in HPC Miskolc

#SBATCH -A rbgma
#SBATCH --time=2:00:0
#SBATCH --job-name=feature
#SBATCH -n 8
#SBATCH --mem-per-cpu=40000

cd /big/scratch/pez5mnr/brownfat/bam

/big/scratch/pez5mnr/brownfat/programs/featureCounts -T 8 -a /big/scratch/pez5mnr/brownfat/genomes/Homo_sapiens.GRCh38.95.gtf -o count.tab *.bam
